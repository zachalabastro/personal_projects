function togglePopup(){
    document.getElementById("popup-1").classList.toggle("active");
}
function login(){
    document.getElementById("popup-2").classList.toggle("active");
  }

function cancel(){
    document.getElementById("popup-4").classList.toggle("active");
}

function deleteReservationAndClosePopup(index) {
  fetch('/delete/' + index, { method: 'GET' })
      .then(response => {
          if (response.ok) {
              var popup = document.getElementById("popup-2");
              popup.style.display = "none";
          } else {
              console.log('Failed to delete reservation');
          }
      })
      .catch(error => {
          console.error('Error:', error);
      });
}
function showTextBoxAndClosePopup(){
  var textBox = document.getElementById("text-box");
  textBox.style.display = "block";

  setTimeout(function(){
    textBox.style.display = "none";
  }, 4000);

  var popup = document.getElementById("popup-2");
  popup.style.display = "none";
}




