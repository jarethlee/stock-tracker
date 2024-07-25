document.addEventListener('DOMContentLoaded', function () {
    const intradayData = JSON.parse(document.getElementById('intradayData').textContent);
    const historicalData = JSON.parse(document.getElementById('historicalData').textContent);

    const intradayLabels = Object.keys(intradayData).reverse();
    const intradayPrices = intradayLabels.map(label => intradayData[label]['Close']);

    const historicalLabels = Object.keys(historicalData).reverse();
    const historicalPrices = historicalLabels.map(label => historicalData[label]['Close']);

    // Create intraday chart
    new Chart(document.getElementById('intradayChart'), {
        type: 'line',
        data: {
            labels: intradayLabels,
            datasets: [{
                label: '1-Minute Close Prices',
                data: intradayPrices,
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
                }
            },
            interaction: {
                mode: 'index',
                intersect: false
            },
            scales: {
                x: {
                    title: { display: false },
                    reverse: true
                },
                y: {
                    title: { display: false }
                }
            }
        }
    });

    // Create historical chart
    new Chart(document.getElementById('historicalChart'), {
        type: 'line',
        data: {
            labels: historicalLabels,
            datasets: [{
                label: 'Daily Close Prices',
                data: historicalPrices,
                borderColor: 'rgba(153, 102, 255, 1)',
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                borderWidth: 1,
                pointRadius: 0
            }]
        },
        options: {
            plugins: {
                legend: { 
                    display: false 
                }
            },
            interaction: {
                mode: 'index',
                intersect: false
            },
            scales: {
                x: {
                    title: { display: false },
                    reverse: true
                },
                y: {
                    title: { display: false }
                }
            }
        }
    });
});