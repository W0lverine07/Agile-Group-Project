$(document).ready(function() {
    // Form toggling
    $('.switch-btn').click(function() {
        $('.switch-btn').removeClass('active');
        $(this).addClass('active');
  
        const formToShow = $(this).data('form');
        $('.form-container').addClass('hidden');
        $(`#${formToShow}-form`).removeClass('hidden');
    });

    // Password matching validation with visual feedback
    $('#register-form form').submit(function(e) {
        const password = $('#password').val();
        const confirmPassword = $('#confirm_password').val();
  
        if (password !== confirmPassword) {
            e.preventDefault();
            $('#password, #confirm_password').addClass('error'); // Add error class for visual feedback
            $('#password-feedback').text('Passwords do not match. Please try again.').css('color', 'red');
        }
    });
  
    // Clear error messages when user starts typing
    $('#password, #confirm_password').on('input', function() {
        $(this).removeClass('error');
        $('#password-feedback').text('');
    });
  
    // Username validation with debounce
    let debounceTimer;
    const usernameInput = document.getElementById("username");
    const feedback = document.getElementById("username-feedback");

    if (!usernameInput || !feedback) return;

    usernameInput.addEventListener("input", function () {
        const username = this.value;

        if (username.length < 3) {
            feedback.textContent = "";
            return;
        }

        // Clear previous timeout
        clearTimeout(debounceTimer);

        // Set new debounce timer
        debounceTimer = setTimeout(() => {
            fetch("/check_username", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: `username=${encodeURIComponent(username)}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.exists) {
                    feedback.textContent = "❌ Username already taken";
                    feedback.style.color = "red";
                } else {
                    feedback.textContent = "✅ Username available";
                    feedback.style.color = "green";
                }
            })
            .catch(err => {
                feedback.textContent = "⚠️ Could not check username";
                feedback.style.color = "orange";
            });
        }, 500); // Adjust delay as necessary
    });
});
