    // Function to switch tabs
    function switchTab(tabName) {
      // Hide all tab contents
      const tabContents = document.getElementsByClassName('tab-content');
      for (let i = 0; i < tabContents.length; i++) {
        tabContents[i].classList.remove('active');
      }
      
      // Remove active class from all tab buttons
      const tabButtons = document.getElementsByClassName('tab-button');
      for (let i = 0; i < tabButtons.length; i++) {
        tabButtons[i].classList.remove('active');
      }
      
      // Show selected tab content and make button active
      document.getElementById(tabName).classList.add('active');
      // Find the clicked button and add active class
      const buttons = document.querySelectorAll('.tab-button');
      for (let button of buttons) {
        if (button.textContent.toLowerCase().includes(tabName.toLowerCase())) {
          button.classList.add('active');
        }
      }
    }
    
    // Variables to track selection
    let selectedItem = null;
    let selectedUsers = [];
    
    // Function to select an item to share
    function selectItem(type, id) {
      // Remove selected class from all items
      const items = document.getElementsByClassName('share-item');
      for (let i = 0; i < items.length; i++) {
        items[i].classList.remove('selected');
      }
      
      // Find the clicked item and add selected class
      const selected = event.currentTarget;
      selected.classList.add('selected');
      
      // Store selection info
      selectedItem = { type: type, id: id };
      
      // Enable share button if at least one user is selected
      updateShareButton();
    }
    
    // Function to select a user
    function selectUser(userId) {
      const userElement = event.currentTarget;
      
      // Toggle selection
      if (selectedUsers.includes(userId)) {
        // Remove from selected users
        selectedUsers = selectedUsers.filter(id => id !== userId);
        userElement.classList.remove('selected');
      } else {
        // Add to selected users
        selectedUsers.push(userId);
        userElement.classList.add('selected');
      }
      
      // Update the checkmark
      const checkmark = userElement.querySelector('.user-selected');
      if (selectedUsers.includes(userId)) {
        checkmark.innerHTML = '✓';
      } else {
        checkmark.innerHTML = '';
      }
      
      // Enable share button if an item is selected
      updateShareButton();
    }
    
    // Function to update share button state
    function updateShareButton() {
      const shareButton = document.getElementById('share-now');
      if (selectedItem && selectedUsers.length > 0) {
        shareButton.disabled = false;
        shareButton.classList.add('active');
      } else {
        shareButton.disabled = true;
        shareButton.classList.remove('active');
      }
    }
    
    // Function to share content
    function shareNow() {
      if (selectedItem && selectedUsers.length > 0) {
        // In a real app, this would send data to the server
        // For demo purposes, just show success notification
        document.getElementById('success-notification').classList.add('show');
        
        // Reset selections after sharing
        setTimeout(() => {
          const items = document.getElementsByClassName('share-item');
          for (let i = 0; i < items.length; i++) {
            items[i].classList.remove('selected');
          }
          
          const userItems = document.getElementsByClassName('user-item');
          for (let i = 0; i < userItems.length; i++) {
            userItems[i].classList.remove('selected');
            userItems[i].querySelector('.user-selected').innerHTML = '';
          }
          
          selectedItem = null;
          selectedUsers = [];
          
          document.getElementById('share-message').value = '';
          
          updateShareButton();
        }, 500);
      }
    }
    
    // Function to close notification
    function closeNotification() {
      document.getElementById('success-notification').classList.remove('show');
    }
    
    // Initialize the share button state
    document.addEventListener('DOMContentLoaded', () => {
      updateShareButton();
    });
