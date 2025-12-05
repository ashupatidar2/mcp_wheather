// ===== Authentication JavaScript =====
// Handles login, signup, logout, and token management

const API_BASE_URL = 'http://localhost:8000/api';

// ===== Utility Functions =====

function showError(elementId, message) {
    const errorEl = document.getElementById(elementId);
    if (errorEl) {
        errorEl.textContent = message;
        errorEl.style.display = 'block';
        setTimeout(() => {
            errorEl.style.display = 'none';
        }, 5000);
    }
}

function showSuccess(elementId, message) {
    const successEl = document.getElementById(elementId);
    if (successEl) {
        successEl.textContent = message;
        successEl.style.display = 'block';
        setTimeout(() => {
            successEl.style.display = 'none';
        }, 5000);
    }
}

function saveToken(token, email) {
    localStorage.setItem('access_token', token);
    localStorage.setItem('user_email', email);
}

function getToken() {
    return localStorage.setItem('access_token');
}

function removeToken() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_email');
}

function isAuthenticated() {
    return localStorage.getItem('access_token') !== null;
}

// ===== Signup Function =====

async function handleSignup(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const signupBtn = document.getElementById('signupBtn');

    // Validate passwords match
    if (password !== confirmPassword) {
        showError('errorMessage', 'Passwords do not match!');
        return;
    }

    // Validate password length
    if (password.length < 6) {
        showError('errorMessage', 'Password must be at least 6 characters!');
        return;
    }

    try {
        signupBtn.disabled = true;
        signupBtn.textContent = 'Creating Account...';

        const response = await fetch(`${API_BASE_URL}/auth/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Signup failed');
        }

        // Show success message
        showSuccess('successMessage', data.message);

        // Redirect to login after 2 seconds
        setTimeout(() => {
            window.location.href = '/login.html';
        }, 2000);

    } catch (error) {
        showError('errorMessage', error.message);
        signupBtn.disabled = false;
        signupBtn.textContent = 'Create Account';
    }
}

// ===== Login Function =====

async function handleLogin(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const loginBtn = document.getElementById('loginBtn');

    try {
        loginBtn.disabled = true;
        loginBtn.textContent = 'Logging in...';

        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Login failed');
        }

        // Save token to localStorage
        saveToken(data.access_token, data.email);

        // Show success message
        showSuccess('successMessage', data.message);

        // Redirect to weather app
        setTimeout(() => {
            window.location.href = '/index.html';
        }, 1000);

    } catch (error) {
        showError('errorMessage', error.message);
        loginBtn.disabled = false;
        loginBtn.textContent = 'Login';
    }
}

// ===== Logout Function =====

function logout() {
    removeToken();
    window.location.href = '/login.html';
}

// ===== Check Authentication =====

function checkAuth() {
    // Get current page
    const currentPage = window.location.pathname;

    // Pages that don't require authentication
    const publicPages = ['/login.html', '/signup.html', '/'];

    // If not authenticated and not on public page, redirect to login
    if (!isAuthenticated() && !publicPages.includes(currentPage)) {
        window.location.href = '/login.html';
    }

    // If authenticated and on login/signup page, redirect to app
    if (isAuthenticated() && (currentPage === '/login.html' || currentPage === '/signup.html')) {
        window.location.href = '/index.html';
    }
}

// ===== API Helper with Token =====

async function apiCall(endpoint, options = {}) {
    const token = localStorage.getItem('access_token');

    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers
    });

    // If unauthorized, redirect to login
    if (response.status === 401) {
        removeToken();
        window.location.href = '/login.html';
        throw new Error('Session expired. Please login again.');
    }

    return response;
}

// ===== Event Listeners =====

// Signup form
const signupForm = document.getElementById('signupForm');
if (signupForm) {
    signupForm.addEventListener('submit', handleSignup);
}

// Login form
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', handleLogin);
}

// Check authentication on page load
document.addEventListener('DOMContentLoaded', checkAuth);

// Export functions for use in other files
window.authUtils = {
    isAuthenticated,
    logout,
    apiCall,
    getToken,
    saveToken,
    removeToken
};

console.log('✅ Authentication module loaded!');
