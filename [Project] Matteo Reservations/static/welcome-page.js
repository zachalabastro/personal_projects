function togglePopup(){
    document.getElementById("popup-1").classList.toggle("active");
}

function login(){
    document.getElementById("popup-2").classList.toggle("active");
}
document.addEventListener("DOMContentLoaded", function() {
    var myDiv = document.getElementById("text-box");

    setTimeout(function() {
        myDiv.style.display = "none";
    }, 5000);
});