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
    .getElementById("loginForm")
    .addEventListener("submit", async (event) => {
        event.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        try {
            const response = await fetch(
                "http://localhost:8000/api/users/token",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        username: email,
                        password,
                    }),
                },
            );

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log("Login successful", data);

            localStorage.setItem("token", data.access_token);

            window.location.href =
                "http://localhost:8000/Profile_new/index.html#";
        } catch (error) {
            console.error("Login failed:", error);
            alert("Login failed. Please check your credentials and try again.");
        }
    });

document
    .getElementById("signupForm")
    .addEventListener("submit", async (event) => {
        event.preventDefault();

        const email = document.getElementById("email2").value;
        const password = document.getElementById("password2").value;
        const retypePassword = document.getElementById("retypePassword").value;

        if (retypePassword !== password) {
            alert("Passwords do not match. Please retype your password.");
            return;
        }
        try {
            const response = await fetch("http://localhost:8000/api/users", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ email, password }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();

            alert("Registration successful! Please log in.");
            wrapper.classList.remove("active");
        } catch (error) {
            console.error("Registration failed:", error);
            alert("Registration failed. User already exists.");
        }
    });
