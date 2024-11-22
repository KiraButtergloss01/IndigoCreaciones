import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, send_from_directory, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import paypalrestsdk
from config import paypalrestsdk
from forms import RegistrationForm, ProductForm
from helpers import apology, login_required, usd
# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///indigo.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/statics/<path:filename>')
def static_files(filename):
    return send_from_directory('statics', filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos/centro_mesa')
def centros_de_mesa():
    productos = db.execute("SELECT * FROM productos WHERE categoria = 'Centros de Mesa'")
    return render_template('productos/centro_mesa.html', productos=productos)

@app.route('/productos/papeleria_decorada')
def papeleria_decorada():
    productos = db.execute("SELECT * FROM productos WHERE categoria = 'Papelería Decorada'")
    return render_template('productos/papeleria_decorada.html', productos=productos)

@app.route('/productos/tarjetas')
def tarjetas_invitaciones():
    productos = db.execute("SELECT * FROM productos WHERE categoria = 'Tarjetas e Invitaciones'")
    return render_template('productos/tarjetas.html', productos=productos)

@app.route('/productos/cajas')
def cajas():
    productos = db.execute("SELECT * FROM productos WHERE categoria = 'Cajas'")
    return render_template('productos/cajas.html', productos=productos)

@app.route('/productos/arreglos_dulces')
def arreglos_dulces():
    productos = db.execute("SELECT * FROM productos WHERE categoria = 'Arreglos con Dulces'")
    return render_template('productos/arreglos_dulces.html', productos=productos)

@app.route('/productos/pedidos')
def pedidos_especiales():
    productos = db.execute("SELECT * FROM productos WHERE categoria = 'Pedidos Especiales'")
    return render_template('productos/pedidos.html', productos=productos)

@app.route('/productos/detalle/<int:producto_id>')
def detalle_producto(producto_id):
    producto = db.execute("SELECT * FROM productos WHERE id = ?", producto_id)
    opciones = db.execute("SELECT * FROM opciones_personalizacion WHERE producto_id = ?", producto_id)
    return render_template('productos/detalle_producto.html', producto=producto[0], opciones=opciones)

@app.route('/usuario/compras_anteriores')
@login_required
def compras_anteriores():
    usuario_id = session["user_id"]
    compras = db.execute("SELECT * FROM registro_compras WHERE usuario_id = ?", usuario_id)
    return render_template('usuario/compras_anteriores.html', compras=compras)

@app.route('/usuario/pedidos_actuales')
@login_required
def pedidos_actuales():
    usuario_id = session["user_id"]
    pedidos = db.execute("SELECT * FROM registro_compras WHERE usuario_id = ? AND estado = 'Pendiente'", usuario_id)
    return render_template('usuario/pedidos_actuales.html', pedidos=pedidos)

@app.route('/usuario/carrito_compras')
@login_required
def carrito_compras():
    carrito = session.get("cart", [])
    return render_template('usuario/carrito_compras.html', carrito=carrito)

@app.route('/admin/agregar_producto', methods=["GET", "POST"])
@login_required
def agregar_producto():
    form = ProductForm()
    if form.validate_on_submit():
        categoria = form.categoria.data
        nombre = form.nombre.data
        descripcion = form.descripcion.data
        precio = form.precio.data
        imagen = form.imagen.data.read() if form.imagen.data else None
        db.execute("INSERT INTO productos (categoria, nombre, descripcion, imagen, precio) VALUES (?, ?, ?, ?, ?)",
        categoria, nombre, descripcion, imagen, precio)
        flash("Producto agregado exitosamente")
        return redirect(url_for("agregar_producto"))
    return render_template('admin/agregar_producto.html', form=form)

@app.route('/admin/editar_producto/<int:producto_id>', methods=["GET", "POST"])
@login_required
def editar_producto(producto_id):
    if request.method == "POST":
        nombre = request.form.get("nombre")
        descripcion = request.form.get("descripcion")
        precio = request.form.get("precio")
        imagen = request.files["imagen"].read() if request.files["imagen"] else None
        db.execute("UPDATE productos SET nombre = ?, descripcion = ?, precio = ?, imagen = ? WHERE id = ?",
        nombre, descripcion, precio, imagen, producto_id)
        flash("Producto actualizado exitosamente")
        return redirect(url_for("editar_producto", producto_id=producto_id))
    producto = db.execute("SELECT * FROM productos WHERE id = ?", producto_id)
    return render_template('admin/editar_producto.html', producto=producto[0])

@app.route('/admin/gestionar_pedidos')
@login_required
def gestionar_pedidos():
    pedidos = db.execute("SELECT * FROM registro_compras")
    return render_template('admin/gestionar_pedidos.html', pedidos=pedidos)

@app.route('/admin/actualizar_estado/<int:pedido_id>', methods=["POST"])
@login_required
def actualizar_estado(pedido_id):
    nuevo_estado = request.form.get("estado")
    db.execute("UPDATE registro_compras SET estado = ? WHERE id = ?", nuevo_estado, pedido_id)
    flash("Estado del pedido actualizado")
    return redirect(url_for('gestionar_pedidos'))

@app.route('/admin/actualizar_notas/<int:pedido_id>', methods=["POST"])
@login_required
def actualizar_notas(pedido_id):
    nuevas_notas = request.form.get("notas")
    db.execute("UPDATE registro_compras SET notas = ? WHERE id = ?", nuevas_notas, pedido_id)
    flash("Notas del pedido actualizadas")
    return redirect(url_for('gestionar_pedidos'))

@app.route('/admin/detalle_pedido/<int:pedido_id>')
@login_required
def detalle_pedido(pedido_id):
    pedido = db.execute("SELECT * FROM registro_compras WHERE id = ?", pedido_id)
    return render_template('admin/detalle_pedido.html', pedido=pedido[0])

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            return apology("must provide username", 403)
        password = request.form.get("password")
        if not password:
            return apology("must provide password", 403)
        rows = db.execute("SELECT * FROM usuarios WHERE nombre_usuario = ?", username)
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 403)
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        hash = generate_password_hash(password)
        try:
            new_user = db.execute("INSERT INTO usuarios (nombre_usuario, hash) VALUES (?, ?)", username, hash)
        except:
            return apology("USERNAME TAKEN >:(")
        session["user_id"] = new_user
        return redirect("/")
    return render_template("register.html", form=form)


@app.route("/add_to_cart/<int:producto_id>", methods=["POST"])
@login_required
def add_to_cart(producto_id):
    cantidad = int(request.form.get("cantidad"))
    opciones = {key: request.form[key] for key in request.form if key != "cantidad"}
    if "cart" not in session:
        session["cart"] = []
    session["cart"].append({"producto_id": producto_id, "cantidad": cantidad, "opciones": opciones})
    session.modified = True
    return redirect(url_for("detalle_producto", producto_id=producto_id))

@app.route("/checkout", methods=["POST"])
@login_required
def checkout():
    usuario_id = session["user_id"]
    direccion_envio = request.form.get("direccion_envio")
    metodo_pago = request.form.get("metodo_pago")
    carrito = session.get("cart", [])
    for item in carrito:
        producto_id = item["producto_id"]
        cantidad = item["cantidad"]
        opciones = item["opciones"]
        pago = calcular_pago(producto_id, cantidad)
        db.execute("INSERT INTO registro_compras (fecha_hora, usuario_id, producto_id, cantidad, pago, metodo_pago, estado, direccion_envio) VALUES (datetime('now'), ?, ?, ?, ?, ?, 'Pendiente', ?)", usuario_id, producto_id, cantidad, pago, metodo_pago, direccion_envio)
    session.pop("cart", None)
    return redirect(url_for("confirmacion"))

def calcular_pago(producto_id, cantidad):
    producto = db.execute("SELECT precio FROM productos WHERE id = ?", producto_id)
    return producto[0]["precio"] * cantidad
@app.route('/pay', methods=['POST'])
@login_required
def pay():
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": url_for('payment_execute', _external=True),
            "cancel_url": url_for('index', _external=True)},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "item",
                    "sku": "item",
                    "price": "5.00",
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": "5.00",
                "currency": "USD"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print("Payment created successfully")
        for link in payment.links:
            if link.rel == "approval_url":
                approval_url = str(link.href)
                return redirect(approval_url)
    else:
        print(payment.error)
        return apology("An error occurred during the payment process")

@app.route('/payment/execute', methods=['GET'])
@login_required
def payment_execute():
    payment_id = request.args.get('paymentId')
    payer_id = request.args.get('PayerID')
    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        print("Payment executed successfully")
        return redirect(url_for('index'))
    else:
        print(payment.error)
        return apology("An error occurred during the payment execution")

if __name__ == "__main__":
    app.run(debug=True)
