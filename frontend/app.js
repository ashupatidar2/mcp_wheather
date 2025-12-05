// ===== API Configuration =====
const API_BASE_URL = 'http://localhost:8000/api';

// ===== Get JWT Token =====
function getAuthToken() {
    return localStorage.getItem('access_token');
}

// ===== API Call with Token =====
async function apiCallWithAuth(url, options = {}) {
    const token = getAuthToken();

    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(url, {
        ...options,
        headers
    });

    // If unauthorized, redirect to login
    if (response.status === 401) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_email');
        window.location.href = '/login.html';
        throw new Error('Session expired. Please login again.');
    }

    return response;
}

// ===== DOM Elements =====
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const themeBtn = document.getElementById('themeBtn');
const loading = document.getElementById('loading');
const error = document.getElementById('error');
const errorMessage = document.getElementById('errorMessage');
const currentWeather = document.getElementById('features');
const forecastSection = document.getElementById('forecast');
const historySection = document.getElementById('history');
const saveBtn = document.getElementById('saveBtn');
const refreshBtn = document.getElementById('refreshBtn');
const dayModal = document.getElementById('dayModal');
const modalClose = document.getElementById('modalClose');
const modalBody = document.getElementById('modalBody');

// Weather display elements
const locationName = document.getElementById('locationName');
const locationCountry = document.getElementById('locationCountry');
const weatherIcon = document.getElementById('weatherIcon');
const weatherDesc = document.getElementById('weatherDesc');
const temperature = document.getElementById('temperature');
const feelsLike = document.getElementById('feelsLike');
const humidity = document.getElementById('humidity');
const windSpeed = document.getElementById('windSpeed');
const pressure = document.getElementById('pressure');

// Forecast elements
const hourlyForecast = document.getElementById('hourlyForecast');
const dailyForecast = document.getElementById('dailyForecast');
const historyGrid = document.getElementById('historyGrid');
const historyLoading = document.getElementById('historyLoading');
const noHistory = document.getElementById('noHistory');

// State
let currentWeatherData = null;
let currentCity = null;

// ===== Theme Management =====
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
}

themeBtn.addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
});

// ===== Utility Functions =====
function show(element) {
    element.classList.remove('hidden');
}

function hide(element) {
    element.classList.add('hidden');
}

function showLoading() {
    show(loading);
    hide(error);
    hide(currentWeather);
    hide(forecastSection);
}

function hideLoading() {
    hide(loading);
}

function showError(message) {
    errorMessage.textContent = message;
    show(error);
    hide(currentWeather);
    hide(forecastSection);
    hideLoading();
}

// ===== Weather Functions =====
async function searchWeather() {
    const city = searchInput.value.trim();
    if (!city) {
        showError('Please enter a location name');
        return;
    }

    try {
        showLoading();
        currentCity = city;

        // Fetch current weather
        const response = await apiCallWithAuth(`${API_BASE_URL}/weather/${encodeURIComponent(city)}`);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || 'Failed to fetch weather');
        }

        if (result.success && result.data) {
            currentWeatherData = result.data;
            displayCurrentWeather(result.data);

            // Load forecasts
            loadHourlyForecast(city);
            loadDailyForecast(city);
        } else {
            throw new Error('Invalid response from server');
        }

    } catch (err) {
        showError(err.message);
    } finally {
        hideLoading();
    }
}

function displayCurrentWeather(data) {
    locationName.textContent = data.city;
    locationCountry.textContent = data.country;

    const iconUrl = `https://openweathermap.org/img/wn/${data.icon}@4x.png`;
    weatherIcon.src = iconUrl;
    weatherIcon.alt = data.description;

    weatherDesc.textContent = data.description;
    temperature.textContent = Math.round(data.temperature);
    feelsLike.textContent = Math.round(data.feels_like);
    humidity.textContent = `${data.humidity}%`;
    windSpeed.textContent = `${data.wind_speed} m/s`;
    pressure.textContent = `${Math.round(data.pressure)} hPa`;

    show(currentWeather);
}

// ===== Hourly Forecast =====
async function loadHourlyForecast(city) {
    try {
        const response = await apiCallWithAuth(`${API_BASE_URL}/forecast/hourly/${encodeURIComponent(city)}`);
        const result = await response.json();

        if (result.success && result.data) {
            displayHourlyForecast(result.data);
            show(forecastSection);
        }
    } catch (err) {
        console.error('Hourly forecast error:', err);
    }
}

function displayHourlyForecast(data) {
    hourlyForecast.innerHTML = '';

    data.slice(0, 24).forEach(hour => {
        const card = document.createElement('div');
        card.className = 'hourly-card';

        const iconUrl = `https://openweathermap.org/img/wn/${hour.icon}@2x.png`;

        card.innerHTML = `
            <div class="hourly-time">${hour.time}</div>
            <img src="${iconUrl}" alt="${hour.description}" class="hourly-icon">
            <div class="hourly-temp">${Math.round(hour.temp)}°</div>
            <div class="hourly-desc">${hour.description}</div>
            <div class="hourly-desc">💧 ${hour.pop}%</div>
        `;

        hourlyForecast.appendChild(card);
    });
}

// ===== Daily Forecast =====
async function loadDailyForecast(city) {
    try {
        const response = await apiCallWithAuth(`${API_BASE_URL}/forecast/daily/${encodeURIComponent(city)}`);
        const result = await response.json();

        if (result.success && result.data) {
            displayDailyForecast(result.data);
        }
    } catch (err) {
        console.error('Daily forecast error:', err);
    }
}

function displayDailyForecast(data) {
    dailyForecast.innerHTML = '';

    data.forEach(day => {
        const card = document.createElement('div');
        card.className = 'daily-card';

        const iconUrl = `https://openweathermap.org/img/wn/${day.icon}@2x.png`;

        card.innerHTML = `
            <div class="daily-date">${day.date}</div>
            <div class="daily-content">
                <img src="${iconUrl}" alt="${day.description}" class="daily-icon">
                <div class="daily-temps">
                    <div class="daily-temp-high">${Math.round(day.temp_max)}°</div>
                    <div class="daily-temp-low">${Math.round(day.temp_min)}°</div>
                </div>
            </div>
            <div class="daily-desc">${day.description}</div>
            <div class="daily-stats">
                <span>💧 ${day.pop}%</span>
                <span>💨 ${day.wind_speed} m/s</span>
            </div>
        `;

        // Make card clickable for details
        card.addEventListener('click', () => showDayModal(day));

        dailyForecast.appendChild(card);
    });
}

// ===== Day Detail Modal =====
function showDayModal(day) {
    const iconUrl = `https://openweathermap.org/img/wn/${day.icon}@4x.png`;

    modalBody.innerHTML = `
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="font-size: 2rem; margin-bottom: 0.5rem;">${day.date}</h2>
            <p style="color: var(--text-muted);">${currentCity}</p>
        </div>
        
        <div style="display: flex; align-items: center; justify-content: center; gap: 2rem; margin-bottom: 2rem;">
            <img src="${iconUrl}" alt="${day.description}" style="width: 120px; height: 120px;">
            <div style="text-align: center;">
                <div style="font-size: 4rem; font-weight: 800; background: var(--gradient-primary); -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1;">${Math.round(day.temp_max)}°</div>
                <div style="font-size: 1.25rem; color: var(--text-secondary); margin-top: 0.5rem;">${day.description}</div>
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
            <div style="background: var(--bg-secondary); padding: 1.5rem; border-radius: 12px; text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🌡️</div>
                <div style="color: var(--text-muted); font-size: 0.875rem; margin-bottom: 0.25rem;">High</div>
                <div style="font-size: 1.5rem; font-weight: 600;">${Math.round(day.temp_max)}°C</div>
            </div>
            <div style="background: var(--bg-secondary); padding: 1.5rem; border-radius: 12px; text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">❄️</div>
                <div style="color: var(--text-muted); font-size: 0.875rem; margin-bottom: 0.25rem;">Low</div>
                <div style="font-size: 1.5rem; font-weight: 600;">${Math.round(day.temp_min)}°C</div>
            </div>
            <div style="background: var(--bg-secondary); padding: 1.5rem; border-radius: 12px; text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🌧️</div>
                <div style="color: var(--text-muted); font-size: 0.875rem; margin-bottom: 0.25rem;">Rain Chance</div>
                <div style="font-size: 1.5rem; font-weight: 600;">${day.pop}%</div>
            </div>
            <div style="background: var(--bg-secondary); padding: 1.5rem; border-radius: 12px; text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">💨</div>
                <div style="color: var(--text-muted); font-size: 0.875rem; margin-bottom: 0.25rem;">Wind Speed</div>
                <div style="font-size: 1.5rem; font-weight: 600;">${day.wind_speed} m/s</div>
            </div>
        </div>
    `;

    show(dayModal);
}

function closeDayModal() {
    hide(dayModal);
}

// ===== Save to Sheets =====
async function saveToSheets() {
    if (!currentWeatherData) {
        showError('No weather data to save');
        return;
    }

    try {
        saveBtn.disabled = true;
        saveBtn.innerHTML = '<span class="btn-icon">⏳</span><span class="btn-text">Saving...</span>';

        const response = await apiCallWithAuth(`${API_BASE_URL}/weather/save`, {
            method: 'POST',
            body: JSON.stringify(currentWeatherData)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || 'Failed to save');
        }

        saveBtn.innerHTML = '<span class="btn-icon">✅</span><span class="btn-text">Saved!</span>';

        setTimeout(() => {
            saveBtn.innerHTML = '<span class="btn-icon">💾</span><span class="btn-text">Save to Sheets</span>';
            saveBtn.disabled = false;
        }, 2000);

        // Refresh history
        loadHistory();

    } catch (err) {
        showError(err.message);
        saveBtn.innerHTML = '<span class="btn-icon">💾</span><span class="btn-text">Save to Sheets</span>';
        saveBtn.disabled = false;
    }
}

// ===== History =====
async function loadHistory() {
    try {
        show(historyLoading);
        hide(historyGrid);
        hide(noHistory);

        const response = await apiCallWithAuth(`${API_BASE_URL}/weather/history?limit=5`);
        const result = await response.json();

        if (result.success && result.data && result.data.length > 0) {
            displayHistory(result.data);
        } else {
            show(noHistory);
        }

    } catch (err) {
        console.error('History error:', err);
        show(noHistory);
    } finally {
        hide(historyLoading);
    }
}

function displayHistory(data) {
    historyGrid.innerHTML = '';

    data.forEach(record => {
        const card = document.createElement('div');
        card.className = 'history-card';

        const city = record.City || 'Unknown';
        const country = record.Country || '';
        const temp = record['Temperature (°C)'] || 'N/A';
        const timestamp = record.Timestamp || '';

        const time = timestamp ? new Date(timestamp).toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit'
        }) : '';

        card.innerHTML = `
            <div class="history-header">
                <div class="history-city">${city}</div>
                <div class="history-country">${country}</div>
            </div>
            <div class="history-temp">${temp}°C</div>
            <div class="history-time">${time}</div>
        `;

        // Click to search again
        card.addEventListener('click', () => {
            searchInput.value = city;
            searchWeather();
        });

        historyGrid.appendChild(card);
    });

    show(historyGrid);
}

// ===== Tab Switching =====
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.getAttribute('data-tab');

        // Remove active class from all
        tabBtns.forEach(b => b.classList.remove('active'));
        tabContents.forEach(c => c.classList.remove('active'));

        // Add active to clicked
        btn.classList.add('active');
        document.getElementById(`${tabName}Tab`).classList.add('active');
    });
});

// ===== Event Listeners =====
searchBtn.addEventListener('click', searchWeather);
searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') searchWeather();
});
saveBtn.addEventListener('click', saveToSheets);
refreshBtn.addEventListener('click', loadHistory);
modalClose.addEventListener('click', closeDayModal);
dayModal.addEventListener('click', (e) => {
    if (e.target === dayModal) closeDayModal();
});

// ===== Initialize =====
initTheme();
loadHistory();

console.log('✅ Weather Pro initialized with Open-Meteo API!');

// ===== Navbar Scroll Effect Only =====
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(15, 23, 42, 0.95)';
        } else {
            navbar.style.background = 'var(--bg-glass)';
        }
    }
});

// Mobile Menu Toggle
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const navMenu = document.getElementById('navMenu');

if (mobileMenuBtn && navMenu) {
    mobileMenuBtn.addEventListener('click', () => {
        navMenu.classList.toggle('active');
    });
}

console.log('✅ Navbar ready - links will navigate to pages!');

// ===== Authentication Check =====
// Check if user is authenticated, redirect to login if not
function checkAuthentication() {
    const token = getAuthToken();
    if (!token) {
        window.location.href = '/login.html';
    }
}

// Run auth check on page load
checkAuthentication();

// ===== Logout Functionality =====
// Add logout button if it exists
const logoutBtn = document.getElementById('logoutBtn');
if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_email');
        window.location.href = '/login.html';
    });
}

console.log('✅ Authentication check complete!');

