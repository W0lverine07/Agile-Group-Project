$(document).ready(function() {
    // Form toggling
    $('.switch-btn').click(function() {
      $('.switch-btn').removeClass('active');
      $(this).addClass('active');
  
      const formToShow = $(this).data('form');
      $('.form-container').addClass('hidden');
      $(`#${formToShow}-form`).removeClass('hidden');
    });
  
    // Password matching validation
    $('#register-form form').submit(function(e) {
      const password = $('#password').val();
      const confirmPassword = $('#confirm_password').val();
  
      if (password !== confirmPassword) {
        e.preventDefault();
        alert('Passwords do not match. Please try again.');
      }
    });
  });
  
document.addEventListener("DOMContentLoaded", () => {
    const usernameInput = document.getElementById("username");
    const feedback = document.getElementById("username-feedback");

    if (!usernameInput || !feedback) return;

    usernameInput.addEventListener("input", function () {
        const username = this.value;

        if (username.length < 3) {
            feedback.textContent = "";
            return;
        }

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
    });
});
