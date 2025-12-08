// ===== API Configuration =====
// Automatically detects if running locally or on production (Render)

function getAPIBaseURL() {
    // Check if we're on localhost
    const isLocalhost = window.location.hostname === 'localhost' ||
        window.location.hostname === '127.0.0.1';

    if (isLocalhost) {
        // Local development - backend on port 8000
        return 'http://localhost:8000/api';
    } else {
        // Production - same domain as frontend (Render serves both)
        return window.location.origin + '/api';
    }
}

// Export the API base URL
const API_BASE_URL = getAPIBaseURL();

console.log('🌐 API Base URL:', API_BASE_URL);
