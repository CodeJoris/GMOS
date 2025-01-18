document.getElementById('runButton').addEventListener('click', function() {
    fetch('/main.py')
    .then(response => response.text())
    .then(data => {
        document.getElementById('result').innerText = data;
    });
});