import sqlite3

def create_tables():
    conn = sqlite3.connect('indigo.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        nombre_usuario TEXT NOT NULL UNIQUE,
        telefono TEXT NOT NULL,
        correo TEXT NOT NULL UNIQUE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        categoria TEXT NOT NULL,
        nombre TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        imagen BLOB,
        precio REAL NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS opciones_personalizacion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto_id INTEGER NOT NULL,
        tipo TEXT NOT NULL,
        opcion TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        FOREIGN KEY (producto_id) REFERENCES productos(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pedidos_especiales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT NOT NULL,
        usuario_id INTEGER NOT NULL,
        imagen BLOB,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS registro_compras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha_hora TEXT NOT NULL,
        usuario_id INTEGER,
        nombre_apellido TEXT,
        direccion_envio TEXT,
        tipo_producto TEXT NOT NULL,
        producto_id INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        pago REAL NOT NULL,
        metodo_pago TEXT NOT NULL,
        estado TEXT NOT NULL,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
        FOREIGN KEY (producto_id) REFERENCES productos(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS comentarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        producto_id INTEGER NOT NULL,
        comentario TEXT NOT NULL,
        estrellas INTEGER NOT NULL,
        fecha_hora TEXT NOT NULL,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
        FOREIGN KEY (producto_id) REFERENCES productos(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS carrito (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        producto_id INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        opciones TEXT,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
        FOREIGN KEY (producto_id) REFERENCES productos(id)
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
