function clique_menu() { //ouvrir et fermer le menu en changeant la taille de la place que prend le contenu et le menu
	var taille = document.getElementById("menu").style.width
	if (taille === "250px") {
		taille = "0px";
	}
	else {
		taille = "250px";
	}
	document.getElementById("menu").style.width=taille
	document.getElementById("contenu").style.marginLeft=taille
}
function toggleDropdown1() {
  var dropdownContent = document.getElementsByClassName("dropdown-content1")[0];
  if (dropdownContent.style.display === "block") {
    dropdownContent.style.display = "none";
  } else {
    dropdownContent.style.display = "block";
  }
}
/*ici je cree 2 fonction indentique pour rendre les 2 boutons idependent*/
function toggleDropdown2() {
  var dropdownContent = document.getElementsByClassName("dropdown-content2")[0];
  if (dropdownContent.style.display === "block") {
    dropdownContent.style.display = "none";
  } else {
    dropdownContent.style.display = "block";
  }
}
//on cherche l'element en fonction de sa class pour ensuite regarder l'etat dans le quelle il est pour le changer quand le bouton est active, onpress: si "block" (actif) -> "none" (cacher) et inversement