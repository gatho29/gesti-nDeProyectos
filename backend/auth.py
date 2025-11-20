"""
Módulo de autenticación y autorización
"""
from functools import wraps
from flask import session, redirect, url_for, request, jsonify
from models import Usuario

def login_required(f):
    """Decorador para requerir autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'No autenticado'}), 401
        return f(*args, **kwargs)
    return decorated_function

def role_required(roles):
    """Decorador para requerir roles específicos"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'error': 'No autenticado'}), 401
            
            user = Usuario.obtener_por_id(session['user_id'])
            if not user or user['rol'] not in roles:
                return jsonify({'error': 'Acceso denegado'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def get_current_user():
    """Obtiene el usuario actual de la sesión"""
    if 'user_id' not in session:
        return None
    return Usuario.obtener_por_id(session['user_id'])

def verificar_permisos_proyecto(usuario, proyecto_id):
    """Verifica si un usuario tiene permisos sobre un proyecto"""
    from models import Proyecto
    
    proyecto = Proyecto.obtener_por_id(proyecto_id)
    if not proyecto:
        return False
    
    # Administrador tiene acceso a todos los proyectos
    if usuario['rol'] == 'Administrador':
        return True
    
    # Gestor solo tiene acceso a sus proyectos
    if usuario['rol'] == 'Gestor':
        return proyecto['responsable_id'] == usuario['id']
    
    # Colaborador solo puede ver proyectos donde tiene tareas
    if usuario['rol'] == 'Colaborador':
        from models import Tarea
        tareas = Tarea.obtener_por_proyecto(proyecto_id)
        return any(tarea['asignado_a_id'] == usuario['id'] for tarea in tareas)
    
    return False

