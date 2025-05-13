 
    document.addEventListener('DOMContentLoaded', function() {
      // Fetch user activity data
      fetch('/api/health_data?period=month')
        .then(response => response.json())
        .then(data => {
          // Update dashboard summary
          updateDashboardSummary(data);

          // Create charts
          createRecentActivitiesChart(data);
          createActivityDistributionChart(data);
        })
        .catch(error => {
          console.error('Error fetching data:', error);
          document.querySelectorAll('.summary-value').forEach(el => {
            el.textContent = 'Error loading data';
          });
        });
    });

    function updateDashboardSummary(data) {
      // Calculate totals
      let totalDuration = 0;
      let totalCalories = 0;
      const uniqueDates = new Set();

      data.forEach(item => {
        totalDuration += parseInt(item.duration || 0);
        totalCalories += parseInt(item.calories || 0);
        uniqueDates.add(item.full_date || item.date);
      });

      // Update summary values
      document.getElementById('total-time').textContent = `${totalDuration} mins`;
      document.getElementById('total-calories').textContent = `${totalCalories} kcal`;
      document.getElementById('total-workouts').textContent = `${uniqueDates.size} sessions`;
    }

    function createRecentActivitiesChart(data) {
      // Sort data by date
      data.sort((a, b) => {
        const dateA = a.full_date || a.date;
        const dateB = b.full_date || b.date;
        return dateA.localeCompare(dateB);
      });

      // Get only the most recent 7 days of data
      const recentData = data.slice(-7);

      // Group by date
      const groupedData = {};
      recentData.forEach(item => {
        const date = item.date || new Date(item.full_date).toLocaleDateString('en-US', { weekday: 'short' });

        if (!groupedData[date]) {
          groupedData[date] = {
            duration: 0,
            calories: 0
          };
        }

        groupedData[date].duration += parseInt(item.duration || 0);
        groupedData[date].calories += parseInt(item.calories || 0);
      });

      const labels = Object.keys(groupedData);
      const durationData = labels.map(date => groupedData[date].duration);
      const caloriesData = labels.map(date => groupedData[date].calories);

      const ctx = document.getElementById('recentActivitiesChart').getContext('2d');
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Duration (mins)',
              data: durationData,
              backgroundColor: 'rgba(255, 99, 132, 0.7)',
              borderColor: 'rgba(255, 99, 132, 1)',
              borderWidth: 1,
              yAxisID: 'y'
            },
            {
              label: 'Calories',
              data: caloriesData,
              backgroundColor: 'rgba(54, 162, 235, 0.7)',
              borderColor: 'rgba(54, 162, 235, 1)',
              borderWidth: 1,
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
              position: 'left',
              title: {
                display: true,
                text: 'Duration (mins)'
              }
            },
            y1: {
              beginAtZero: true,
              position: 'right',
              grid: {
                drawOnChartArea: false
              },
              title: {
                display: true,
                text: 'Calories'
              }
            }
          }
        }
      });
    }

    function createActivityDistributionChart(data) {
      // Group by exercise type
      const exerciseTypes = {};

      data.forEach(item => {
        const type = item.exercise_type || 'Unknown';

        if (!exerciseTypes[type]) {
          exerciseTypes[type] = 0;
        }

        exerciseTypes[type] += parseInt(item.duration || 0);
      });

      const labels = Object.keys(exerciseTypes);
      const durationData = labels.map(type => exerciseTypes[type]);

      // Generate colors
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

      const ctx = document.getElementById('activityDistributionChart').getContext('2d');
      new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: labels,
          datasets: [
            {
              data: durationData,
              backgroundColor: backgroundColors.slice(0, labels.length),
              borderColor: backgroundColors.map(color => color.replace('0.7', '1')).slice(0, labels.length),
              borderWidth: 1
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'right'
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  const label = context.label || '';
                  const value = context.raw || 0;
                  const total = context.dataset.data.reduce((a, b) => a + b, 0);
                  const percentage = Math.round((value / total) * 100);
                  return `${label}: ${value} mins (${percentage}%)`;
                }
              }
            }
          }
        }
      });
    }
 