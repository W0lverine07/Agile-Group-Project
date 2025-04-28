// Generate a random 6-character CAPTCHA string
function generateCaptcha() {
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let captcha = '';
  for (let i = 0; i < 6; i++) {
    captcha += characters.charAt(Math.floor(Math.random() * characters.length));
  }
  return captcha;
}

// Display the CAPTCHA in the .captcha-text element
function displayCaptcha() {
  const captchaText = generateCaptcha();
  document.getElementById('captcha-text').textContent = captchaText;
  return captchaText;
}

// Check if the CAPTCHA entered matches the displayed CAPTCHA
function validateCaptcha(captchaInput, correctCaptcha) {
  if (captchaInput === correctCaptcha) {
    return true;
  } else {
    alert('Captcha does not match. Please try again.');
    return false;
  }
}

// On page load, display a new CAPTCHA
window.onload = function() {
  const captchaText = displayCaptcha();

  // Handle form submission
  const form = document.querySelector('form');
  form.onsubmit = function(e) {
    const captchaInput = document.getElementById('captcha-input').value;

    if (!validateCaptcha(captchaInput, captchaText)) {
      e.preventDefault(); // Prevent form submission if CAPTCHA is incorrect
    }
  }
};

