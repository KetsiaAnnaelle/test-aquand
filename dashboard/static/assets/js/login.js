document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("loginForm");
  const registerForm = document.getElementById("registerForm");
  const showRegister = document.getElementById("showRegister");
  const showLogin = document.getElementById("showLogin");

  // Switch vers inscription
  if (showRegister) {
    showRegister.addEventListener("click", (e) => {
      e.preventDefault();
      loginForm.style.display = "none";
      registerForm.style.display = "block";
      document.getElementById("form-title").textContent = "Créer votre compte";
    });
  }

  // Switch vers connexion
  if (showLogin) {
    showLogin.addEventListener("click", (e) => {
      e.preventDefault();
      loginForm.style.display = "block";
      registerForm.style.display = "none";
      document.getElementById("form-title").textContent = "Connectez-vous à votre espace";
    });
  }

  // Validation RegEx
  const validateEmail = (email) => /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email);


  // Connexion
  if (loginForm) {
    loginForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const email = document.getElementById("loginEmail").value.trim();
      const password = document.getElementById("loginPassword").value.trim();

      if (!validateEmail(email)) {
        alert("Adresse email invalide !");
        return;
      }

      if (password.length < 4) {
        alert("Le mot de passe doit contenir au moins 4 caractères.");
        return;
      }

      // Simule une session
      localStorage.setItem("user", email);
      alert("Connexion réussie !");
      window.location.href = "Annuaire.html"; // redirection après connexion
    });
  }

  // Inscription
  if (registerForm) {
  registerForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const name = document.getElementById("registerName").value.trim();
    const email = document.getElementById("registerEmail").value.trim();
    const password = document.getElementById("registerPassword").value.trim();

    if (!name || !validateEmail(email) || password.length < 6) {
      alert("Tous les champs doivent être valides (email + mot de passe ≥ 6 caractères).");
      return;
    }

    

    localStorage.setItem("user", email);
    alert("Compte créé avec succès !");
    window.location.href = "Annuaire.html";
  });
}

});
