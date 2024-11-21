from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
# Configure application
app = Flask(__name__)


db = SQL("sqlite:///indigo.db")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos/centros_de_mesa')
def centros_de_mesa():
    return render_template('productos/centros_de_mesa.html')

@app.route('/productos/papeleria_decorada')
def papeleria_decorada():
    return render_template('productos/papeleria_decorada.html')

@app.route('/productos/tarjetas_invitaciones')
def tarjetas_invitaciones():
    return render_template('productos/tarjetas_invitaciones.html')

@app.route('/productos/cajas')
def cajas():
    return render_template('productos/cajas.html')

@app.route('/productos/arreglos_dulces')
def arreglos_dulces():
    return render_template('productos/arreglos_dulces.html')

@app.route('/productos/pedidos_especiales')
def pedidos_especiales():
    return render_template('productos/pedidos_especiales.html')

@app.route('/productos/detalle/<int:producto_id>')
def detalle_producto(producto_id):
    # Aquí puedes obtener los detalles del producto desde la base de datos
    return render_template('productos/detalle_producto.html', producto_id=producto_id)

@app.route('/usuario/compras_anteriores')
def compras_anteriores():
    return render_template('usuario/compras_anteriores.html')

@app.route('/usuario/pedidos_actuales')
def pedidos_actuales():
    return render_template('usuario/pedidos_actuales.html')

@app.route('/usuario/carrito_compras')
def carrito_compras():
    return render_template('usuario/carrito_compras.html')

@app.route('/admin/agregar_producto')
def agregar_producto():
    return render_template('admin/agregar_producto.html')

@app.route('/admin/editar_producto/<int:producto_id>')
def editar_producto(producto_id):
    # Aquí puedes obtener los detalles del producto desde la base de datos
    return render_template('admin/editar_producto.html', producto_id=producto_id)

@app.route('/admin/gestionar_pedidos')
def gestionar_pedidos():
    return render_template('admin/gestionar_pedidos.html')

