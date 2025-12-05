const API_BASE_URL = 'http://localhost:8000/api';
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const loading = document.getElementById('loading');
const forecastSection = document.getElementById('forecastSection');
const dailyForecast = document.getElementById('dailyForecast');
const hourlyForecast = document.getElementById('hourlyForecast');
const themeBtn = document.getElementById('themeBtn');

// Theme
const savedTheme = localStorage.getItem('theme') || 'dark';
document.documentElement.setAttribute('data-theme', savedTheme);

themeBtn.addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
});

// Tab switching
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.getAttribute('data-tab');
        tabBtns.forEach(b => b.classList.remove('active'));
        tabContents.forEach(c => c.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById(`${tabName}Tab`).classList.add('active');
    });
});

// Search
async function searchForecast() {
    const city = searchInput.value.trim();
    if (!city) return;
    
    loading.classList.remove('hidden');
    forecastSection.classList.add('hidden');
    
    try {
        await Promise.all([loadDaily(city), loadHourly(city)]);
        forecastSection.classList.remove('hidden');
    } catch (err) {
        alert('Failed to load forecast: ' + err.message);
    } finally {
        loading.classList.add('hidden');
    }
}

async function loadDaily(city) {
    const response = await fetch(`${API_BASE_URL}/forecast/daily/${encodeURIComponent(city)}`);
    const result = await response.json();
    
    if (result.success && result.data) {
        displayDaily(result.data);
    }
}

async function loadHourly(city) {
    const response = await fetch(`${API_BASE_URL}/forecast/hourly/${encodeURIComponent(city)}`);
    const result = await response.json();
    
    if (result.success && result.data) {
        displayHourly(result.data);
    }
}

function displayDaily(data) {
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
        
        dailyForecast.appendChild(card);
    });
}

function displayHourly(data) {
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

searchBtn.addEventListener('click', searchForecast);
searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') searchForecast();
});
