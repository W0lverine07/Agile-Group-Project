document.addEventListener("DOMContentLoaded", function() {
  const editBtn = document.getElementById("editBtn");
  const saveBtn = document.getElementById("saveBtn");

  const fields = [
    document.getElementById("weightInput"),
    document.getElementById("heightInput"),
    document.getElementById("allergiesInput"),
    document.getElementById("medicationsInput")
  ];

  editBtn.addEventListener("click", () => {
  fields.forEach(field => {
    field.removeAttribute("readonly");
    field.classList.add("editable");  // Highlight editable fields
  });
  editBtn.style.display = "none";
  saveBtn.style.display = "block";
});

saveBtn.addEventListener("click", () => {
  const payload = {
    weight: fields[0].value,
    height: fields[1].value,
    allergies: fields[2].value,
    medications: fields[3].value
  };

  fetch("/update_profile", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      alert("Profile updated!");
      location.reload();
    } else {
      alert("Error updating profile.");
    }
  });
});
});