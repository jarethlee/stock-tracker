document.addEventListener('DOMContentLoaded', function() {
    const stockTrackerLink = document.getElementById('stockTrackerLink');
    const icon = stockTrackerLink.querySelector('i');

    stockTrackerLink.addEventListener('mouseenter', function() {
        stockTrackerLink.classList.add('text-yellow');
        icon.classList.remove('bi-graph-up');
        icon.classList.add('bi-graph-up-arrow', 'text-yellow');
    });

    stockTrackerLink.addEventListener('mouseleave', function() {
        stockTrackerLink.classList.remove('text-yellow');
        icon.classList.remove('bi-graph-up-arrow', 'text-yellow');
        icon.classList.add('bi-graph-up');
    });
});