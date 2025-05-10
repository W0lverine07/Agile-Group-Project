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

    // FLASH MESSAGE ALERT
    const flashElem = document.getElementById('flash-messages');
    if (flashElem) {
        const flashMessages = JSON.parse(flashElem.textContent || '[]');
        flashMessages.forEach(([category, message]) => {
        });
    }

    // TERMS/PRIVACY MODAL HANDLER (moved out of DOMContentLoaded)
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
        <strong>10. Contact:</strong> For any concerns, email support@wellnesstracker.example.com.`;
        }
       else if (type === 'privacy') {
    title = "Privacy Policy";
    content = `
        <strong>1. Information We Collect:</strong> We collect personal, health, and usage data to personalize your experience.<br><br>
        <strong>2. How We Use Your Information:</strong> Your data is used to track progress, generate analytics, and improve app performance.<br><br>
        <strong>3. Data Storage and Security:</strong> We store your data securely and take precautions to protect it.<br><br>
        <strong>4. Data Sharing:</strong> We never sell your data. You may choose to share activity data within the app.<br><br>
        <strong>5. User Control and Consent:</strong> You can modify or delete your data at any time through your profile.<br><br>
        <strong>6. Children’s Privacy:</strong> The app is not intended for users under 13. We do not collect data from children.<br><br>
        <strong>7. Changes to This Policy:</strong> We’ll inform you if we make important changes to our privacy practices.<br><br>
        <strong>8. Contact:</strong> Email privacy@wellnesstracker.example.com for any concerns.`;
        
        }
        document.getElementById("popup-title").innerText = title;
        document.getElementById("popup-content").innerHTML = content;
        document.getElementById("popup-modal").style.display = "block";
        document.getElementById("modal-overlay").style.display = "block";
    };

    window.closePopup = function() {
        document.getElementById("popup-modal").style.display = "none";
        document.getElementById("modal-overlay").style.display = "none";
    };

});


