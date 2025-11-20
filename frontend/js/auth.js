/**
 * Módulo de autenticación
 */

/**
 * Verifica si el usuario está autenticado
 */
async function checkAuth() {
    try {
        const response = await fetch('/api/auth/me', {
            credentials: 'include'
        });
        
        if (!response.ok) {
            window.location.href = '/login.html';
            throw new Error('No autenticado');
        }
        
        return await response.json();
    } catch (error) {
        window.location.href = '/login.html';
        throw error;
    }
}

/**
 * Obtiene el usuario actual
 */
async function getCurrentUser() {
    try {
        const response = await fetch('/api/auth/me', {
            credentials: 'include'
        });
        
        if (!response.ok) {
            throw new Error('No autenticado');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error obteniendo usuario:', error);
        window.location.href = '/login.html';
        throw error;
    }
}

/**
 * Cierra la sesión del usuario
 */
async function logout() {
    try {
        await fetch('/api/auth/logout', {
            method: 'POST',
            credentials: 'include'
        });
    } catch (error) {
        console.error('Error al cerrar sesión:', error);
    }
}

