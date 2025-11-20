@echo off
REM Script para ejecutar el proyecto automáticamente
REM Script de comandos para Windows

echo ========================================
echo Sistema de Gestion de Proyectos
echo Script de Ejecucion Automatica
echo ========================================
echo.

REM Verificar Python
echo Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ERROR: Python no esta instalado o no esta en el PATH
        echo.
        echo Por favor instala Python 3.8 o superior desde:
        echo   https://www.python.org/downloads/
        echo.
        echo Durante la instalacion, asegurate de marcar:
        echo   [X] Add Python to PATH
        echo.
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=py
    )
) else (
    set PYTHON_CMD=python
)

echo Python encontrado
echo.

REM Verificar pip
echo Verificando pip...
%PYTHON_CMD% -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pip no esta disponible
    pause
    exit /b 1
)
echo pip encontrado
echo.

REM Crear entorno virtual si no existe
echo Verificando entorno virtual...
if not exist "venv" (
    echo Creando entorno virtual...
    %PYTHON_CMD% -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
    echo Entorno virtual creado
) else (
    echo Entorno virtual ya existe
)
echo.

REM Activar entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: No se pudo activar el entorno virtual
    pause
    exit /b 1
)
echo Entorno virtual activado
echo.

REM Instalar dependencias
echo Instalando dependencias...
python -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)
echo Dependencias instaladas
echo.

REM Inicializar base de datos
echo Inicializando base de datos...
python backend\init_db.py
if %errorlevel% neq 0 (
    echo ADVERTENCIA: Hubo un problema al inicializar la base de datos
    echo Intentando continuar...
)
echo.

REM Ejecutar aplicación
echo ========================================
echo Iniciando servidor...
echo ========================================
echo.
echo Servidor disponible en: http://localhost:5000
echo.
echo Credenciales del administrador:
echo   Email: admin@proyectos.com
echo   Contrasena: admin123
echo.
echo Presiona CTRL+C para detener el servidor
echo.
echo ========================================
echo.

REM Ejecutar la aplicación
python backend\app.py

