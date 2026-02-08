// Configuration
const API_URL = window.ENV?.API_URL || '/api';
const ENVIRONMENT = window.ENV?.ENVIRONMENT || 'production';
const VERSION = window.ENV?.VERSION || 'unknown';

// State
let currentUser = null;
let currentBoardId = null;

// DOM Elements
const authSection = document.getElementById('auth-section');
const appSection = document.getElementById('app-section');
const loading = document.getElementById('loading');

// Auth Forms
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const showLoginBtn = document.getElementById('show-login');
const showRegisterBtn = document.getElementById('show-register');

// App Elements
const usernameDisplay = document.getElementById('username-display');
const logoutBtn = document.getElementById('logout-btn');
const createBoardForm = document.getElementById('create-board-form');
const boardsContainer = document.getElementById('boards-container');

// Modal Elements
const boardModal = document.getElementById('board-modal');
const closeModalBtn = document.getElementById('close-modal');
const modalBoardName = document.getElementById('modal-board-name');
const uploadForm = document.getElementById('upload-form');
const imagesContainer = document.getElementById('images-container');
const deleteBoardBtn = document.getElementById('delete-board-btn');

// Utility Functions
function showLoading() {
    loading.classList.remove('hidden');
}

function hideLoading() {
    loading.classList.add('hidden');
}

function showError(elementId, message) {
    const errorEl = document.getElementById(elementId);
    errorEl.textContent = message;
    errorEl.classList.remove('hidden');
    setTimeout(() => {
        errorEl.classList.add('hidden');
    }, 5000);
}

function getToken() {
    return localStorage.getItem('token');
}

function setToken(token) {
    localStorage.setItem('token', token);
}

function clearToken() {
    localStorage.removeItem('token');
}

async function apiCall(endpoint, options = {}) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers,
    });

    if (response.status === 401) {
        clearToken();
        showAuthSection();
        throw new Error('Session expired. Please login again.');
    }

    if (!response.ok) {
        try {
            const error = await response.json();
            throw new Error(error.detail || 'Request failed');
        } catch (e) {
            throw new Error(`Request failed with status ${response.status}`);
        }
    }

    // Handle 204 No Content (DELETE operations)
    if (response.status === 204) {
        return null;
    }

    // Only parse JSON if content-type is JSON
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
        return response.json();
    }

    // No JSON content
    return null;
}

// Auth Functions
async function register(username, email, password) {
    showLoading();
    try {
        const data = await apiCall('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ username, email, password }),
        });

        // Auto-login: registration returns token
        setToken(data.access_token);
        currentUser = data.user;
        showAppSection();
    } catch (error) {
        showError('register-error', error.message);
    } finally {
        hideLoading();
    }
}

async function login(username, password) {
    showLoading();
    try {
        const data = await apiCall('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ username, password }),
        });

        setToken(data.access_token);
        
        // Get user info
        currentUser = await apiCall('/auth/me');
        
        showAppSection();
    } catch (error) {
        showError('login-error', error.message);
    } finally {
        hideLoading();
    }
}

function logout() {
    clearToken();
    currentUser = null;
    showAuthSection();
}

// Board Functions
async function loadBoards() {
    try {
        const boards = await apiCall('/boards/');
        displayBoards(boards);
    } catch (error) {
        boardsContainer.innerHTML = `<p class="loading-text">Failed to load boards: ${error.message}</p>`;
    }
}

function displayBoards(boards) {
    if (boards.length === 0) {
        boardsContainer.innerHTML = '<p class="loading-text">No vision boards yet. Create your first one!</p>';
        return;
    }

    boardsContainer.innerHTML = boards.map(board => `
        <div class="board-card" onclick="openBoard(${board.id})">
            <h3>${escapeHtml(board.name)}</h3>
            <p>${escapeHtml(board.description || 'No description')}</p>
            <div class="board-meta">
                <span>${new Date(board.created_at).toLocaleDateString()}</span>
                <span class="image-count">${board.image_count} images</span>
            </div>
        </div>
    `).join('');
}

async function createBoard(name, description) {
    showLoading();
    try {
        await apiCall('/boards/', {
            method: 'POST',
            body: JSON.stringify({ name, description }),
        });

        // Reload boards
        await loadBoards();

        // Clear form
        document.getElementById('board-name').value = '';
        document.getElementById('board-description').value = '';
    } catch (error) {
        alert('Failed to create board: ' + error.message);
    } finally {
        hideLoading();
    }
}

async function openBoard(boardId) {
    currentBoardId = boardId;
    showLoading();
    
    try {
        const board = await apiCall(`/boards/${boardId}`);
        
        modalBoardName.textContent = board.name;
        displayImages(board.images);
        boardModal.classList.remove('hidden');
    } catch (error) {
        alert('Failed to load board: ' + error.message);
    } finally {
        hideLoading();
    }
}

function closeBoard() {
    boardModal.classList.add('hidden');
    currentBoardId = null;
}

async function deleteBoard() {
    if (!confirm('Are you sure you want to delete this board? All images will be permanently deleted.')) {
        return;
    }

    showLoading();
    try {
        await apiCall(`/boards/${currentBoardId}`, {
            method: 'DELETE',
        });

        closeBoard();
        await loadBoards();
    } catch (error) {
        alert('Failed to delete board: ' + error.message);
    } finally {
        hideLoading();
    }
}

// Image Functions
function displayImages(images) {
    if (images.length === 0) {
        imagesContainer.innerHTML = '<p class="no-images">No images yet. Upload your first vision image!</p>';
        return;
    }

    imagesContainer.innerHTML = images.map(image => `
        <div class="image-card">
            <img src="${image.image_url}" alt="Vision image" loading="lazy">
            <button class="image-delete-btn" onclick="deleteImage(${image.id})">×</button>
        </div>
    `).join('');
}

async function uploadImage(file) {
    showLoading();
    try {
        const formData = new FormData();
        formData.append('file', file);

        const token = getToken();
        const response = await fetch(`${API_URL}/boards/${currentBoardId}/images`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
            },
            body: formData,
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Upload failed');
        }

        // Reload board
        await openBoard(currentBoardId);

        // Clear file input
        document.getElementById('image-file').value = '';
    } catch (error) {
        alert('Failed to upload image: ' + error.message);
    } finally {
        hideLoading();
    }
}

async function deleteImage(imageId) {
    if (!confirm('Delete this image?')) {
        return;
    }

    showLoading();
    try {
        await apiCall(`/boards/${currentBoardId}/images/${imageId}`, {
            method: 'DELETE',
        });

        // Reload board
        await openBoard(currentBoardId);
    } catch (error) {
        alert('Failed to delete image: ' + error.message);
    } finally {
        hideLoading();
    }
}

// UI Functions
function showAuthSection() {
    authSection.classList.remove('hidden');
    appSection.classList.add('hidden');
}

function showAppSection() {
    authSection.classList.add('hidden');
    appSection.classList.remove('hidden');
    
    usernameDisplay.textContent = currentUser.username;
    loadBoards();
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Event Listeners
showLoginBtn.addEventListener('click', () => {
    loginForm.classList.remove('hidden');
    registerForm.classList.add('hidden');
    showLoginBtn.classList.add('active');
    showRegisterBtn.classList.remove('active');
});

showRegisterBtn.addEventListener('click', () => {
    registerForm.classList.remove('hidden');
    loginForm.classList.add('hidden');
    showRegisterBtn.classList.add('active');
    showLoginBtn.classList.remove('active');
});

loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    login(username, password);
});

registerForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    register(username, email, password);
});

logoutBtn.addEventListener('click', logout);

createBoardForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = document.getElementById('board-name').value;
    const description = document.getElementById('board-description').value;
    createBoard(name, description);
});

closeModalBtn.addEventListener('click', closeBoard);
boardModal.addEventListener('click', (e) => {
    if (e.target === boardModal) {
        closeBoard();
    }
});

uploadForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const file = document.getElementById('image-file').files[0];
    if (file) {
        uploadImage(file);
    }
});

deleteBoardBtn.addEventListener('click', deleteBoard);

// Initialize
(async function init() {
    const token = getToken();
    
    if (token) {
        // Try to auto-login with existing token
        showLoading();
        try {
            currentUser = await apiCall('/auth/me');
            showAppSection();
        } catch (error) {
            // Token invalid, show login
            clearToken();
            showAuthSection();
        } finally {
            hideLoading();
        }
    } else {
        showAuthSection();
    }
})();