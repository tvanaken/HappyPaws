const wrapper = document.querySelector(".wrapper");
const loginLink = document.querySelector(".login-link");
const registerLink = document.querySelector(".register-link");

registerLink.addEventListener("click", () => {
    wrapper.classList.add("active");
});

loginLink.addEventListener("click", () => {
    wrapper.classList.remove("active");
});

document
    .getElementById("signupForm")
    .addEventListener("submit", async function (event) {
        event.preventDefault();

        const email = document.getElementById("email2").value;
        const password = document.getElementById("password2").value;

        const response = await fetch("http://localhost:8000/api/users", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email: email, password: password }),
        });
        const result = await response.json();
    });
