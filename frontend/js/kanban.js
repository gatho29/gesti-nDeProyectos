/**
 * Funcionalidad específica del tablero Kanban
 */

/**
 * Inicializa el drag and drop para el tablero Kanban
 */
function initKanbanDragDrop() {
    const tareas = document.querySelectorAll('.tarea-kanban');
    const columnas = document.querySelectorAll('.kanban-column');
    
    tareas.forEach(tarea => {
        tarea.addEventListener('dragstart', (e) => {
            e.dataTransfer.setData('text/plain', tarea.dataset.tareaId);
            tarea.classList.add('dragging');
        });
        
        tarea.addEventListener('dragend', (e) => {
            tarea.classList.remove('dragging');
        });
    });
    
    columnas.forEach(columna => {
        columna.addEventListener('dragover', (e) => {
            e.preventDefault();
            columna.classList.add('drag-over');
        });
        
        columna.addEventListener('dragleave', (e) => {
            columna.classList.remove('drag-over');
        });
        
        columna.addEventListener('drop', async (e) => {
            e.preventDefault();
            columna.classList.remove('drag-over');
            
            const tareaId = parseInt(e.dataTransfer.getData('text/plain'));
            const nuevoEstado = columna.dataset.estado;
            
            await actualizarEstadoTarea(tareaId, nuevoEstado);
        });
    });
}

/**
 * Actualiza el estado de una tarea
 */
async function actualizarEstadoTarea(tareaId, nuevoEstado) {
    try {
        const response = await fetch(`/api/tareas/${tareaId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({ estado: nuevoEstado })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Error al actualizar tarea');
        }
        
        // Recargar las tareas
        if (typeof loadTareas === 'function') {
            loadTareas();
        } else {
            location.reload();
        }
    } catch (error) {
        console.error('Error actualizando tarea:', error);
        alert('Error al actualizar la tarea: ' + error.message);
    }
}

