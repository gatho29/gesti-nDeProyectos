# Guía de Instalación - Sistema de Gestión de Proyectos

## Requisitos Previos

Antes de instalar el sistema, asegúrate de tener instalado:

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Un navegador web moderno (Chrome, Firefox, Edge, Safari)

## Instalación Paso a Paso

### 1. Clonar o Descargar el Proyecto

Si tienes el proyecto en un repositorio Git:
```bash
git clone <url-del-repositorio>
cd proyecto-gestion
```

O simplemente navega a la carpeta del proyecto si ya la tienes.

### 2. Crear un Entorno Virtual (Recomendado)

Es recomendable usar un entorno virtual para aislar las dependencias:

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**En Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

Con el entorno virtual activado, instala las dependencias:

```bash
pip install -r requirements.txt
```

Esto instalará:
- Flask 3.0.0
- Flask-CORS 4.0.0
- Werkzeug 3.0.1
- bcrypt 4.1.1
- python-dotenv 1.0.0

### 4. Inicializar la Base de Datos

Ejecuta el script de inicialización para crear la base de datos y el usuario administrador:

```bash
cd backend
python init_db.py
```

Esto creará:
- La base de datos `proyectos.db`
- Las tablas necesarias
- Un usuario administrador por defecto:
  - Email: `admin@proyectos.com`
  - Contraseña: `admin123`

**⚠️ IMPORTANTE**: Cambia la contraseña del administrador después del primer acceso en producción.

### 5. Ejecutar la Aplicación

Desde la raíz del proyecto, ejecuta:

```bash
cd backend
python app.py
```

O desde la raíz del proyecto:

```bash
python backend/app.py
```

Deberías ver un mensaje como:

```
==================================================
Sistema de Gestión de Proyectos
==================================================
Servidor iniciado en http://localhost:5000
Usuario administrador por defecto:
  Email: admin@proyectos.com
  Contraseña: admin123
==================================================
```

### 6. Acceder a la Aplicación

Abre tu navegador y ve a:

```
http://localhost:5000
```

## Uso Inicial

### Primer Inicio de Sesión

1. Ve a `http://localhost:5000/login.html`
2. Inicia sesión con:
   - Email: `admin@proyectos.com`
   - Contraseña: `admin123`

### Crear Usuarios Adicionales

Como administrador, puedes crear usuarios adicionales:

1. Ve a la sección de Reportes (temporalmente, desde la consola del servidor o directamente en la base de datos)
2. O crea usuarios programáticamente desde la API

**Nota**: La creación de usuarios desde la interfaz web se puede implementar en una versión futura. Por ahora, puedes usar la API directamente o agregarlos manualmente a la base de datos.

### Crear tu Primer Proyecto

1. Ve a la sección "Proyectos"
2. Haz clic en "Nuevo Proyecto"
3. Completa el formulario:
   - Nombre del proyecto
   - Descripción (opcional)
   - Fecha de inicio y fin
   - Responsable (si eres administrador)

### Crear Tareas

1. Ve a la sección "Kanban" o "Proyectos"
2. Haz clic en "Nueva Tarea"
3. Completa el formulario:
   - Título
   - Descripción (opcional)
   - Proyecto
   - Asignado a (opcional)
   - Prioridad
   - Fecha límite (opcional)

### Usar el Tablero Kanban

1. Ve a la sección "Kanban"
2. Verás las tareas organizadas por columnas (Pendiente, En Progreso, Finalizado)
3. Arrastra y suelta las tareas entre columnas para cambiar su estado

## Solución de Problemas

### Error: "No module named 'flask'"

**Solución**: Asegúrate de haber activado el entorno virtual e instalado las dependencias:
```bash
pip install -r requirements.txt
```

### Error: "Address already in use"

**Solución**: El puerto 5000 está en uso. Puedes:
1. Cerrar la aplicación que está usando el puerto
2. O cambiar el puerto en `backend/app.py`:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

### Error al cargar la base de datos

**Solución**: Asegúrate de ejecutar `init_db.py` antes de iniciar la aplicación:
```bash
cd backend
python init_db.py
```

### No puedo iniciar sesión

**Solución**: Verifica que:
1. La base de datos esté inicializada
2. Estés usando las credenciales correctas (admin@proyectos.com / admin123)
3. El servidor esté ejecutándose correctamente

## Estructura de Archivos

```
proyecto-gestion/
├── backend/
│   ├── app.py              # Aplicación principal
│   ├── database.py         # Configuración BD
│   ├── models.py           # Modelos de datos
│   ├── auth.py             # Autenticación
│   ├── routes.py           # Rutas API
│   ├── init_db.py          # Inicialización BD
│   └── proyectos.db        # Base de datos (se crea automáticamente)
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── dashboard.html
│   ├── proyectos.html
│   ├── kanban.html
│   ├── reportes.html
│   ├── css/
│   │   └── styles.css
│   └── js/
│       ├── auth.js
│       ├── app.js
│       └── kanban.js
├── docs/
│   ├── analisis-requisitos.md
│   ├── diseño-sistema.md
│   └── informe-final.md
├── requirements.txt
├── README.md
└── INSTALACION.md
```

## Desarrollo

### Modo de Desarrollo

El servidor se ejecuta en modo debug por defecto. Esto significa que:
- Los cambios en el código se recargan automáticamente
- Se muestran mensajes de error detallados
- No es apropiado para producción

### Modo de Producción

Para producción, considera:
1. Configurar un servidor WSGI (como Gunicorn)
2. Usar una base de datos más robusta (PostgreSQL)
3. Configurar HTTPS
4. Cambiar la clave secreta en `app.py`
5. Desactivar el modo debug

## Soporte

Para problemas o preguntas:
1. Revisa la documentación en la carpeta `docs/`
2. Consulta el README.md principal
3. Revisa los mensajes de error en la consola del servidor

## Licencia

Este proyecto fue desarrollado como trabajo final académico.

