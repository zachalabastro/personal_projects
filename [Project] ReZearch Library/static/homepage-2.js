function togglePopup(){
    var popup = document.getElementById('popup');
    var overlay = document.getElementById('overlay');
    popup.classList.toggle('show');
    overlay.classList.toggle('show');
}

document.addEventListener("DOMContentLoaded", function(){
    var submitPopup = document.getElementById("submitpopup");

    setTimeout(function () {
        submitPopup.style.display = "none";
    }, 5000);
});

window.onload = function() {
    if (window.performance.navigation.type === 1) { 
        window.location.href = "/";
    }
}