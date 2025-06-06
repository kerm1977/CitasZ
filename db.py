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
        conn.close()
        print(f"DEBUG: Usuario {username} creado exitosamente.")
        return True
    except sqlite3.IntegrityError:
        print(f"DEBUG: Error al crear usuario {username}: ya existe un usuario con ese username o correo.")
        conn.close()
        return False

def get_user_by_username_or_phone(identifier):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? OR telefono_whatsapp = ?', (identifier, identifier))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
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
        print(f"DEBUG: Datos de usuario obtenidos de DB para ID {user_id}: {user_dict['username']}")
        return user_dict
    print(f"DEBUG: No se encontraron datos de usuario para ID {user_id}")
    return None

def update_user_profile(user_id, **kwargs):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    set_clauses = []
    values = []
    for key, value in kwargs.items():
        set_clauses.append(f"{key} = ?")
        values.append(value)
    
    if not set_clauses:
        conn.close()
        return False

    sql = f"UPDATE users SET {', '.join(set_clauses)} WHERE id = ?"
    values.append(user_id)

    try:
        cursor.execute(sql, tuple(values))
        conn.commit()
        conn.close()
        print(f"DEBUG: Perfil del usuario {user_id} actualizado exitosamente.")
        return True
    except Exception as e:
        print(f"DEBUG: Error al actualizar perfil del usuario {user_id}: {e}")
        conn.close()
        return False

# --- NUEVAS FUNCIONES PARA RECUPERACIÓN DE CONTRASEÑA ---
def get_user_by_username_or_email(identifier):
    """Busca un usuario por su nombre de usuario o correo electrónico."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? OR correo_electronico = ?', (identifier, identifier))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        columns = [description[0] for description in cursor.description]
        return dict(zip(columns, user_data))
    return None

def update_user_password(user_id, new_password):
    """Actualiza la contraseña de un usuario."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE users SET password = ? WHERE id = ?', (new_password, user_id))
        conn.commit()
        conn.close()
        print(f"DEBUG: Contraseña del usuario {user_id} actualizada exitosamente.")
        return True
    except Exception as e:
        print(f"DEBUG: Error al actualizar contraseña del usuario {user_id}: {e}")
        conn.close()
        return False