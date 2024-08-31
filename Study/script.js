document
    .getElementById("login-form")
    .addEventListener("submit", async (event) => {
        event.preventDefault();

        const email = document.getElementById("email").value.toLowerCase();
        const password = document.getElementById("password").value;

        try {
            const response = await fetch("", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    username: email,
                    password,
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
        } catch (error) {
            console.error();
        }
    });
