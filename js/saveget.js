var startPoint;
var endPoint;
function getDataStart()
{
  var ad = localStorage.getItem("startPoint");
  document.getElementById("startAdress").setAttribute("href", ad);
  
}

function getDataEnd() 
{
  var l = localStorage.getItem("endPoint");
  document.getElementById("linkldt").setAttribute("href", l);
  
  
}
window.onload = () => {
document.getElementById("framel").setAttribute("src", localStorage.getItem("ldt"));
document.getElementById("frameb").setAttribute("src", localStorage.getItem("adresse"));
}
