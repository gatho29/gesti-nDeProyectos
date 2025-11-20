# Script para ejecutar el proyecto automáticamente
# PowerShell Script para Windows

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Sistema de Gestión de Proyectos" -ForegroundColor Cyan
Write-Host "Script de Ejecución Automática" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar Python
Write-Host "Verificando Python..." -ForegroundColor Yellow
$pythonCmd = $null

# Intentar diferentes comandos de Python
$pythonCommands = @("python", "py", "python3", "python.exe")
foreach ($cmd in $pythonCommands) {
    try {
        $version = & $cmd --version 2>&1
        if ($LASTEXITCODE -eq 0 -or $version -match "Python") {
            $pythonCmd = $cmd
            Write-Host "✓ Python encontrado: $version" -ForegroundColor Green
            break
        }
    } catch {
        continue
    }
}

if (-not $pythonCmd) {
    Write-Host "✗ ERROR: Python no está instalado o no está en el PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Por favor instala Python 3.8 o superior desde:" -ForegroundColor Yellow
    Write-Host "  https://www.python.org/downloads/" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Durante la instalación, asegúrate de marcar:" -ForegroundColor Yellow
    Write-Host "  ☑ Add Python to PATH" -ForegroundColor Cyan
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Verificar pip
Write-Host ""
Write-Host "Verificando pip..." -ForegroundColor Yellow
try {
    $pipVersion = & $pythonCmd -m pip --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ pip encontrado" -ForegroundColor Green
    } else {
        Write-Host "✗ ERROR: pip no está disponible" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "✗ ERROR: pip no está disponible" -ForegroundColor Red
    exit 1
}

# Crear entorno virtual si no existe
Write-Host ""
Write-Host "Verificando entorno virtual..." -ForegroundColor Yellow
if (-not (Test-Path "venv")) {
    Write-Host "Creando entorno virtual..." -ForegroundColor Yellow
    & $pythonCmd -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Entorno virtual creado" -ForegroundColor Green
    } else {
        Write-Host "✗ ERROR: No se pudo crear el entorno virtual" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✓ Entorno virtual ya existe" -ForegroundColor Green
}

# Activar entorno virtual
Write-Host ""
Write-Host "Activando entorno virtual..." -ForegroundColor Yellow
if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
    Write-Host "✓ Entorno virtual activado" -ForegroundColor Green
} else {
    Write-Host "✗ ERROR: No se encontró el script de activación" -ForegroundColor Red
    exit 1
}

# Instalar dependencias
Write-Host ""
Write-Host "Instalando dependencias..." -ForegroundColor Yellow
& $pythonCmd -m pip install -r requirements.txt --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencias instaladas" -ForegroundColor Green
} else {
    Write-Host "✗ ERROR: No se pudieron instalar las dependencias" -ForegroundColor Red
    exit 1
}

# Inicializar base de datos
Write-Host ""
Write-Host "Inicializando base de datos..." -ForegroundColor Yellow
& $pythonCmd backend\init_db.py
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Base de datos inicializada" -ForegroundColor Green
} else {
    Write-Host "⚠ ADVERTENCIA: Hubo un problema al inicializar la base de datos" -ForegroundColor Yellow
    Write-Host "  Intentando continuar..." -ForegroundColor Yellow
}

# Ejecutar aplicación
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Iniciando servidor..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Servidor disponible en: http://localhost:5000" -ForegroundColor Green
Write-Host ""
Write-Host "Credenciales del administrador:" -ForegroundColor Yellow
Write-Host "  Email: admin@proyectos.com" -ForegroundColor White
Write-Host "  Contraseña: admin123" -ForegroundColor White
Write-Host ""
Write-Host "Presiona CTRL+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Ejecutar la aplicación
& $pythonCmd backend\app.py

