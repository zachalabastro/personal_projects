function togglePopup(){
    document.getElementById("popup-1").classList.toggle("active");
}

function reserve(){
    document.getElementById("popup-3").classList.toggle("active");
}

function handleButtonClick(tableClass) {
    document.getElementById('table_class_input').value = tableClass;
  }

function login(){
    document.getElementById("popup-2").classList.toggle("active");
}
