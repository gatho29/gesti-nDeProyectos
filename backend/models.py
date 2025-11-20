"""
Modelos de datos del sistema
"""
import sqlite3
from database import get_db_connection
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, date

class Usuario:
    """Modelo de Usuario"""
    
    @staticmethod
    def crear(nombre, email, password, rol='Colaborador'):
        """Crea un nuevo usuario"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            password_hash = generate_password_hash(password)
            cursor.execute('''
                INSERT INTO usuarios (nombre, email, password_hash, rol)
                VALUES (?, ?, ?, ?)
            ''', (nombre, email, password_hash, rol))
            conn.commit()
            user_id = cursor.lastrowid
            return {'id': user_id, 'nombre': nombre, 'email': email, 'rol': rol}
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    @staticmethod
    def obtener_por_email(email):
        """Obtiene un usuario por su email"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None
    
    @staticmethod
    def obtener_por_id(user_id):
        """Obtiene un usuario por su ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, nombre, email, rol FROM usuarios WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None
    
    @staticmethod
    def verificar_password(user, password):
        """Verifica la contraseña de un usuario"""
        return check_password_hash(user['password_hash'], password)
    
    @staticmethod
    def obtener_todos():
        """Obtiene todos los usuarios"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, nombre, email, rol FROM usuarios ORDER BY nombre')
        users = cursor.fetchall()
        conn.close()
        return [dict(user) for user in users]

class Proyecto:
    """Modelo de Proyecto"""
    
    @staticmethod
    def crear(nombre, descripcion, responsable_id, fecha_inicio, fecha_fin):
        """Crea un nuevo proyecto"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO proyectos (nombre, descripcion, responsable_id, fecha_inicio, fecha_fin)
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre, descripcion, responsable_id, fecha_inicio, fecha_fin))
        
        conn.commit()
        proyecto_id = cursor.lastrowid
        conn.close()
        
        return Proyecto.obtener_por_id(proyecto_id)
    
    @staticmethod
    def obtener_por_id(proyecto_id):
        """Obtiene un proyecto por su ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.*, u.nombre as responsable_nombre
            FROM proyectos p
            JOIN usuarios u ON p.responsable_id = u.id
            WHERE p.id = ?
        ''', (proyecto_id,))
        proyecto = cursor.fetchone()
        conn.close()
        return dict(proyecto) if proyecto else None
    
    @staticmethod
    def obtener_todos(usuario_id=None, rol=None):
        """Obtiene todos los proyectos, filtrados por usuario y rol"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if rol == 'Administrador':
            cursor.execute('''
                SELECT p.*, u.nombre as responsable_nombre
                FROM proyectos p
                JOIN usuarios u ON p.responsable_id = u.id
                ORDER BY p.fecha_creacion DESC
            ''')
        elif rol == 'Gestor':
            cursor.execute('''
                SELECT p.*, u.nombre as responsable_nombre
                FROM proyectos p
                JOIN usuarios u ON p.responsable_id = u.id
                WHERE p.responsable_id = ?
                ORDER BY p.fecha_creacion DESC
            ''', (usuario_id,))
        else:
            # Colaborador ve proyectos donde tiene tareas asignadas
            cursor.execute('''
                SELECT DISTINCT p.*, u.nombre as responsable_nombre
                FROM proyectos p
                JOIN usuarios u ON p.responsable_id = u.id
                JOIN tareas t ON t.proyecto_id = p.id
                WHERE t.asignado_a_id = ?
                ORDER BY p.fecha_creacion DESC
            ''', (usuario_id,))
        
        proyectos = cursor.fetchall()
        conn.close()
        return [dict(proyecto) for proyecto in proyectos]
    
    @staticmethod
    def actualizar(proyecto_id, nombre=None, descripcion=None, fecha_inicio=None, 
                   fecha_fin=None, estado=None):
        """Actualiza un proyecto"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        updates = []
        values = []
        
        if nombre:
            updates.append('nombre = ?')
            values.append(nombre)
        if descripcion is not None:
            updates.append('descripcion = ?')
            values.append(descripcion)
        if fecha_inicio:
            updates.append('fecha_inicio = ?')
            values.append(fecha_inicio)
        if fecha_fin:
            updates.append('fecha_fin = ?')
            values.append(fecha_fin)
        if estado:
            updates.append('estado = ?')
            values.append(estado)
        
        if updates:
            values.append(proyecto_id)
            query = f'UPDATE proyectos SET {", ".join(updates)} WHERE id = ?'
            cursor.execute(query, values)
            conn.commit()
        
        conn.close()
        return Proyecto.obtener_por_id(proyecto_id)
    
    @staticmethod
    def calcular_progreso(proyecto_id):
        """Calcula el progreso de un proyecto basado en tareas completadas"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as total FROM tareas WHERE proyecto_id = ?', (proyecto_id,))
        total = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as completadas FROM tareas WHERE proyecto_id = ? AND estado = ?', 
                      (proyecto_id, 'Finalizado'))
        completadas = cursor.fetchone()['completadas']
        
        conn.close()
        
        if total == 0:
            return 0
        return int((completadas / total) * 100)

class Tarea:
    """Modelo de Tarea"""
    
    @staticmethod
    def crear(titulo, descripcion, proyecto_id, creado_por_id, asignado_a_id=None,
              prioridad='Media', fecha_limite=None):
        """Crea una nueva tarea"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO tareas (titulo, descripcion, proyecto_id, creado_por_id, 
                              asignado_a_id, prioridad, fecha_limite)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (titulo, descripcion, proyecto_id, creado_por_id, asignado_a_id, 
              prioridad, fecha_limite))
        
        conn.commit()
        tarea_id = cursor.lastrowid
        conn.close()
        
        return Tarea.obtener_por_id(tarea_id)
    
    @staticmethod
    def obtener_por_id(tarea_id):
        """Obtiene una tarea por su ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.*, 
                   u1.nombre as asignado_nombre,
                   u2.nombre as creado_por_nombre,
                   p.nombre as proyecto_nombre
            FROM tareas t
            LEFT JOIN usuarios u1 ON t.asignado_a_id = u1.id
            JOIN usuarios u2 ON t.creado_por_id = u2.id
            JOIN proyectos p ON t.proyecto_id = p.id
            WHERE t.id = ?
        ''', (tarea_id,))
        tarea = cursor.fetchone()
        conn.close()
        return dict(tarea) if tarea else None
    
    @staticmethod
    def obtener_por_proyecto(proyecto_id):
        """Obtiene todas las tareas de un proyecto"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.*, 
                   u1.nombre as asignado_nombre,
                   u2.nombre as creado_por_nombre
            FROM tareas t
            LEFT JOIN usuarios u1 ON t.asignado_a_id = u1.id
            JOIN usuarios u2 ON t.creado_por_id = u2.id
            WHERE t.proyecto_id = ?
            ORDER BY t.fecha_creacion DESC
        ''', (proyecto_id,))
        tareas = cursor.fetchall()
        conn.close()
        return [dict(tarea) for tarea in tareas]
    
    @staticmethod
    def obtener_por_usuario(usuario_id):
        """Obtiene todas las tareas asignadas a un usuario"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.*, 
                   u.nombre as creado_por_nombre,
                   p.nombre as proyecto_nombre
            FROM tareas t
            JOIN usuarios u ON t.creado_por_id = u.id
            JOIN proyectos p ON t.proyecto_id = p.id
            WHERE t.asignado_a_id = ?
            ORDER BY t.fecha_limite ASC
        ''', (usuario_id,))
        tareas = cursor.fetchall()
        conn.close()
        return [dict(tarea) for tarea in tareas]
    
    @staticmethod
    def obtener_por_estado(estado, usuario_id=None, proyecto_id=None):
        """Obtiene tareas por estado, opcionalmente filtradas por usuario o proyecto"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT t.*, 
                   u1.nombre as asignado_nombre,
                   u2.nombre as creado_por_nombre,
                   p.nombre as proyecto_nombre
            FROM tareas t
            LEFT JOIN usuarios u1 ON t.asignado_a_id = u1.id
            JOIN usuarios u2 ON t.creado_por_id = u2.id
            JOIN proyectos p ON t.proyecto_id = p.id
            WHERE t.estado = ?
        '''
        params = [estado]
        
        if usuario_id:
            query += ' AND t.asignado_a_id = ?'
            params.append(usuario_id)
        
        if proyecto_id:
            query += ' AND t.proyecto_id = ?'
            params.append(proyecto_id)
        
        query += ' ORDER BY t.fecha_limite ASC'
        
        cursor.execute(query, params)
        tareas = cursor.fetchall()
        conn.close()
        return [dict(tarea) for tarea in tareas]
    
    @staticmethod
    def actualizar_estado(tarea_id, nuevo_estado):
        """Actualiza el estado de una tarea"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE tareas 
            SET estado = ?, fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (nuevo_estado, tarea_id))
        
        conn.commit()
        conn.close()
        
        return Tarea.obtener_por_id(tarea_id)
    
    @staticmethod
    def actualizar(tarea_id, titulo=None, descripcion=None, asignado_a_id=None,
                   prioridad=None, fecha_limite=None):
        """Actualiza una tarea"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        updates = []
        values = []
        
        if titulo:
            updates.append('titulo = ?')
            values.append(titulo)
        if descripcion is not None:
            updates.append('descripcion = ?')
            values.append(descripcion)
        if asignado_a_id is not None:
            updates.append('asignado_a_id = ?')
            values.append(asignado_a_id)
        if prioridad:
            updates.append('prioridad = ?')
            values.append(prioridad)
        if fecha_limite is not None:
            updates.append('fecha_limite = ?')
            values.append(fecha_limite)
        
        if updates:
            updates.append('fecha_actualizacion = CURRENT_TIMESTAMP')
            values.append(tarea_id)
            query = f'UPDATE tareas SET {", ".join(updates)} WHERE id = ?'
            cursor.execute(query, values)
            conn.commit()
        
        conn.close()
        return Tarea.obtener_por_id(tarea_id)
    
    @staticmethod
    def esta_retrasada(tarea):
        """Verifica si una tarea está retrasada"""
        if tarea['estado'] == 'Finalizado':
            return False
        
        if tarea['fecha_limite']:
            fecha_limite = datetime.strptime(tarea['fecha_limite'], '%Y-%m-%d').date()
            return fecha_limite < date.today()
        
        return False

class Reporte:
    """Modelo para generar reportes"""
    
    @staticmethod
    def obtener_metricas_generales():
        """Obtiene métricas generales del sistema"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total de proyectos
        cursor.execute('SELECT COUNT(*) as total FROM proyectos')
        total_proyectos = cursor.fetchone()['total']
        
        # Total de tareas
        cursor.execute('SELECT COUNT(*) as total FROM tareas')
        total_tareas = cursor.fetchone()['total']
        
        # Tareas completadas
        cursor.execute('SELECT COUNT(*) as total FROM tareas WHERE estado = ?', ('Finalizado',))
        tareas_completadas = cursor.fetchone()['total']
        
        # Tareas retrasadas
        cursor.execute('''
            SELECT COUNT(*) as total 
            FROM tareas 
            WHERE estado != ? AND fecha_limite < date('now')
        ''', ('Finalizado',))
        tareas_retrasadas = cursor.fetchone()['total']
        
        # Tareas por estado
        cursor.execute('''
            SELECT estado, COUNT(*) as cantidad
            FROM tareas
            GROUP BY estado
        ''')
        tareas_por_estado = {row['estado']: row['cantidad'] for row in cursor.fetchall()}
        
        conn.close()
        
        return {
            'total_proyectos': total_proyectos,
            'total_tareas': total_tareas,
            'tareas_completadas': tareas_completadas,
            'tareas_retrasadas': tareas_retrasadas,
            'tareas_por_estado': tareas_por_estado,
            'porcentaje_completado': int((tareas_completadas / total_tareas * 100)) if total_tareas > 0 else 0
        }
    
    @staticmethod
    def obtener_metricas_proyecto(proyecto_id):
        """Obtiene métricas de un proyecto específico"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total de tareas del proyecto
        cursor.execute('SELECT COUNT(*) as total FROM tareas WHERE proyecto_id = ?', (proyecto_id,))
        total_tareas = cursor.fetchone()['total']
        
        # Tareas completadas
        cursor.execute('SELECT COUNT(*) as total FROM tareas WHERE proyecto_id = ? AND estado = ?', 
                      (proyecto_id, 'Finalizado'))
        tareas_completadas = cursor.fetchone()['total']
        
        # Tareas retrasadas
        cursor.execute('''
            SELECT COUNT(*) as total 
            FROM tareas 
            WHERE proyecto_id = ? AND estado != ? AND fecha_limite < date('now')
        ''', (proyecto_id, 'Finalizado'))
        tareas_retrasadas = cursor.fetchone()['total']
        
        # Tareas por estado
        cursor.execute('''
            SELECT estado, COUNT(*) as cantidad
            FROM tareas
            WHERE proyecto_id = ?
            GROUP BY estado
        ''', (proyecto_id,))
        tareas_por_estado = {row['estado']: row['cantidad'] for row in cursor.fetchall()}
        
        conn.close()
        
        return {
            'total_tareas': total_tareas,
            'tareas_completadas': tareas_completadas,
            'tareas_retrasadas': tareas_retrasadas,
            'tareas_por_estado': tareas_por_estado,
            'porcentaje_completado': int((tareas_completadas / total_tareas * 100)) if total_tareas > 0 else 0
        }
    
    @staticmethod
    def obtener_metricas_usuario(usuario_id):
        """Obtiene métricas de un usuario específico"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total de tareas asignadas
        cursor.execute('SELECT COUNT(*) as total FROM tareas WHERE asignado_a_id = ?', (usuario_id,))
        total_tareas = cursor.fetchone()['total']
        
        # Tareas completadas
        cursor.execute('SELECT COUNT(*) as total FROM tareas WHERE asignado_a_id = ? AND estado = ?', 
                      (usuario_id, 'Finalizado'))
        tareas_completadas = cursor.fetchone()['total']
        
        # Tareas retrasadas
        cursor.execute('''
            SELECT COUNT(*) as total 
            FROM tareas 
            WHERE asignado_a_id = ? AND estado != ? AND fecha_limite < date('now')
        ''', (usuario_id, 'Finalizado'))
        tareas_retrasadas = cursor.fetchone()['total']
        
        conn.close()
        
        return {
            'total_tareas': total_tareas,
            'tareas_completadas': tareas_completadas,
            'tareas_retrasadas': tareas_retrasadas,
            'porcentaje_completado': int((tareas_completadas / total_tareas * 100)) if total_tareas > 0 else 0
        }

