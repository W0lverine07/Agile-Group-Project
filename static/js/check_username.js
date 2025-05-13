$(document).ready(function () {
    // ===== Username Availability Check =====
    const usernameInput = $('#username');
    const feedback = $('#username-feedback');

    usernameInput.on('blur', function () {
        const username = usernameInput.val().trim();
        if (username.length < 3) {
            feedback.text('Username must be at least 3 characters long.').css('color', 'red');
            return;
        }

        $.ajax({
            url: '/check_username',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ username: username }),
            success: function (response) {
                if (response.available) {
                    feedback.text('Username is available.').css('color', 'green');
                } else {
                    feedback.text('Username is taken.').css('color', 'red');
                }
            },
            error: function () {
                feedback.text('Error checking username. Please try again.').css('color', 'red');
            }
        });
    });

    // ===== Password Match Check =====
    const password = $('#password');
    const confirmPassword = $('#confirm_password');

    confirmPassword.on('input', function () {
        if (confirmPassword.val() !== password.val()) {
            confirmPassword[0].setCustomValidity("Passwords do not match.");
        } else {
            confirmPassword[0].setCustomValidity('');
        }
    });

    // ===== Form Switcher Logic =====
    $('.switch-btn').on('click', function () {
        const targetForm = $(this).data('form');
        $('.switch-btn').removeClass('active');
        $(this).addClass('active');

        $('.form-container').addClass('hidden');
        $('#' + targetForm + '-form').removeClass('hidden');
    });

    // ===== Optional: Show/Hide Terms Modal (already in your HTML) =====
});
