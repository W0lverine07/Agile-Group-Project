document.addEventListener('DOMContentLoaded', function() {
    // Set default date to today
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('date').value = today;

    // Device import modal
    const modal = document.getElementById('deviceModal');
    const importBtn = document.getElementById('importDataBtn');
    const closeBtn = document.querySelector('.close-btn');
    const cancelBtn = document.getElementById('cancelBtn');
    const devices = document.querySelectorAll('.device');
    const connectBtn = document.getElementById('connectBtn');
    const connectionMessage = document.getElementById('connectionMessage');
    const loadingSpinner = document.getElementById('loadingSpinner');

    // Add event listeners for exercise type and duration to update calories
    document.getElementById('exercise_type').addEventListener('change', updateCalories);
    document.getElementById('duration').addEventListener('change', updateCalories);
    document.getElementById('duration').addEventListener('input', updateCalories);

    // Open modal
    importBtn.addEventListener('click', function() {
        modal.style.display = 'flex';
    });

    // Close modal
    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    cancelBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    // Close modal when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Device selection
    let selectedDevice = null;
    
    devices.forEach(device => {
        device.addEventListener('click', function() {
            devices.forEach(d => d.classList.remove('selected'));
            this.classList.add('selected');
            selectedDevice = this.dataset.device;
            connectBtn.disabled = false;
        });
    });

    // Connect button
    connectBtn.addEventListener('click', function() {
        if (selectedDevice) {
            // Show loading
            loadingSpinner.style.display = 'block';
            connectionMessage.textContent = `Connecting to ${selectedDevice}...`;
            
            // Simulate connection delay
            setTimeout(function() {
                // Simulate data retrieval
                loadingSpinner.style.display = 'none';
                
                if (Math.random() > 0.2) { // 80% success chance
                    connectionMessage.textContent = `Successfully imported data from ${selectedDevice}!`;
                    connectionMessage.classList.add('success');
                    
                    // Get random exercise type
                    const exerciseSelect = document.getElementById('exercise_type');
                    const randomExerciseIndex = Math.floor(Math.random() * (exerciseSelect.options.length - 1)) + 1;
                    exerciseSelect.selectedIndex = randomExerciseIndex;
                    
                    // Fill form with random data
                    const duration = Math.floor(Math.random() * 50) + 20; // 20-70 minutes
                    document.getElementById('duration').value = duration;
                    
                    // Calculate calories
                    updateCalories();
                    
                    // Close modal after a delay
                    setTimeout(function() {
                        modal.style.display = 'none';
                        connectionMessage.classList.remove('success');
                    }, 2000);
                } else {
                    // Failure case
                    connectionMessage.textContent = `Failed to connect to ${selectedDevice}. Please try again.`;
                    connectionMessage.classList.add('error');
                    
                    setTimeout(function() {
                        connectionMessage.classList.remove('error');
                        connectionMessage.textContent = 'Select a device to connect';
                    }, 3000);
                }
            }, 2000);
        }
    });
    
    // Form validation
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        const exerciseType = document.getElementById('exercise_type').value;
        const duration = document.getElementById('duration').value;
        
        if (!exerciseType || !duration) {
            event.preventDefault();
            alert('Please select an exercise type and enter duration.');
        }
    });
});

// Function to update calories based on exercise type and duration
function updateCalories() {
    const exerciseSelect = document.getElementById('exercise_type');
    const duration = document.getElementById('duration').value;
    const caloriesField = document.getElementById('calories');
    
    if (exerciseSelect.selectedIndex > 0 && duration > 0) {
        const selectedOption = exerciseSelect.options[exerciseSelect.selectedIndex];
        const caloriesPerMinute = parseFloat(selectedOption.dataset.rate);
        const totalCalories = Math.round(caloriesPerMinute * duration);
        
        caloriesField.value = totalCalories;
    } else {
        caloriesField.value = '';
    }
}

// Alternative method using AJAX for server-side calculation
function updateCaloriesFromServer() {
    const exerciseTypeId = document.getElementById('exercise_type').value;
    const duration = document.getElementById('duration').value;
    
    if (exerciseTypeId && duration > 0) {
        fetch(`/api/calculate_calories?exercise_type_id=${exerciseTypeId}&duration=${duration}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('calories').value = data.calories;
            })
            .catch(error => {
                console.error('Error calculating calories:', error);
            });
    }
}