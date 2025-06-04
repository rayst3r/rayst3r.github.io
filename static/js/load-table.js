document.addEventListener('DOMContentLoaded', function() {
    fetch('static/tables/results_updated.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('results-table').innerHTML = data;
        })
        .catch(error => console.error('Error loading table:', error));
}); 