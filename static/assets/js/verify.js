const inputs = document.querySelectorAll(".otp-card-inputs input");
const button = document.querySelector(".otp-card button");

// function validateForm() {
//   var password = document.getElementById("signupPassword").value;
//   var confirmPassword = document.getElementById("ConfirmPassword").value;

//   if (str(password) !== str(confirmPassword)) {
//     alert("Passwords do not match");
//     return false;
//   }
//   return true;
// }

inputs.forEach((input) => {
  let LastInputStatus = 0;
  input.onkeyup = (e) => {
    const CurrentElement = e.target;
    const NextElement = input.nextElementSibling;
    const PrevElement = input.previousElementSibling;

    if (PrevElement && e.keyCode === 8) {
      if (LastInputStatus === 1) {
        PrevElement.value = "";
        PrevElement.focus();
      }
      button.setAttribute("disabled", true);
      LastInputStatus = 1;
    } else {
      const reg = /^\d+$/;
      if (!reg.test(CurrentElement.value)) {
        CurrentElement.value = CurrentElement.value.replace(/\D/g, "");
      } else if (CurrentElement.value) {
        if (NextElement) {
          NextElement.focus();
        } else {
          button.removeAttribute("disabled");
          LastInputStatus = 0;
        }
      }
    }
  };
});
