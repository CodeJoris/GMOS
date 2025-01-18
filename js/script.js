var adresse;
var ldt;
function saveData() {
  localStorage.setItem("adresse", document.getElementById("adresse").value);
  localStorage.setItem("ldt", document.getElementById("ldt").value);

}
  
window.onload = () => { //attend que toute les information de la page soivent charge pour etre sur que tout marche bien comme il faut 
var a = document.createElement('a');
a.href = 'https://www.google.ca/maps';
a.textContent = 'Google Maps';
a.target = '_blank';
document.body.appendChild(a);

  var button1 = document.getElementById('button1');
  var image1 = document.getElementById('image');
  var text1 = document.getElementById("text") ; 
  let currentText1 = 0 ;
  let currentImage1 = 0;
  var texts1 = ["Entrez la station de bus la plus proche de chez vous que vous souhaitez utiliser sur "+ a.innerText, "Cliquez sur l'onglet avec les horraire du bus", 'Copier l\'URL dans la case "adresse" puis faite la meme chose pour votre lieu de travail']
  var images1 = ['../image/tuto1.png', '../image/tuto2.png', '../image/tuto3.png'];

  button1.addEventListener('click', () => {
	currentText1 = (currentText1 + 1) % texts1.length;
    text1.textContent = texts1[currentText1];
    currentImage1 = (currentImage1 + 1) % images1.length;
    image1.src = images1[currentImage1];
  });
};

/*tentative de deuxieme bouton mais ca marche pas tres bien
  var button2 = document.getElementById('button2');
  var image2 = document.getElementById('image');
  var text2 = document.getElementById("text") ; 
  let currentText2 = 0 ;
  let currentImage2 = 0;
  var images2 = ['../image/tuto1.png', '../image/tuto2.png', '../image/tuto3.png'];
  var texts2 = ['Entrez la station de bus la plus proche de chez vous que vous souhaitez utiliser sur '+ lien.innerHTML, "Cliquez sur l'onglet avec les horraire du bus", "Copier l'URL dans la case \"adresse\" puis faite la meme chose pour votre lieu de travail"]
button2.addEventListener('click', () => {
  currentImage2 = (currentImage2 - 1 + images2.length) % images2.length;
  image2.src = images2[currentImage2];
  currentText2 = (currentText2 - 1 + texts2.length) % texts2.length;
  text2.textContent = texts2[currentText2];
});
*/