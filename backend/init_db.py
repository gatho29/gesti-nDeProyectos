"""
Script para inicializar la base de datos
"""
from database import init_db

if __name__ == '__main__':
    init_db()
    print("✓ Base de datos inicializada")
    print("✓ Usuario administrador creado: admin@proyectos.com / admin123")

