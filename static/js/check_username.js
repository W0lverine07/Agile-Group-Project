$(document).ready(function () {
    // ===== Username Availability Check =====
    const usernameInput = $('#username');
    const feedback = $('#username-feedback');

    let debounceTimer;
    usernameInput.on('input', function () {
        clearTimeout(debounceTimer);
        const username = usernameInput.val().trim();

        debounceTimer = setTimeout(() => {
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
                        feedback.text('Username is available').css('color', 'lightgreen');
                    } else {
                        feedback.text('Username is already taken').css('color', 'red');
                    }
                },
                error: function () {
                    feedback.text('Error checking username. Please try again.').css('color', 'orange');
                }
            });
        }, 300); // runs only after 300ms of no typing
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

// ========== Terms and Privacy Popup Handler ==========
window.showPopup = function(type) {
    let title = "", content = "";
    if (type === 'terms') {
        title = "Terms and Conditions";
        content = `
            <strong>1. Acceptance of Terms:</strong> By registering or using the Wellness Tracker application, you agree to comply with and be bound by these Terms and Conditions.<br><br>
            <strong>2. Not Medical Advice:</strong> The information provided by Wellness Tracker is for general health tracking purposes only. It is <em>not</em> a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for any medical concerns.<br><br>
            <strong>3. User Responsibility:</strong> You are responsible for maintaining the accuracy of the information you input. Misuse or false data may affect analytics and recommendations.<br><br>
            <strong>4. Privacy and Data Use:</strong> Your personal data will be stored securely and not shared with third parties without consent.<br><br>
            <strong>5. Account Security:</strong> You must not share your login credentials. You are solely responsible for all activities under your account.<br><br>
            <strong>6. Prohibited Activities:</strong> Do not use the app unlawfully, interfere with systems, or upload malicious content.<br><br>
            <strong>7. Changes to the App:</strong> We may update, suspend, or discontinue features at any time. We are not liable for data loss.<br><br>
            <strong>8. Limitation of Liability:</strong> We are not liable for injuries, losses, or damages resulting from your use of the app.<br><br>
            <strong>9. Modifications to Terms:</strong> Continued use after changes means you accept the updated terms.<br><br>
            <strong>10. Contact:</strong> For any concerns, email support@wellnesstracker.gmail.com.
        `;
    } else if (type === 'privacy') {
        title = "Privacy Policy";
        content = `
            <strong>1. Information We Collect:</strong> We collect personal, health, and usage data to personalize your experience.<br><br>
            <strong>2. How We Use Your Information:</strong> Your data is used to track progress, generate analytics, and improve app performance.<br><br>
            <strong>3. Data Storage and Security:</strong> We store your data securely and take precautions to protect it.<br><br>
            <strong>4. Data Sharing:</strong> We never sell your data. You may choose to share activity data within the app.<br><br>
            <strong>5. User Control and Consent:</strong> You can modify or delete your data at any time through your profile.<br><br>
            <strong>6. Children’s Privacy:</strong> The app is not intended for users under 13. We do not collect data from children.<br><br>
            <strong>7. Changes to This Policy:</strong> We’ll inform you if we make important changes to our privacy practices.<br><br>
            <strong>8. Contact:</strong> Email privacy@wellnesstracker.gmail.com for any concerns.
        `;
    }

    document.getElementById("popup-title").innerText = title;
    document.getElementById("popup-content").innerHTML = content;
    document.getElementById("popup-modal").classList.remove("hidden");
    document.getElementById("modal-overlay").classList.remove("hidden");
};

window.closePopup = function () {
    document.getElementById("popup-modal").classList.add("hidden");
    document.getElementById("modal-overlay").classList.add("hidden");
};
