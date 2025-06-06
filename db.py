# db.py
import sqlite3

DATABASE = 'database.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            nombre_registrado TEXT NOT NULL,
            apellido1 TEXT NOT NULL,
            apellido2 TEXT,
            telefono_whatsapp TEXT NOT NULL,
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

def create_user(username, password, nombre_registrado, apellido1, apellido2,
                telefono_whatsapp, otro_telefono, correo_electronico,
                avatar_url, pais, provincia, busco):
    conn = sqlite3.connect(DATABASE)
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
        print("Error: Username or email already exists.")
        return False
    finally:
        conn.close()

def get_user_by_username_or_phone(identifier):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? OR telefono_whatsapp = ? OR correo_electronico = ?',
                   (identifier, identifier, identifier))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        # Convertir a diccionario para fácil acceso por nombre de columna
        columns = [description[0] for description in cursor.description]
        return dict(zip(columns, user_data))
    return None

def get_user_by_id(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        columns = [description[0] for description in cursor.description]
        user_dict = dict(zip(columns, user_data))
        print(f"DEBUG: Datos de usuario obtenidos de DB para ID {user_id}: {user_dict['username']}") # DEBUG PRINT
        return user_dict
    print(f"DEBUG: No se encontraron datos de usuario para ID {user_id}") # DEBUG PRINT
    return None

def update_user_profile(user_id, **kwargs):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Construir la parte SET de la consulta SQL dinámicamente
    set_clauses = []
    values = []
    for key, value in kwargs.items():
        set_clauses.append(f"{key} = ?")
        values.append(value)
    
    if not set_clauses:
        conn.close()
        return False # No hay nada que actualizar

    sql = f"UPDATE users SET {', '.join(set_clauses)} WHERE id = ?"
    values.append(user_id)

    try:
        cursor.execute(sql, tuple(values))
        conn.commit()
        print(f"DEBUG: Perfil de usuario {user_id} actualizado exitosamente.") # DEBUG PRINT
        return True
    except Exception as e:
        print(f"DEBUG: Error al actualizar perfil de usuario {user_id}: {e}") # DEBUG PRINT
        return False
    finally:
        conn.close()