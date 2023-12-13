const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");
const loginForm = document.getElementById("signIn");
const signupForm = document.getElementById("signUp");
function validateForm() {
  var password = document.getElementById("signupPassword").value;
  var confirmPassword = document.getElementById("ConfirmPassword").value;

  if (password !== confirmPassword) {
    alert("Passwords do not match");
    return false;
  }
  return true;
}

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});
