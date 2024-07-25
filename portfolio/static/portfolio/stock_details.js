function toggleBuyStockForm() {
    var form = document.getElementById('buyStockForm');
    var button = document.getElementById('buyStockButton');
    if (form.style.display === 'none') {
        form.style.display = 'block';
        button.textContent = 'Cancel';
    } else {
        form.style.display = 'none';
        button.textContent = 'Buy Stock';
    }
}

function handleSubmit(event) {
    event.preventDefault();
    sessionStorage.setItem('formSubmitted', 'true');
    event.target.submit();
}

window.onload = function() {
    if (sessionStorage.getItem('formSubmitted') === 'true') {
        alert('Your purchase was successful!');
        sessionStorage.removeItem('formSubmitted');
    } else {
        sessionStorage.removeItem('formSubmitted');
    }
}

function toggleSection(sectionId) {
    const section = document.getElementById(sectionId);
    const icon = document.getElementById(`${sectionId}Icon`);
    const isCollapsed = section.classList.contains('collapse');

    if (isCollapsed) {
        section.classList.remove('collapse');
        icon.classList.remove('bi-chevron-down');
        icon.classList.add('bi-chevron-up');
    } else {
        section.classList.add('collapse');
        icon.classList.remove('bi-chevron-up');
        icon.classList.add('bi-chevron-down');
    }
}