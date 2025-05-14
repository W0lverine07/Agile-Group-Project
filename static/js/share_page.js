// Track selections
let selectedItem = null;
let selectedUsers = [];

// === Load Data ===
document.addEventListener('DOMContentLoaded', () => {
  updateShareButton();
  loadUsers();
  loadActivities();
  loadSharedWithMe();
});

// === Switch Tabs ===
function switchTab(tabName) {
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
  document.getElementById(tabName).classList.add('active');
  [...document.querySelectorAll('.tab-button')].find(b => b.textContent.toLowerCase().includes(tabName)).classList.add('active');
}

// === Load Users ===
function loadUsers() {
  fetch('/api/users')
    .then(res => res.json())
    .then(users => {
      const userList = document.querySelector('.user-list');
      userList.innerHTML = '';
      users.forEach((user, index) => {
        const div = document.createElement('div');
        div.className = 'user-item';
        div.onclick = () => selectUser(user.username, div);
        div.innerHTML = `
          <span class="user-name">${user.username}</span>
          <span class="user-selected"></span>
        `;

        userList.appendChild(div);
      });
    });
}

// === Load Activities ===
function loadActivities() {
  fetch('/api/my_activities')
    .then(res => res.json())
    .then(activities => {
      const container = document.getElementById('activities').querySelector('.scroll-container');
      container.innerHTML = '';
      activities.forEach(activity => {
        const div = document.createElement('div');
        div.className = 'share-item';
        div.onclick = () => selectItem('activity', activity.id, div);
        div.innerHTML = `
          <div class="item-icon"><img src="https://cdn-icons-png.flaticon.com/512/384/384276.png" /></div>
          <div class="item-details">
            <h4>${activity.exercise_name}</h4>
            <p>${activity.duration} min • ${activity.calories} cal</p>
            <p class="item-date">${activity.date}</p>
          </div>
        `;
        container.appendChild(div);
      });
    });
}

// === Load Shared With Me ===
function loadSharedWithMe() {
  fetch('/api/shared_with_me')
    .then(res => res.json())
    .then(data => {
      const container = document.querySelector('.shared-items');
      container.innerHTML = '';
      data.forEach((item, index) => {
        const div = document.createElement('div');
        div.className = 'shared-item';
        div.innerHTML = `
          <div class="shared-header">
            <div class="shared-info">
              <h4>${item.shared_by} shared with you</h4>
              <p class="item-date">${item.share_date}</p>
            </div>
          </div>
          <div class="shared-content">
            <div class="shared-item-icon">
              <img src="https://cdn-icons-png.flaticon.com/512/3198/3198336.png">
            </div>
            <div class="shared-item-details">
              <h4>${item.content_type.toUpperCase()}</h4>
              <p>ID: ${item.content_id}</p>
              <p class="shared-message">${item.message || ''}</p>
            </div>
          </div>
        `;
        container.appendChild(div);
      });
    });
}

// === Selection Logic ===
function selectItem(type, id, el) {
  document.querySelectorAll('.share-item').forEach(i => i.classList.remove('selected'));
  el.classList.add('selected');
  selectedItem = { type, id };
  updateShareButton();
}

function selectUser(username, el) {
  if (selectedUsers.includes(username)) {
    selectedUsers = selectedUsers.filter(u => u !== username);
    el.classList.remove('selected');
    el.querySelector('.user-selected').textContent = '';
  } else {
    selectedUsers.push(username);
    el.classList.add('selected');
    el.querySelector('.user-selected').textContent = '✓';
  }
  updateShareButton();
}

function updateShareButton() {
  const btn = document.getElementById('share-now');
  if (selectedItem && selectedUsers.length > 0) {
    btn.disabled = false;
    btn.classList.add('active');
  } else {
    btn.disabled = true;
    btn.classList.remove('active');
  }
}

// === Share Now ===
function shareNow() {
  const message = document.getElementById('share-message').value;

  selectedUsers.forEach(username => {
    const formData = new FormData();
    formData.append('shared_with_id', username);
    formData.append('content_type', selectedItem.type);
    formData.append('content_id', selectedItem.id);
    formData.append('message', message);

    fetch('/api/share_data', {
      method: 'POST',
      body: formData
    }).then(res => res.json())
      .then(response => {
        if (response.success) {
          document.getElementById('success-notification').classList.add('show');
          setTimeout(() => {
            document.getElementById('success-notification').classList.remove('show');
            loadSharedWithMe();
          }, 3000);
        }
      });
  });

  // Clear all
  document.querySelectorAll('.share-item').forEach(i => i.classList.remove('selected'));
  document.querySelectorAll('.user-item').forEach(i => {
    i.classList.remove('selected');
    i.querySelector('.user-selected').textContent = '';
  });
  selectedItem = null;
  selectedUsers = [];
  document.getElementById('share-message').value = '';
  updateShareButton();
}

function closeNotification() {
  document.getElementById('success-notification').classList.remove('show');
}
