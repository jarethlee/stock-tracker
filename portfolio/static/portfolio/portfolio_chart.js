document.addEventListener('DOMContentLoaded', function() {
    const portfolioPerformanceData = JSON.parse(document.getElementById('portfolioPerformanceData').textContent);

    const aggregatedData = {};
    
    portfolioPerformanceData.forEach(dataset => {
        dataset.forEach(item => {
            const date = item.Date;
            const close = item.Close;

            if (!aggregatedData[date]) {
                aggregatedData[date] = 0;
            }
            aggregatedData[date] += close;
        });
    });

    const chartLabels = Object.keys(aggregatedData);
    const chartData = chartLabels.map(date => aggregatedData[date]);

    new Chart(document.getElementById('portfolioPerformanceChart'), {
        type: 'line',
        data: {
            labels: chartLabels,
            datasets: [{
                label: 'Portfolio Performance',
                data: chartData,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderWidth: 1,
                pointRadius: 0
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false 
                },
            },
            interaction: {
                mode: 'index',
                intersect: false
            },
            scales: {
                x: {
                    title: { display: false },
                },
                y: {
                    title: { display: false },
                }
            }
        }
    });
});