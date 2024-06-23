// Function to fetch and display JSON data
function fetchAndDisplayJson() {
    fetch('../json/aboutMe.json')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('json-container');
            container.textContent = JSON.stringify(data, null, 4); // Pretty-print JSON with 4 spaces indentation
        })
        .catch(error => {
            console.error('Error fetching JSON:', error);
            const container = document.getElementById('json-container');
            container.textContent = 'Error loading JSON data';
        });
}

// Call the function to fetch and display the JSON data
fetchAndDisplayJson();
