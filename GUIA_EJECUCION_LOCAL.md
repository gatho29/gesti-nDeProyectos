# 🚀 Guía Completa para Ejecutar el Proyecto Localmente

Esta guía te ayudará a ejecutar el **Sistema de Gestión de Proyectos** en tu máquina local paso a paso.

---

## 📋 Requisitos Previos

### Software Necesario

1. **Python 3.8 o superior**
   - Descarga desde: https://www.python.org/downloads/
   - **IMPORTANTE**: Durante la instalación, marca la opción **"Add Python to PATH"**
   - Verifica la instalación ejecutando:
     ```powershell
     python --version
     ```
     O en Windows puede ser:
     ```powershell
     py --version
     ```

2. **pip** (viene incluido con Python)
   - Verifica con: `pip --version`

3. **Navegador web moderno**
   - Chrome, Firefox, Edge o Safari
   - (El proyecto usa Chart.js desde CDN, requiere conexión a internet)

4. **Conexión a Internet** (solo la primera vez)
   - Para descargar las dependencias de Python
   - Para cargar Chart.js desde CDN en la página de reportes

---

## 📁 Estructura del Proyecto

```
proyecto-gestion/
├── backend/                    # Código del servidor Flask
│   ├── app.py                 # Aplicación principal
│   ├── database.py            # Configuración de base de datos SQLite
│   ├── models.py              # Modelos de datos (Usuario, Proyecto, Tarea, Reporte)
│   ├── auth.py                # Autenticación y autorización
│   ├── routes.py              # Rutas de la API REST
│   ├── init_db.py             # Script de inicialización de BD
│   └── proyectos.db           # Base de datos (se crea automáticamente)
│
├── frontend/                   # Interfaz de usuario
│   ├── index.html             # Página principal
│   ├── login.html             # Página de login
│   ├── dashboard.html         # Dashboard principal
│   ├── proyectos.html         # Gestión de proyectos
│   ├── kanban.html            # Tablero Kanban
│   ├── reportes.html          # Página de reportes (usa Chart.js CDN)
│   ├── css/
│   │   └── styles.css         # Estilos principales
│   └── js/
│       ├── auth.js            # Manejo de autenticación
│       ├── app.js             # Lógica principal
│       └── kanban.js          # Funcionalidad Kanban drag & drop
│
├── docs/                       # Documentación
├── requirements.txt            # Dependencias de Python
├── README.md                   # Documentación general
└── INSTALACION.md             # Guía de instalación
```

---

## 🔧 Instalación Paso a Paso

### Paso 1: Navegar al Directorio del Proyecto

Abre PowerShell o Terminal en la carpeta del proyecto:

```powershell
cd C:\proyecto-gestion
```

### Paso 2: Crear Entorno Virtual (Recomendado)

Es buena práctica usar un entorno virtual para aislar las dependencias:

**Windows PowerShell:**
```powershell
python -m venv venv
```

Si `python` no funciona, prueba:
```powershell
py -m venv venv
```

### Paso 3: Activar el Entorno Virtual

**Windows PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

Si obtienes un error de política de ejecución, ejecuta primero:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Windows CMD:**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

Deberías ver `(venv)` al inicio de tu línea de comandos.

### Paso 4: Instalar Dependencias

Con el entorno virtual activado, instala todas las dependencias:

```powershell
pip install -r requirements.txt
```

Esto instalará:
- **Flask 3.0.0** - Framework web
- **Flask-CORS 4.0.0** - Soporte para CORS
- **Werkzeug 3.0.1** - Utilidades WSGI
- **bcrypt 4.1.1** - Encriptación de contraseñas
- **python-dotenv 1.0.0** - Variables de entorno (opcional)

### Paso 5: Inicializar la Base de Datos

Ejecuta el script que crea la base de datos y el usuario administrador:

```powershell
cd backend
python init_db.py
```

O desde la raíz del proyecto:

```powershell
python backend/init_db.py
```

Esto creará:
- ✅ Base de datos SQLite: `backend/proyectos.db`
- ✅ Tablas: `usuarios`, `proyectos`, `tareas`, `reportes`
- ✅ Usuario administrador por defecto

**Credenciales del administrador:**
- Email: `admin@proyectos.com`
- Contraseña: `admin123`

⚠️ **IMPORTANTE**: Cambia esta contraseña después del primer acceso en producción.

### Paso 6: Ejecutar la Aplicación

Desde la raíz del proyecto:

```powershell
python backend/app.py
```

O desde la carpeta backend:

```powershell
cd backend
python app.py
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
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://0.0.0.0:5000
Press CTRL+C to quit
```

### Paso 7: Acceder a la Aplicación

Abre tu navegador y ve a:

```
http://localhost:5000
```

O directamente al login:

```
http://localhost:5000/login.html
```

Inicia sesión con:
- **Email**: `admin@proyectos.com`
- **Contraseña**: `admin123`

---

## 🎯 Uso del Sistema

### Primeros Pasos

1. **Iniciar Sesión**: Usa las credenciales del administrador
2. **Crear Usuarios** (como Administrador):
   - Puedes crear usuarios a través de la API o directamente en la base de datos
   - Los roles disponibles son: `Administrador`, `Gestor`, `Colaborador`

3. **Crear un Proyecto**:
   - Ve a la sección "Proyectos"
   - Haz clic en "Nuevo Proyecto"
   - Completa el formulario

4. **Crear Tareas**:
   - Ve a "Proyectos" o "Kanban"
   - Crea tareas y asígnalas a usuarios

5. **Usar el Tablero Kanban**:
   - Arrastra y suelta tareas entre columnas (Pendiente, En Progreso, Finalizado)
   - Los cambios se guardan automáticamente

6. **Ver Reportes**:
   - Los administradores ven reportes generales
   - Los gestores ven reportes de sus proyectos
   - Los colaboradores ven sus reportes personales

---

## 🔍 Verificación de Funcionamiento

### Verificar que Todo Está Funcionando

1. **Backend corriendo**: El mensaje en la consola muestra "Running on http://0.0.0.0:5000"

2. **Base de datos creada**: Verifica que existe el archivo:
   ```
   backend/proyectos.db
   ```

3. **Frontend carga**: Al abrir `http://localhost:5000`, deberías ver la página principal

4. **Login funciona**: Puedes iniciar sesión con las credenciales del administrador

5. **API responde**: Abre las herramientas de desarrollador (F12) y verifica que no hay errores en la consola

---

## 🐛 Solución de Problemas Comunes

### Error: "No module named 'flask'"

**Solución:**
1. Verifica que el entorno virtual esté activado (deberías ver `(venv)` en la terminal)
2. Reinstala las dependencias:
   ```powershell
   pip install -r requirements.txt
   ```

### Error: "Address already in use" o "Port 5000 already in use"

**Solución:**
1. Cierra otras aplicaciones que usen el puerto 5000
2. O cambia el puerto en `backend/app.py`:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)  # Cambia a puerto 5001
   ```
   Luego accede a `http://localhost:5001`

### Error: "No such file or directory: 'proyectos.db'"

**Solución:**
Ejecuta el script de inicialización:
```powershell
python backend/init_db.py
```

### Error: "Cannot activate virtual environment"

**Windows PowerShell:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

### No puedo iniciar sesión

**Solución:**
1. Verifica que la base de datos esté inicializada
2. Verifica las credenciales:
   - Email: `admin@proyectos.com`
   - Contraseña: `admin123`
3. Revisa la consola del servidor para errores

### Los gráficos no aparecen en Reportes

**Solución:**
- Verifica que tengas conexión a internet (Chart.js se carga desde CDN)
- Abre las herramientas de desarrollador (F12) y verifica errores en la consola

### Error de CORS

**Solución:**
El proyecto ya tiene Flask-CORS configurado. Si hay problemas:
1. Verifica que estés usando `credentials: 'include'` en las peticiones fetch
2. Verifica que Flask-CORS esté instalado: `pip install Flask-CORS`

---

## 📝 Comandos Rápidos de Referencia

```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Inicializar base de datos
python backend/init_db.py

# Ejecutar aplicación
python backend/app.py
```

---

## 🔐 Credenciales por Defecto

| Rol | Email | Contraseña |
|-----|-------|------------|
| Administrador | admin@proyectos.com | admin123 |

**⚠️ Cambia estas credenciales en producción.**

---

## 🌐 URLs Importantes

| URL | Descripción |
|-----|-------------|
| http://localhost:5000 | Página principal |
| http://localhost:5000/login.html | Página de login |
| http://localhost:5000/dashboard.html | Dashboard (requiere autenticación) |
| http://localhost:5000/proyectos.html | Gestión de proyectos |
| http://localhost:5000/kanban.html | Tablero Kanban |
| http://localhost:5000/reportes.html | Reportes y métricas |
| http://localhost:5000/api/* | Endpoints de la API REST |

---

## 🛠️ Tecnologías Utilizadas

### Backend
- **Python 3.8+**
- **Flask 3.0.0** - Framework web
- **SQLite** - Base de datos
- **bcrypt** - Encriptación de contraseñas
- **Flask-CORS** - Soporte CORS

### Frontend
- **HTML5** - Estructura
- **CSS3** - Estilos (Grid, Flexbox)
- **JavaScript ES6+** - Lógica del cliente
- **Chart.js** (CDN) - Gráficos en reportes

---

## 📦 Dependencias Externas

El proyecto usa las siguientes dependencias desde CDN:

- **Chart.js**: Para gráficos en la página de reportes
  - Se carga desde: `https://cdn.jsdelivr.net/npm/chart.js`
  - Requiere conexión a internet

---

## 🔄 Modo de Desarrollo

El servidor se ejecuta en **modo debug** por defecto, lo que significa:

✅ Los cambios en el código se recargan automáticamente
✅ Se muestran mensajes de error detallados
✅ No es apropiado para producción

Para producción, considera:
1. Usar un servidor WSGI como Gunicorn
2. Cambiar `debug=False` en `app.py`
3. Usar una base de datos más robusta (PostgreSQL)
4. Configurar HTTPS
5. Cambiar la clave secreta en `app.py`

---

## 📚 Recursos Adicionales

- **README.md**: Documentación general del proyecto
- **INSTALACION.md**: Guía de instalación detallada
- **docs/**: Documentación técnica adicional

---

## ✅ Checklist de Instalación

Marca cada paso conforme lo completes:

- [ ] Python 3.8+ instalado
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Base de datos inicializada (`python backend/init_db.py`)
- [ ] Servidor ejecutándose (`python backend/app.py`)
- [ ] Acceso a http://localhost:5000 funciona
- [ ] Login exitoso con credenciales de administrador

---

## 🆘 Obtener Ayuda

Si encuentras problemas:

1. Revisa la sección "Solución de Problemas Comunes" arriba
2. Verifica la consola del servidor para mensajes de error
3. Revisa la consola del navegador (F12) para errores del frontend
4. Consulta la documentación en la carpeta `docs/`

---

**¡Listo! Ya deberías tener el proyecto corriendo localmente. 🎉**

