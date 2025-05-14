// Global variables
let activityChart = null;
let distributionChart = null;
let intensityChart = null;
let consistencyChart = null;
let comparisonChart = null;
let tableData = [];
let filteredData = [];
let currentPage = 1;
const rowsPerPage = 6;
let sortColumn = 0;
let sortDirection = 'desc';

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    // Parse data from server
    parseServerData();
    
    // Create the initial charts
    createActivityChart();
    createDistributionChart();
    createExtraCharts();
    
    // Populate the table
    populateTable();
    
    // Update progress bars
    updateProgressBars();
    
    // Add event listeners
    setupEventListeners();
});

function setupEventListeners() {
    // Pagination buttons
    document.getElementById('prev-page').addEventListener('click', prevPage);
    document.getElementById('next-page').addEventListener('click', nextPage);
    
    // Time period filter
    document.getElementById('time-period').addEventListener('change', updateCharts);
    
    // Data toggles
    document.getElementById('show-duration').addEventListener('change', function() {
        toggleDataset('duration');
    });
    document.getElementById('show-calories').addEventListener('change', function() {
        toggleDataset('calories');
    });
    
    // Table search
    document.getElementById('table-search').addEventListener('input', filterTable);
    
    // Export button
    document.getElementById('export-csv').addEventListener('click', exportCSV);
    
    // Share prompt
    document.getElementById('close-share-prompt').addEventListener('click', closeSharePrompt);
    
    // Table headers for sorting
    const headers = document.querySelectorAll('#activityDataTable th');
    headers.forEach((header, index) => {
        if (index < 4) { // Only first 4 columns are sortable
            header.addEventListener('click', () => sortTable(index));
        }
    });
}

function parseServerData() {
    if (serverData && serverData.length > 0) {
        // Parse JSON if it's a string
        if (typeof serverData === 'string') {
            tableData = JSON.parse(serverData);
        } else {
            tableData = serverData;
        }
        filteredData = [...tableData];
    } else {
        // Demo data if no server data
        tableData = generateDemoData();
        filteredData = [...tableData];
    }
}

function createActivityChart() {
    const ctx = document.getElementById('activityChart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (activityChart) {
        activityChart.destroy();
    }
    
    // Group data by date
    const groupedData = {};
    filteredData.forEach(item => {
        if (!groupedData[item.date]) {
            groupedData[item.date] = {
                duration: 0,
                calories: 0
            };
        }
        let duration = Math.round(Number(item.duration));
        groupedData[item.date].duration += duration;
        groupedData[item.date].calories += parseInt(item.calories);
    });
    
    // Prepare data for chart
    const labels = Object.keys(groupedData);
    const durationData = Object.values(groupedData).map(item => item.duration);
    const caloriesData = Object.values(groupedData).map(item => item.calories);
    
    // Create chart
    activityChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Duration (mins)',
                    data: durationData,
                    borderColor: '#ff0000',
                    backgroundColor: 'rgba(255, 0, 0, 0.1)',
                    fill: true,
                    tension: 0.4,
                    yAxisID: 'y'
                },
                {
                    label: 'Calories',
                    data: caloriesData,
                    borderColor: '#16a085',
                    backgroundColor: 'rgba(22, 160, 133, 0.1)',
                    fill: true,
                    tension: 0.4,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Duration (mins)'
                    }
                },
                y1: {
                    beginAtZero: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Calories'
                    },
                    grid: {
                        drawOnChartArea: false
                    }
                }
            }
        }
    });
}

function createDistributionChart() {
    const ctx = document.getElementById('distributionChart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (distributionChart) {
        distributionChart.destroy();
    }
    
    // Group data by exercise type
    const groupedData = {};
    filteredData.forEach(item => {
        if (!groupedData[item.exercise_type]) {
            groupedData[item.exercise_type] = {
                duration: 0,
                calories: 0,
                count: 0
            };
        }
        groupedData[item.exercise_type].duration += parseInt(item.duration);
        groupedData[item.exercise_type].calories += parseInt(item.calories);
        groupedData[item.exercise_type].count += 1;
    });
    
    // Prepare data for chart
    const labels = Object.keys(groupedData);
    const durationData = labels.map(type => groupedData[type].duration);
    const caloriesData = labels.map(type => groupedData[type].calories);
    const countData = labels.map(type => groupedData[type].count);
    
    // Color palette
    const backgroundColors = [
        'rgba(255, 99, 132, 0.7)',
        'rgba(54, 162, 235, 0.7)',
        'rgba(255, 206, 86, 0.7)',
        'rgba(75, 192, 192, 0.7)',
        'rgba(153, 102, 255, 0.7)',
        'rgba(255, 159, 64, 0.7)',
        'rgba(199, 199, 199, 0.7)',
        'rgba(83, 102, 255, 0.7)',
        'rgba(40, 159, 64, 0.7)',
        'rgba(210, 199, 199, 0.7)'
    ];
    
    // Create chart
    distributionChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Total Duration (mins)',
                    data: durationData,
                    backgroundColor: backgroundColors.map(color => color.replace('0.7', '0.8')),
                    borderColor: backgroundColors.map(color => color.replace('0.7', '1')),
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    callbacks: {
                        afterLabel: function(context) {
                            const index = context.dataIndex;
                            const label = context.label;
                            return [
                                `Calories: ${caloriesData[index]}`,
                                `Workouts: ${countData[index]}`
                            ];
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Total Duration (mins)'
                    }
                }
            }
        }
    });
}

function createExtraCharts() {
    // Create intensity chart
    const intensityCtx = document.getElementById('intensityChart').getContext('2d');
    
    if (intensityChart) {
        intensityChart.destroy();
    }
    
    // Calculate intensity levels
    const intensityLevels = {
        'Low': 0,
        'Moderate': 0,
        'High': 0,
        'Very High': 0
    };
    
    filteredData.forEach(item => {
        const duration = parseInt(item.duration);
        const calories = parseInt(item.calories);
        const calsPerMinute = calories / duration;
        
        if (calsPerMinute < 5) {
            intensityLevels['Low'] += duration;
        } else if (calsPerMinute < 8) {
            intensityLevels['Moderate'] += duration;
        } else if (calsPerMinute < 12) {
            intensityLevels['High'] += duration;
        } else {
            intensityLevels['Very High'] += duration;
        }
    });
    
    intensityChart = new Chart(intensityCtx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(intensityLevels),
            datasets: [{
                data: Object.values(intensityLevels),
                backgroundColor: [
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 159, 64, 0.8)',
                    'rgba(255, 99, 132, 0.8)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
    
    // Create consistency chart (simplified heatmap)
    const consistencyCtx = document.getElementById('consistencyChart').getContext('2d');
    
    if (consistencyChart) {
        consistencyChart.destroy();
    }
    
    // Group by weekday
    const weekdayData = {
        'Mon': 0,
        'Tue': 0,
        'Wed': 0,
        'Thu': 0,
        'Fri': 0,
        'Sat': 0,
        'Sun': 0
    };
    
    filteredData.forEach(item => {
        const date = new Date(item.full_date);
        const weekday = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'][date.getDay()];
        weekdayData[weekday] += 1;
    });
    
    consistencyChart = new Chart(consistencyCtx, {
        type: 'bar',
        data: {
            labels: Object.keys(weekdayData),
            datasets: [{
                label: 'Workout Frequency',
                data: Object.values(weekdayData),
                backgroundColor: 'rgba(54, 162, 235, 0.8)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Workouts'
                    }
                }
            }
        }
    });
    
    // Create comparison chart
    const comparisonCtx = document.getElementById('comparisonChart').getContext('2d');
    
    if (comparisonChart) {
        comparisonChart.destroy();
    }
    
    // Calculate calories per minute by exercise type
    const efficiencyData = {};
    
    filteredData.forEach(item => {
        const type = item.exercise_type;
        if (!efficiencyData[type]) {
            efficiencyData[type] = {
                totalCalories: 0,
                totalDuration: 0
            };
        }
        
        efficiencyData[type].totalCalories += parseInt(item.calories);
        efficiencyData[type].totalDuration += parseInt(item.duration);
    });
    
    const efficiencyLabels = Object.keys(efficiencyData);
    const efficiencyValues = efficiencyLabels.map(type => {
        const data = efficiencyData[type];
        return data.totalCalories / data.totalDuration;
    });
    
    comparisonChart = new Chart(comparisonCtx, {
        type: 'bar',
        data: {
            labels: efficiencyLabels,
            datasets: [{
                label: 'Calories per Minute',
                data: efficiencyValues,
                backgroundColor: 'rgba(153, 102, 255, 0.8)',
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Calories per Minute'
                    }
                }
            }
        }
    });
}

function populateTable() {
    const tableBody = document.getElementById('activityDataBody');
    tableBody.innerHTML = '';
    
    // Calculate pagination
    const startIndex = (currentPage - 1) * rowsPerPage;
    const endIndex = startIndex + rowsPerPage;
    const paginatedData = filteredData.slice(startIndex, endIndex);
    
    // Update pagination controls
    document.getElementById('page-indicator').textContent = `Page ${currentPage} of ${Math.ceil(filteredData.length / rowsPerPage) || 1}`;
    document.getElementById('prev-page').disabled = currentPage === 1;
    document.getElementById('next-page').disabled = currentPage >= Math.ceil(filteredData.length / rowsPerPage);
    
    // Add rows to table
    paginatedData.forEach(item => {
        const row = document.createElement('tr');
        
        // Date cell
        const dateCell = document.createElement('td');
        dateCell.textContent = item.full_date || item.date;
        row.appendChild(dateCell);
        
        // Exercise type cell
        const typeCell = document.createElement('td');
        typeCell.textContent = item.exercise_type || "Unknown";
        row.appendChild(typeCell);
        
        // Duration cell
        const durationCell = document.createElement('td');
        durationCell.textContent = item.duration;
        row.appendChild(durationCell);
        
        // Calories cell
        const caloriesCell = document.createElement('td');
        caloriesCell.textContent = item.calories;
        row.appendChild(caloriesCell);
        
        // Actions cell
        const actionsCell = document.createElement('td');
        
        // Share button
        const shareButton = document.createElement('button');
        shareButton.className = 'action-btn share-btn';
        shareButton.textContent = 'Share';
        shareButton.addEventListener('click', function() { shareActivity(item); });
        actionsCell.appendChild(shareButton);
        
        row.appendChild(actionsCell);
        
        tableBody.appendChild(row);
    });
}

function updateProgressBars() {
    // Calculate progress values
    let totalDuration = 0;
    let totalCalories = 0;
    let workoutCount = 0;
    
    // Group by date to count unique workout days
    const workoutDays = new Set();
    
    filteredData.forEach(item => {
        totalDuration += parseInt(item.duration);
        totalCalories += parseInt(item.calories);
        workoutDays.add(item.full_date || item.date);
    });
    
    workoutCount = workoutDays.size;
    
    // Update duration progress
    const durationGoal = 300; // minutes per week
    const durationPercent = Math.min(Math.round((totalDuration / durationGoal) * 100), 100);
    document.getElementById('duration-progress').textContent = `${totalDuration}/${durationGoal} mins`;
    document.getElementById('duration-fill').style.width = `${durationPercent}%`;
    
    // Update calories progress
    const caloriesGoal = 2500; // calories per week
    const caloriesPercent = Math.min(Math.round((totalCalories / caloriesGoal) * 100), 100);
    document.getElementById('calories-progress').textContent = `${totalCalories}/${caloriesGoal}`;
    document.getElementById('calories-fill').style.width = `${caloriesPercent}%`;
    
    // Update weekly workout progress
    const workoutGoal = 5; // workouts per week
    const workoutPercent = Math.min(Math.round((workoutCount / workoutGoal) * 100), 100);
    document.getElementById('weekly-progress').textContent = `${workoutCount}/${workoutGoal} workouts`;
    document.getElementById('weekly-fill').style.width = `${workoutPercent}%`;
    
    // Update goal cards if they exist
    if (document.getElementById('weekly-goal-fill')) {
        document.getElementById('weekly-goal-fill').style.width = `${workoutPercent}%`;
        document.querySelector('.goal-value').textContent = `${workoutCount}/${workoutGoal} workouts`;
    }
    
    if (document.getElementById('calorie-goal-fill')) {
        document.getElementById('calorie-goal-fill').style.width = `${caloriesPercent}%`;
        document.querySelectorAll('.goal-value')[1].textContent = `${totalCalories}/${caloriesGoal} kcal`;
    }
}

function updateCharts() {
    // When time period changes, fetch new data from server
    const newPeriod = document.getElementById('time-period').value;
    
    if (userId) {
        // Show loading state
        document.querySelectorAll('.chart-wrapper').forEach(wrapper => {
            wrapper.classList.add('loading');
        });
        
        // Make AJAX request to get data for the new time period
        fetch(`/api/health_data?period=${newPeriod}`)
            .then(response => response.json())
            .then(data => {
                tableData = data;
                filteredData = [...tableData];
                createActivityChart();
                createDistributionChart();
                createExtraCharts();
                populateTable();
                updateProgressBars();
                
                // Remove loading state
                document.querySelectorAll('.chart-wrapper').forEach(wrapper => {
                    wrapper.classList.remove('loading');
                });
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                
                // Remove loading state
                document.querySelectorAll('.chart-wrapper').forEach(wrapper => {
                    wrapper.classList.remove('loading');
                });
                
                // Show error message
                alert('Failed to fetch data. Please try again later.');
            });
    } else {
        // No user ID available, just use demo data
        createActivityChart();
        createDistributionChart();
        createExtraCharts();
    }
}

function toggleDataset(datasetName) {
    const isVisible = document.getElementById(`show-${datasetName}`).checked;
    
    if (activityChart) {
        activityChart.data.datasets.forEach(dataset => {
            if (dataset.label.toLowerCase().includes(datasetName)) {
                dataset.hidden = !isVisible;
            }
        });
        activityChart.update();
    }
    
    if (distributionChart) {
        distributionChart.data.datasets.forEach(dataset => {
            if (dataset.label.toLowerCase().includes(datasetName)) {
                dataset.hidden = !isVisible;
            }
        });
        distributionChart.update();
    }
}

function sortTable(columnIndex) {
    if (sortColumn === columnIndex) {
        // Toggle sort direction
        sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
    } else {
        // New column, default to descending
        sortColumn = columnIndex;
        sortDirection = 'desc';
    }
    
    // Sort the data
    filteredData.sort((a, b) => {
        let valA, valB;
        
        switch (columnIndex) {
            case 0: // Date
                valA = a.full_date || a.date;
                valB = b.full_date || b.date;
                break;
            case 1: // Exercise Type
                valA = a.exercise_type || '';
                valB = b.exercise_type || '';
                break;
            case 2: // Duration
                valA = parseInt(a.duration);
                valB = parseInt(b.duration);
                break;
            case 3: // Calories
                valA = parseInt(a.calories);
                valB = parseInt(b.calories);
                break;
            default:
                return 0;
        }
        
        if (valA < valB) return sortDirection === 'asc' ? -1 : 1;
        if (valA > valB) return sortDirection === 'asc' ? 1 : -1;
        return 0;
    });
    
    // Reset pagination to first page
    currentPage = 1;
    
    // Update table
    populateTable();
}

function filterTable() {
    const searchTerm = document.getElementById('table-search').value.toLowerCase();
    
    if (searchTerm.trim() === '') {
        filteredData = [...tableData];
    } else {
        filteredData = tableData.filter(item => {
            return (
                (item.full_date && item.full_date.toLowerCase().includes(searchTerm)) ||
                (item.date && item.date.toLowerCase().includes(searchTerm)) ||
                (item.exercise_type && item.exercise_type.toLowerCase().includes(searchTerm)) ||
                String(item.duration).includes(searchTerm) ||
                String(item.calories).includes(searchTerm)
            );
        });
    }
    
    // Reset to first page
    currentPage = 1;
    
    // Update table and charts
    populateTable();
    createActivityChart();
    createDistributionChart();
    createExtraCharts();
    updateProgressBars();
}

function prevPage() {
    if (currentPage > 1) {
        currentPage--;
        populateTable();
    }
}

function nextPage() {
    if (currentPage < Math.ceil(filteredData.length / rowsPerPage)) {
        currentPage++;
        populateTable();
    }
}

function exportCSV() {
    // Create CSV content
    let csv = 'Date,Exercise Type,Duration (mins),Calories\n';
    
    filteredData.forEach(item => {
        csv += `${item.full_date || item.date},${item.exercise_type || 'Unknown'},${item.duration},${item.calories}\n`;
    });
    
    // Create download link
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.setAttribute('hidden', '');
    a.setAttribute('href', url);
    a.setAttribute('download', 'activity_data.csv');
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

function shareActivity(activity) {
    // Redirect to share page with activity data
    const activityId = activity.id || '1';
    const date = activity.full_date || activity.date;
    window.location.href = `/share_page?content_type=activity&content_id=${activityId}&date=${date}`;
}

function closeSharePrompt() {
    document.getElementById('share-prompt').style.display = 'none';
}