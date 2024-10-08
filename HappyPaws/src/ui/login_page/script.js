/* eslint-disable no-undef */
/**
 * Switches the view between the login/sign-up forms
 * @param {Event} event - The click event
 */
const wrapper = document.querySelector(".wrapper");
const loginLink = document.querySelector(".login-link");
const registerLink = document.querySelector(".register-link");

registerLink.addEventListener("click", () => {
    wrapper.classList.add("active");
});
loginLink.addEventListener("click", () => {
    wrapper.classList.remove("active");
});


/**
 * Displays a notification message on the page.
 * 
 * @param {string} message - The message to be displayed in the notification.
 * @param {boolean} isError - Indicates whether the notification is an error message or not.
 * @returns {void}
 */
function showNotification(message, isError) {
    const notification = document.getElementById("notification");
    notification.textContent = message;
    notification.classList.add("active");
    if (isError) {
        notification.classList.add("error");
    } else {
        notification.classList.remove("error");
    }

    setTimeout(() => {
        notification.classList.remove("active");
    }, 5000);
}

/**
 * Sends a POST request to the server to obtain a token for the given user credentials.
 * 
 * @param {string} email - The email address of the user.
 * @param {string} password - The password of the user.
 * @returns {Promise<Response>} - A promise that resolves to the response from the server.
 */
document
    .getElementById("loginForm")
    .addEventListener("submit", async (event) => {
        event.preventDefault();

        const email = document.getElementById("email").value.toLowerCase();
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
            localStorage.setItem("token", data.access_token);

            window.location.href =
                "http://localhost:8000/Profile_new/index.html#";
        } catch (error) {
            console.error("Login failed:", error);
            showNotification("Login failed. Please try again.", true);
        }
    });

/**
 * Sends a POST request to the specified API endpoint with the provided email and password.
 * 
 * @param {string} email - The email of the user.
 * @param {string} password - The password of the user.
 * @returns {Promise<Response>} - A promise that resolves to the response of the request.
 */
document
    .getElementById("signupForm")
    .addEventListener("submit", async (event) => {
        event.preventDefault();

        const email = document.getElementById("email2").value.toLowerCase();
        const password = document.getElementById("password2").value;
        const retypePassword = document.getElementById("retypePassword").value;

        if (retypePassword !== password) {
            showNotification("Passwords do not match. Please try again.", true);
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

            showNotification("Registration successful! Please log in.", false);
            wrapper.classList.remove("active");
        } catch (error) {
            console.error("Registration failed:", error);
            showNotification("Registration failed. User already exists.", true);
        }
    });
