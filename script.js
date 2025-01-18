function exportToJson() {
    // Get the user input value
    const userInput = document.getElementById('userInput').value;
    
    // Create a JSON object
    const data = {
        userInput: userInput
    };

    // Convert JSON object to a string
    const jsonData = JSON.stringify(data, null, 2);

    // Create a Blob from the JSON string
    const blob = new Blob([jsonData], { type: 'application/json' });

    // Create a link element
    const link = document.createElement('a');

    // Set the download attribute with the file name
    link.download = 'user_input.json';

    // Create a URL for the Blob and set it as the href attribute
    link.href = URL.createObjectURL(blob);

    // Append the link to the body (it won’t be visible)
    document.body.appendChild(link);

    // Programmatically click the link to trigger the download
    link.click();

    // Remove the link element after the download
    document.body.removeChild(link);
}
