document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('showPassword').addEventListener('change', function(e) {
        var passwordInput = document.getElementById('password');
        if (e.target.checked) {
            passwordInput.type = 'text';
        } else {
            passwordInput.type = 'password';
        }
    });
});
