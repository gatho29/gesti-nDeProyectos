"""
Configuración de la base de datos
"""
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash

DATABASE = 'proyectos.db'

def get_db_connection():
    """Obtiene una conexión a la base de datos"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa la base de datos con las tablas necesarias"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tabla Usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            rol TEXT NOT NULL CHECK(rol IN ('Administrador', 'Gestor', 'Colaborador')),
            fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla Proyectos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proyectos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            responsable_id INTEGER NOT NULL,
            fecha_inicio DATE NOT NULL,
            fecha_fin DATE NOT NULL,
            estado TEXT DEFAULT 'Activo' CHECK(estado IN ('Activo', 'Pausado', 'Completado')),
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (responsable_id) REFERENCES usuarios(id)
        )
    ''')
    
    # Tabla Tareas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            proyecto_id INTEGER NOT NULL,
            asignado_a_id INTEGER,
            creado_por_id INTEGER NOT NULL,
            estado TEXT DEFAULT 'Pendiente' CHECK(estado IN ('Pendiente', 'En Progreso', 'Finalizado')),
            prioridad TEXT DEFAULT 'Media' CHECK(prioridad IN ('Baja', 'Media', 'Alta')),
            fecha_limite DATE,
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (proyecto_id) REFERENCES proyectos(id),
            FOREIGN KEY (asignado_a_id) REFERENCES usuarios(id),
            FOREIGN KEY (creado_por_id) REFERENCES usuarios(id)
        )
    ''')
    
    # Tabla Reportes (cache)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reportes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            proyecto_id INTEGER,
            usuario_id INTEGER,
            datos TEXT,
            fecha_generacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (proyecto_id) REFERENCES proyectos(id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')
    
    # Crear usuario administrador por defecto si no existe
    cursor.execute('SELECT * FROM usuarios WHERE email = ?', ('admin@proyectos.com',))
    admin = cursor.fetchone()
    
    if not admin:
        password_hash = generate_password_hash('admin123')
        cursor.execute('''
            INSERT INTO usuarios (nombre, email, password_hash, rol)
            VALUES (?, ?, ?, ?)
        ''', ('Administrador', 'admin@proyectos.com', password_hash, 'Administrador'))
    
    conn.commit()
    conn.close()
    print("Base de datos inicializada correctamente")

if __name__ == '__main__':
    init_db()

