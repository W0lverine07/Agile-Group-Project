// ===== Modal Animation Helpers =====
function animateOpen(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.remove("hidden", "fade-out");
    modal.classList.add("fade-in");
    document.getElementById("modal-overlay").classList.remove("hidden");
}

function animateClose(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.remove("fade-in");
    modal.classList.add("fade-out");

    setTimeout(() => {
        modal.classList.add("hidden");
        document.getElementById("modal-overlay").classList.add("hidden");
    }, 300); // match CSS animation duration
}

// ===== Forgot Password Entry Point =====
window.showForgotPassword = function () {
    animateOpen("forgot-modal");
};

// ===== Step 1: Verify Username & Email =====
window.verifyForgotDetails = function () {
    const username = document.getElementById("forgot-username").value.trim();
    const email = document.getElementById("forgot-email").value.trim();
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content'); // CSRF token for security


    if (!username || !email) {
        alert("Please enter both username and email.");
        return;
    }
    
    fetch("/verify_forgot", {
        method: "POST",
        headers: { "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken }, // include CSRF token

        body: JSON.stringify({ username, email })
    })
    .then(res => res.json())
    .then(data => {
        if (data.valid) {
            animateClose("forgot-modal");
            setTimeout(() => animateOpen("reset-modal"), 350);
        } else {
            alert("No matching user found.");
        }
    })
    .catch(() => alert("Error verifying user."));
};

// ===== Step 2: Reset Password =====
window.resetPassword = function () {
    const username = document.getElementById("forgot-username").value.trim();
    const password = document.getElementById("new-password").value.trim();
    const confirm = document.getElementById("confirm-password").value.trim();
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content'); // CSRF token for security

    if (password.length < 6) {
        alert("Password must be at least 6 characters.");
        return;
    }
    if (password !== confirm) {
        alert("Passwords do not match.");
        return;
    }

    fetch("/reset_password", {
        method: "POST",
        headers: { "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken }, // include CSRF token
        body: JSON.stringify({ username, password })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            alert("Password updated. You can now log in.");
            closePopup();
        } else {
            alert("Failed to update password.");
        }
    })
    .catch(() => alert("Error updating password."));
};

// ===== Close All Open Modals =====
window.closePopup = function () {
    document.querySelectorAll(".modal:not(.hidden)").forEach(modal => {
        animateClose(modal.id);
    });
};
