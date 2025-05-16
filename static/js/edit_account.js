document.addEventListener("DOMContentLoaded", function () {
  const editBtn = document.getElementById("editBtn");
  const saveBtn = document.getElementById("saveBtn");
  const avatarModal = document.getElementById("avatarModal");
  const editAvatarIcon = document.getElementById("editAvatarIcon");
  const closeAvatarModal = document.getElementById("closeAvatarModal");
  const avatarPreview = document.getElementById("avatarPreview");

  const fields = [
    document.getElementById("weightInput"),
    document.getElementById("heightInput"),
    document.getElementById("allergiesInput"),
    document.getElementById("medicationsInput"),
  ];

  let selectedAvatar = avatarPreview.src;

  editBtn.addEventListener("click", () => {
    fields.forEach((field) => {
      field.removeAttribute("readonly");
      field.classList.add("editable");
    });

    editBtn.style.display = "none";
    saveBtn.style.display = "block";
    editAvatarIcon.style.display = "block";
  });

  editAvatarIcon.addEventListener("click", () => {
    avatarModal.style.display = "flex";
  });

  closeAvatarModal.addEventListener("click", () => {
    avatarModal.style.display = "none";
  });

  document
    .querySelectorAll('input[name="avatar_url"]')
    .forEach((radio) => {
      radio.addEventListener("change", () => {
        selectedAvatar = radio.value;
        avatarPreview.src = selectedAvatar;
        avatarModal.style.display = "none";
      });
    });

  saveBtn.addEventListener("click", () => {
    const payload = {
      weight: fields[0].value,
      height: fields[1].value,
      allergies: fields[2].value,
      medications: fields[3].value,
      avatar_url: selectedAvatar,
    };

// Inclusion of CSRF token for security

    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    fetch("/update_profile", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken
      },
      body: JSON.stringify(payload),
    })

//    fetch("/update_profile", {
//      method: "POST",
//      headers: { "Content-Type": "application/json" },
//      body: JSON.stringify(payload),
//    })

      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          alert("Profile updated!");
          location.reload();
        } else {
          alert("Error updating profile.");
        }
      });
  });
});
