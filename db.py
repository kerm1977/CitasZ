import sqlite3

DATABASE = 'db.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Esto permite acceder a las columnas por nombre
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            nombre_registrado TEXT,
            apellido1 TEXT,
            apellido2 TEXT,
            telefono_whatsapp TEXT,
            otro_telefono TEXT,
            correo_electronico TEXT UNIQUE NOT NULL,
            avatar_url TEXT,
            pais TEXT,
            provincia TEXT,
            busco TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Inicializa la base de datos al importar el módulo
init_db()

def create_user(username, password, nombre_registrado=None, apellido1=None, apellido2=None,
                telefono_whatsapp=None, otro_telefono=None, correo_electronico=None,
                avatar_url=None, pais=None, provincia=None, busco=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (username, password, nombre_registrado, apellido1, apellido2,
                               telefono_whatsapp, otro_telefono, correo_electronico,
                               avatar_url, pais, provincia, busco)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, password, nombre_registrado, apellido1, apellido2,
              telefono_whatsapp, otro_telefono, correo_electronico,
              avatar_url, pais, provincia, busco))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print("Error: El nombre de usuario o correo electrónico ya existe.")
        return False
    finally:
        conn.close()

def get_user_by_username_or_phone(identifier):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? OR telefono_whatsapp = ?", (identifier, identifier))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def update_user_profile(user_id, **kwargs):
    conn = get_db_connection()
    cursor = conn.cursor()
    set_clauses = []
    values = []
    for key, value in kwargs.items():
        set_clauses.append(f"{key} = ?")
        values.append(value)
    values.append(user_id)

    query = f"UPDATE users SET {', '.join(set_clauses)} WHERE id = ?"
    cursor.execute(query, tuple(values))
    conn.commit()
    conn.close()
    return True