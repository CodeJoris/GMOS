var var_startAdress;
var var_endAdress;
function saveData() {
  const startAdress = document.getElementById("id_startAdress").value;
  const endAdress = document.getElementById("id_endAdress").value;

  // Prepare the data to send to the backend
  const data = {
      startAdress: startAdress,
      endAdress: endAdress
  };

  // Send the data to the server using a POST request
  fetch('http://localhost:3000/save-addresses', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(result => {
      alert('Data saved to JSON file successfully!');
  })
  .catch(error => {
      console.error('Error:', error);
  });
}

