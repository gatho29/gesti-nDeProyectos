/**
 * Funciones de utilidad generales
 */

/**
 * Formatea una fecha para mostrar
 */
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

/**
 * Formatea una fecha corta
 */
function formatDateShort(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES');
}

/**
 * Obtiene el color según la prioridad
 */
function getPriorityColor(prioridad) {
    const colors = {
        'Baja': '#28a745',
        'Media': '#ffc107',
        'Alta': '#dc3545'
    };
    return colors[prioridad] || '#6c757d';
}

/**
 * Verifica si una tarea está retrasada
 */
function isTaskOverdue(tarea) {
    if (tarea.estado === 'Finalizado') return false;
    if (!tarea.fecha_limite) return false;
    
    const fechaLimite = new Date(tarea.fecha_limite);
    const hoy = new Date();
    hoy.setHours(0, 0, 0, 0);
    
    return fechaLimite < hoy;
}

/**
 * Muestra un mensaje de error
 */
function showError(message) {
    alert('Error: ' + message);
}

/**
 * Muestra un mensaje de éxito
 */
function showSuccess(message) {
    alert('Éxito: ' + message);
}

/**
 * Maneja errores de API
 */
async function handleApiError(response) {
    if (!response.ok) {
        const error = await response.json().catch(() => ({ error: 'Error desconocido' }));
        throw new Error(error.error || 'Error en la solicitud');
    }
    return response.json();
}

