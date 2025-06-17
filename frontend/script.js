// script.js

let token = null;

function showPage(page) {
  const pages = ['login', 'signup', 'home'];
  pages.forEach(p => {
    const section = document.getElementById(`${p}-page`);
    if (section) {
      section.classList.add('hidden');
    }
  });

  const activePage = document.getElementById(`${page}-page`);
  if (activePage) {
    activePage.classList.remove('hidden');
  }
  console.log("Showing page:", page);

}

function signup(event) {
  event.preventDefault();
  const username = document.getElementById('signup-username').value;
  const password = document.getElementById('signup-password').value;

  fetch('http://127.0.0.1:8000/signup', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  })
  .then(res => res.json())
  .then(data => {
    alert('Signup successful! Please log in.');
    showPage('login');
  })
  .catch(err => alert('Signup failed'));
}

function login(event) {
  event.preventDefault();
  const username = document.getElementById('login-username').value;
  const password = document.getElementById('login-password').value;

  const formData = new URLSearchParams();
  formData.append('username', username);
  formData.append('password', password);

  fetch('http://127.0.0.1:8000/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    if (data.access_token) {
      token = data.access_token;
      document.getElementById('logoutBtn').classList.remove('hidden');
      showPage('home');
      fetchTasks();
    } else {
      alert('Login failed');
    }
  })
  .catch(() => alert('Login error'));
}

function logout() {
  token = null;
  document.getElementById('logoutBtn').classList.add('hidden');
  showPage('login');
}

function fetchTasks() {
  fetch('http://127.0.0.1:8000/tasks', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })
  .then(res => res.json())
  .then(tasks => {
    const tasksDiv = document.getElementById('tasks');
    tasksDiv.innerHTML = '';
    tasks.forEach(task => {
      const taskElement = document.createElement('div');
      taskElement.innerHTML = `
        <div style="margin-bottom: 10px; padding: 10px; border: 1px solid #ccc; border-radius: 8px;">
          <strong>${task.title}</strong><br>
          ${task.description || ''}
        </div>
      `;
      tasksDiv.appendChild(taskElement);
    });
  })
  .catch(() => alert('Failed to load tasks'));
}

function createTask() {
  const title = prompt('Enter task title:');
  const description = prompt('Enter description (optional):');
  if (!title) return alert('Title is required');

  fetch('http://127.0.0.1:8000/tasks', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ title, description })
  })
  .then(res => res.json())
  .then(task => {
    fetchTasks();
  })
  .catch(() => alert('Failed to create task'));
}
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById("signupBtn").addEventListener("click", () => showPage("signup"));
  document.getElementById("loginBtn").addEventListener("click", () => showPage("login"));
  document.getElementById("homeBtn").addEventListener("click", () => showPage("home"));
  document.getElementById("logoutBtn").addEventListener("click", logout);

  document.getElementById("signupForm").addEventListener("submit", signup);
  document.getElementById("loginForm").addEventListener("submit", login);
});
