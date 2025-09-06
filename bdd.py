import sqlite3

DB_NAME = "bdd-chat-mjs.db"

def init_bdd():
    """
    se inicializa la base de datos y se crea la tabla si no existe
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
        print("base de datos inicializada correctamente!")
        
    except sqlite3.Error as e:
        print(f"error de SQLite: {e}")
        raise

def guardar_mensaje(contenido, fecha_envio, ip_cliente):
    """
    se guarda un mensaje en la base de datos
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO mensajes (contenido, fecha_envio, ip_cliente) VALUES (?, ?, ?)",
            (contenido, fecha_envio, ip_cliente)
        )
        
        conn.commit()
        conn.close()
        
    except sqlite3.Error as e:
        print(f"error al guardar mensaje: {e}")
        raise