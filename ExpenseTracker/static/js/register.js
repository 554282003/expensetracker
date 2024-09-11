const usernamefield = document.querySelector("#usernamefield");
const emailfield = document.querySelector("#emailfield");
const invalidfeedbackArea = document.querySelector(".invalid-feedback");
const emailfeedbackarea = document.querySelector(".emailfeedbackarea");
const showpasswordtoggle = document.querySelector(".showpasswordtoggle");
const passwordfield = document.querySelector("#passwordfield");
const submitbtn = document.querySelector(".submit-btn");
let usernameError = false;
let emailError = false;

const checkFormValidity = () => {
  if (usernameError || emailError) {
    submitbtn.disabled = true;
  } else {
    submitbtn.disabled = false;
  }
};

usernamefield.addEventListener("keyup", (e) => {
  const usernameVal = e.target.value;
  usernamefield.classList.remove("is-invalid");
  invalidfeedbackArea.style.display = "none";

  if (usernameVal.length > 0) {
    fetch("/authentication/user-validation/", {
      body: JSON.stringify({ username: usernameVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.username_error) {
          usernamefield.classList.add("is-invalid");
          invalidfeedbackArea.style.display = "block";
          invalidfeedbackArea.innerHTML = `<p>${data.username_error}</p>`;
          usernameError = true;
        } else {
          usernameError = false;
        }
        checkFormValidity();
      });
  } else {
    usernameError = false;
    checkFormValidity();
  }
});

if (emailfield != null) {
  emailfield.addEventListener("keyup", (e) => {
    const emailVal = e.target.value;
    emailfield.classList.remove("is-invalid");
    emailfeedbackarea.style.display = "none";

    if (emailVal.length > 0) {
      fetch("/authentication/email-validation/", {
        body: JSON.stringify({ email: emailVal }),
        method: "POST",
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.email_error) {
            emailfield.classList.add("is-invalid");
            emailfeedbackarea.style.display = "block";
            emailfeedbackarea.innerHTML = `<p>${data.email_error}</p>`;
            emailError = true;
          } else {
            emailError = false;
          }
          checkFormValidity();
        });
    } else {
      emailError = false;
      checkFormValidity();
    }
  });
}

const handletoggle = () => {
  console.log("click");
  if (showpasswordtoggle.textContent === "SHOW") {
    showpasswordtoggle.textContent = "HIDE";
    passwordfield.type = "text";
  } else {
    showpasswordtoggle.textContent = "SHOW";
    passwordfield.type = "password";
  }
};
showpasswordtoggle.addEventListener("click", handletoggle);
