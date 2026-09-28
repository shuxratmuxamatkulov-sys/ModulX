const API_BASE = 'http://127.0.0.1:8000/api';

// Elementlar
const loginSection = document.getElementById('login-section');
const dashboardSection = document.getElementById('dashboard-section');
const loginForm = document.getElementById('login-form');
const loginError = document.getElementById('login-error');
const logoutBtn = document.getElementById('logout-btn');
const userDisplay = document.getElementById('user-display');

const addYarnForm = document.getElementById('add-yarn-form');
const yarnTableBody = document.getElementById('yarn-table-body');
const refreshYarnsBtn = document.getElementById('refresh-yarns');

// Tizimga kirish holatini tekshirish
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');
    if (token) {
        showDashboard();
    } else {
        showLogin();
    }
});

// Login formasini yuborish
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    loginError.classList.add('hidden');

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const res = await fetch(`${API_BASE}/token/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        if (!res.ok) throw new Error('Login xato');

        const data = await res.json();
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);
        localStorage.setItem('username', username);

        showDashboard();
    } catch (err) {
        loginError.classList.remove('hidden');
    }
});

// Chiqish tugmasi
logoutBtn.addEventListener('click', () => {
    localStorage.clear();
    showLogin();
});

function showLogin() {
    loginSection.classList.remove('hidden');
    dashboardSection.classList.add('hidden');
}

function showDashboard() {
    loginSection.classList.add('hidden');
    dashboardSection.classList.remove('hidden');
    userDisplay.textContent = localStorage.getItem('username') || 'Foydalanuvchi';
    loadYarns();
}

// Ip ro'yxatini yuklash (GET)
async function loadYarns() {
    const token = localStorage.getItem('access_token');
    try {
        const res = await fetch(`${API_BASE}/yarns/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (res.status === 401) {
            localStorage.clear();
            showLogin();
            return;
        }

        const yarns = await res.json();
        yarnTableBody.innerHTML = '';

        yarns.forEach(yarn => {
            const tr = document.createElement('tr');
            tr.className = 'hover:bg-slate-50 border-b';
            tr.innerHTML = `
                <td class="p-3 font-semibold text-slate-500">#${yarn.id}</td>
                <td class="p-3 font-medium text-slate-800">${yarn.name}</td>
                <td class="p-3">${yarn.title_num}</td>
                <td class="p-3 font-bold text-blue-600">${yarn.quantity_kg} kg</td>
                <td class="p-3 text-slate-500">${yarn.supplier}</td>
            `;
            yarnTableBody.appendChild(tr);
        });
    } catch (err) {
        console.error('Yarns yuklashda xatolik:', err);
    }
}

// Yangi ip qo'shish (POST)
addYarnForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('access_token');

    const payload = {
        name: document.getElementById('yarn-name').value,
        title_num: document.getElementById('yarn-title').value,
        quantity_kg: parseFloat(document.getElementById('yarn-qty').value),
        supplier: document.getElementById('yarn-supplier').value
    };

    try {
        const res = await fetch(`${API_BASE}/yarns/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (res.ok) {
            addYarnForm.reset();
            loadYarns();
        } else {
            alert("Ip qo'shishda xatolik yuz berdi!");
        }
    } catch (err) {
        console.error("Xatolik:", err);
    }
});

refreshYarnsBtn.addEventListener('click', loadYarns);