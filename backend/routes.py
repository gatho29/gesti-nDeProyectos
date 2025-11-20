"""
Rutas de la API del sistema
"""
from flask import Blueprint, request, jsonify, session
from models import Usuario, Proyecto, Tarea, Reporte
from auth import login_required, role_required, get_current_user, verificar_permisos_proyecto

api = Blueprint('api', __name__)

# ==================== AUTENTICACIÓN ====================

@api.route('/api/auth/login', methods=['POST'])
def login():
    """Endpoint para autenticación de usuarios"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email y contraseña son requeridos'}), 400
    
    user = Usuario.obtener_por_email(email)
    if not user or not Usuario.verificar_password(user, password):
        return jsonify({'error': 'Credenciales inválidas'}), 401
    
    # Crear sesión
    session['user_id'] = user['id']
    session['user_email'] = user['email']
    session['user_rol'] = user['rol']
    
    return jsonify({
        'message': 'Login exitoso',
        'user': {
            'id': user['id'],
            'nombre': user['nombre'],
            'email': user['email'],
            'rol': user['rol']
        }
    }), 200

@api.route('/api/auth/logout', methods=['POST'])
def logout():
    """Endpoint para cerrar sesión"""
    session.clear()
    return jsonify({'message': 'Sesión cerrada'}), 200

@api.route('/api/auth/me', methods=['GET'])
@login_required
def get_current_user_info():
    """Obtiene información del usuario actual"""
    user = get_current_user()
    if user:
        return jsonify({
            'id': user['id'],
            'nombre': user['nombre'],
            'email': user['email'],
            'rol': user['rol']
        }), 200
    return jsonify({'error': 'Usuario no encontrado'}), 404

# ==================== USUARIOS ====================

@api.route('/api/usuarios', methods=['GET'])
@login_required
@role_required(['Administrador'])
def obtener_usuarios():
    """Obtiene todos los usuarios (solo administradores)"""
    usuarios = Usuario.obtener_todos()
    return jsonify(usuarios), 200

@api.route('/api/usuarios', methods=['POST'])
@login_required
@role_required(['Administrador'])
def crear_usuario():
    """Crea un nuevo usuario (solo administradores)"""
    data = request.get_json()
    
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')
    rol = data.get('rol', 'Colaborador')
    
    if not nombre or not email or not password:
        return jsonify({'error': 'Nombre, email y contraseña son requeridos'}), 400
    
    if rol not in ['Administrador', 'Gestor', 'Colaborador']:
        return jsonify({'error': 'Rol inválido'}), 400
    
    user = Usuario.crear(nombre, email, password, rol)
    if user:
        return jsonify(user), 201
    return jsonify({'error': 'El email ya está registrado'}), 409

# ==================== PROYECTOS ====================

@api.route('/api/proyectos', methods=['GET'])
@login_required
def obtener_proyectos():
    """Obtiene todos los proyectos según el rol del usuario"""
    user = get_current_user()
    proyectos = Proyecto.obtener_todos(user['id'], user['rol'])
    return jsonify(proyectos), 200

@api.route('/api/proyectos', methods=['POST'])
@login_required
@role_required(['Administrador', 'Gestor'])
def crear_proyecto():
    """Crea un nuevo proyecto"""
    data = request.get_json()
    user = get_current_user()
    
    nombre = data.get('nombre')
    descripcion = data.get('descripcion', '')
    responsable_id = data.get('responsable_id', user['id'])
    fecha_inicio = data.get('fecha_inicio')
    fecha_fin = data.get('fecha_fin')
    
    if not nombre or not fecha_inicio or not fecha_fin:
        return jsonify({'error': 'Nombre, fecha inicio y fecha fin son requeridos'}), 400
    
    # Solo administradores pueden asignar otros responsables
    if user['rol'] != 'Administrador':
        responsable_id = user['id']
    
    proyecto = Proyecto.crear(nombre, descripcion, responsable_id, fecha_inicio, fecha_fin)
    if proyecto:
        return jsonify(proyecto), 201
    return jsonify({'error': 'Error al crear proyecto'}), 500

@api.route('/api/proyectos/<int:proyecto_id>', methods=['GET'])
@login_required
def obtener_proyecto(proyecto_id):
    """Obtiene un proyecto específico"""
    user = get_current_user()
    
    if not verificar_permisos_proyecto(user, proyecto_id):
        return jsonify({'error': 'Acceso denegado'}), 403
    
    proyecto = Proyecto.obtener_por_id(proyecto_id)
    if proyecto:
        proyecto['progreso'] = Proyecto.calcular_progreso(proyecto_id)
        return jsonify(proyecto), 200
    return jsonify({'error': 'Proyecto no encontrado'}), 404

@api.route('/api/proyectos/<int:proyecto_id>', methods=['PUT'])
@login_required
@role_required(['Administrador', 'Gestor'])
def actualizar_proyecto(proyecto_id):
    """Actualiza un proyecto"""
    user = get_current_user()
    
    if not verificar_permisos_proyecto(user, proyecto_id):
        return jsonify({'error': 'Acceso denegado'}), 403
    
    data = request.get_json()
    proyecto = Proyecto.actualizar(
        proyecto_id,
        nombre=data.get('nombre'),
        descripcion=data.get('descripcion'),
        fecha_inicio=data.get('fecha_inicio'),
        fecha_fin=data.get('fecha_fin'),
        estado=data.get('estado')
    )
    
    if proyecto:
        return jsonify(proyecto), 200
    return jsonify({'error': 'Error al actualizar proyecto'}), 500

# ==================== TAREAS ====================

@api.route('/api/tareas', methods=['GET'])
@login_required
def obtener_tareas():
    """Obtiene tareas según el rol del usuario"""
    user = get_current_user()
    proyecto_id = request.args.get('proyecto_id', type=int)
    estado = request.args.get('estado')
    
    if estado:
        tareas = Tarea.obtener_por_estado(estado, user['id'] if user['rol'] == 'Colaborador' else None, proyecto_id)
    elif proyecto_id:
        if not verificar_permisos_proyecto(user, proyecto_id):
            return jsonify({'error': 'Acceso denegado'}), 403
        tareas = Tarea.obtener_por_proyecto(proyecto_id)
    elif user['rol'] == 'Colaborador':
        tareas = Tarea.obtener_por_usuario(user['id'])
    else:
        # Administradores y gestores ven todas las tareas de sus proyectos
        proyectos = Proyecto.obtener_todos(user['id'], user['rol'])
        tareas = []
        for proyecto in proyectos:
            tareas.extend(Tarea.obtener_por_proyecto(proyecto['id']))
    
    return jsonify(tareas), 200

@api.route('/api/tareas', methods=['POST'])
@login_required
@role_required(['Administrador', 'Gestor'])
def crear_tarea():
    """Crea una nueva tarea"""
    data = request.get_json()
    user = get_current_user()
    
    titulo = data.get('titulo')
    descripcion = data.get('descripcion', '')
    proyecto_id = data.get('proyecto_id')
    asignado_a_id = data.get('asignado_a_id')
    prioridad = data.get('prioridad', 'Media')
    fecha_limite = data.get('fecha_limite')
    
    if not titulo or not proyecto_id:
        return jsonify({'error': 'Título y proyecto son requeridos'}), 400
    
    if not verificar_permisos_proyecto(user, proyecto_id):
        return jsonify({'error': 'Acceso denegado al proyecto'}), 403
    
    tarea = Tarea.crear(titulo, descripcion, proyecto_id, user['id'], asignado_a_id, prioridad, fecha_limite)
    if tarea:
        return jsonify(tarea), 201
    return jsonify({'error': 'Error al crear tarea'}), 500

@api.route('/api/tareas/<int:tarea_id>', methods=['GET'])
@login_required
def obtener_tarea(tarea_id):
    """Obtiene una tarea específica"""
    user = get_current_user()
    tarea = Tarea.obtener_por_id(tarea_id)
    
    if not tarea:
        return jsonify({'error': 'Tarea no encontrada'}), 404
    
    # Verificar permisos
    if not verificar_permisos_proyecto(user, tarea['proyecto_id']):
        if user['rol'] == 'Colaborador' and tarea['asignado_a_id'] != user['id']:
            return jsonify({'error': 'Acceso denegado'}), 403
    
    return jsonify(tarea), 200

@api.route('/api/tareas/<int:tarea_id>', methods=['PUT'])
@login_required
def actualizar_tarea(tarea_id):
    """Actualiza una tarea"""
    user = get_current_user()
    tarea = Tarea.obtener_por_id(tarea_id)
    
    if not tarea:
        return jsonify({'error': 'Tarea no encontrada'}), 404
    
    data = request.get_json()
    
    # Colaboradores solo pueden actualizar el estado
    if user['rol'] == 'Colaborador':
        if tarea['asignado_a_id'] != user['id']:
            return jsonify({'error': 'Acceso denegado'}), 403
        
        nuevo_estado = data.get('estado')
        if nuevo_estado:
            tarea = Tarea.actualizar_estado(tarea_id, nuevo_estado)
            return jsonify(tarea), 200
    else:
        # Gestores y administradores pueden actualizar todo
        if not verificar_permisos_proyecto(user, tarea['proyecto_id']):
            return jsonify({'error': 'Acceso denegado'}), 403
        
        tarea = Tarea.actualizar(
            tarea_id,
            titulo=data.get('titulo'),
            descripcion=data.get('descripcion'),
            asignado_a_id=data.get('asignado_a_id'),
            prioridad=data.get('prioridad'),
            fecha_limite=data.get('fecha_limite')
        )
        
        if data.get('estado'):
            tarea = Tarea.actualizar_estado(tarea_id, data.get('estado'))
    
    return jsonify(tarea), 200

# ==================== REPORTES ====================

@api.route('/api/reportes/generales', methods=['GET'])
@login_required
@role_required(['Administrador'])
def obtener_reportes_generales():
    """Obtiene reportes generales del sistema (solo administradores)"""
    metricas = Reporte.obtener_metricas_generales()
    return jsonify(metricas), 200

@api.route('/api/reportes/proyecto/<int:proyecto_id>', methods=['GET'])
@login_required
def obtener_reporte_proyecto(proyecto_id):
    """Obtiene reportes de un proyecto específico"""
    user = get_current_user()
    
    if not verificar_permisos_proyecto(user, proyecto_id):
        return jsonify({'error': 'Acceso denegado'}), 403
    
    metricas = Reporte.obtener_metricas_proyecto(proyecto_id)
    return jsonify(metricas), 200

@api.route('/api/reportes/usuario/<int:usuario_id>', methods=['GET'])
@login_required
def obtener_reporte_usuario(usuario_id):
    """Obtiene reportes de un usuario específico"""
    user = get_current_user()
    
    # Solo puede ver su propio reporte o ser administrador
    if user['id'] != usuario_id and user['rol'] != 'Administrador':
        return jsonify({'error': 'Acceso denegado'}), 403
    
    metricas = Reporte.obtener_metricas_usuario(usuario_id)
    return jsonify(metricas), 200

