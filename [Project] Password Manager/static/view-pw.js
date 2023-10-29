document.addEventListener('DOMContentLoaded', function() {
    // References to the elements
    var popup = document.getElementById('passwordPopup');
    var overlay = document.querySelector('.overlay');
    var addButton = document.querySelector('.add-password');
    var closeButton = document.querySelector('.close-btn');

    // Event listener to open the popup
    addButton.addEventListener('click', function() {
        popup.style.display = 'block';
        overlay.style.display = 'block';
    });

    // Event listener to close the popup using the close button
    closeButton.addEventListener('click', function() {
        popup.style.display = 'none';
        overlay.style.display = 'none';
    });

    // Event listener to close the popup when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target == popup) {
            popup.style.display = 'none';
        }
    });

    document.getElementById('showPassword').addEventListener('change', function(e) {
        var passwordInput = document.getElementById('passwordValue');
        if (e.target.checked) {
            passwordInput.type = 'text';
        } else {
            passwordInput.type = 'password';
        }
    });
});