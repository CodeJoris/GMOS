document.getElementById('runButton').addEventListener('click', function() {
    fetch('/frontend-dev.py')
    .then(response => response.text())
    .then(data => {
        document.getElementById('result').innerText = data;
    });
});