# Sistema de Gestión de Proyectos

Sistema completo de gestión de proyectos que permite gestionar usuarios, crear proyectos y tareas, realizar seguimiento mediante tableros Kanban y generar reportes.

## Características Principales

- **Gestión de Usuarios**: Registro y autenticación con roles (Administrador, Gestor de Proyecto, Colaborador)
- **Gestión de Proyectos**: Creación de proyectos con responsables y fechas de entrega
- **Gestión de Tareas**: Asignación de tareas con estados y seguimiento
- **Tablero Kanban**: Visualización de tareas por estados (Pendiente, En progreso, Finalizado)
- **Reportes**: Generación de reportes de desempeño y métricas

## Estructura del Proyecto

```
proyecto-gestion/
├── backend/
│   ├── app.py                 # Aplicación Flask principal
│   ├── models.py              # Modelos de base de datos
│   ├── auth.py                # Autenticación y autorización
│   ├── routes.py              # Rutas de la API
│   ├── database.py            # Configuración de base de datos
│   └── init_db.py             # Inicialización de base de datos
├── frontend/
│   ├── index.html             # Página principal
│   ├── login.html             # Página de login
│   ├── dashboard.html         # Dashboard principal
│   ├── proyectos.html         # Gestión de proyectos
│   ├── kanban.html            # Tablero Kanban
│   ├── reportes.html          # Página de reportes
│   ├── css/
│   │   └── styles.css         # Estilos principales
│   └── js/
│       ├── app.js             # Lógica principal
│       ├── auth.js            # Manejo de autenticación
│       └── kanban.js          # Funcionalidad Kanban
├── docs/
│   ├── analisis-requisitos.md # Documento de análisis de requisitos
│   ├── diseño-sistema.md      # Documentación de diseño
│   └── informe-final.md       # Informe final del proyecto
└── requirements.txt           # Dependencias de Python
```

## Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Inicializar base de datos:
```bash
cd backend
python init_db.py
```

3. Ejecutar aplicación:
```bash
python backend/app.py
```

4. Abrir navegador en: `http://localhost:5000`

## Uso

- **Administradores**: Pueden gestionar usuarios, proyectos y ver todos los reportes
- **Gestores de Proyecto**: Pueden crear proyectos, asignar tareas y ver reportes de sus proyectos
- **Colaboradores**: Pueden ver sus tareas asignadas y actualizar su estado en el tablero Kanban

## Tecnologías Utilizadas

- Backend: Python/Flask
- Frontend: HTML5, CSS3, JavaScript (Vanilla)
- Base de datos: SQLite
- Diseño: CSS Grid, Flexbox, responsive design

## Créditos

Trabajo Final - Módulo de Gestión de Proyectos

