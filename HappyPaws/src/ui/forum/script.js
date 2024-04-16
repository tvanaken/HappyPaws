async function initializeAutocomplete(breedInputId, suggestionsContainerId) {
    const breedInput = document.getElementById(breedInputId);
    const suggestionsContainer = document.getElementById(
        suggestionsContainerId,
    );

    breedInput.addEventListener("input", async function () {
        const inputValue = this.value;
        if (inputValue.length > 1) {
            fetch(`/api/breeds?search=${inputValue}`)
                .then((response) => response.json())
                .then((data) => {
                    console.log("data", data);
                    suggestionsContainer.innerHTML = "";
                    data.forEach((breed) => {
                        const suggestionItem = document.createElement("div");
                        suggestionItem.innerHTML = breed.name;
                        suggestionItem.addEventListener("click", function () {
                            breedInput.value = this.textContent;
                            suggestionsContainer.innerHTML = "";
                        });
                        suggestionsContainer.appendChild(suggestionItem);
                    });
                })
                .catch((error) => console.log("error", error));
        } else {
            suggestionsContainer.innerHTML = "";
        }
    });
}

async function toggleLoginLogoutButtons() {
    const token = localStorage.getItem("token");
    const loginButton = document.getElementById("loginButton");
    const logoutButton = document.getElementById("logoutButton");

    if (token) {
        loginButton.style.display = "none";
        logoutButton.style.display = "inline-block";
        logoutButton.addEventListener("click", () => {
            localStorage.removeItem("token");
            window.location.href =
                "http://localhost:8000/Login_page/index.html";
        });
    } else {
        loginButton.style.display = "inline-block";
        logoutButton.style.display = "none";
    }
}

async function fetchAndDisplayPosts() {
    try {
        const response = await fetch("http://localhost:8000/forum/posts", {
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${localStorage.getItem("token")}`, // Include this if your endpoint requires authentication
            },
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const posts = await response.json();

        const discussionsElement = document.getElementById("discussions");
        discussionsElement.innerHTML = "";

        posts.forEach((post) => {
            const postElement = document.createElement("div");

            postElement.className = "post";
            postElement.innerHTML = `
                <h3>${post.title}</h3><br>
                <p>${post.content}</p><br>
                <small>Breed: ${post.breed_name || "N/A"}</small>`;

            postElement.addEventListener("click", () => {
                window.location.href = `http://localhost:8000/forum/post.html?postId=${post.id}`;
            });

            discussionsElement.appendChild(postElement);
        });
    } catch (error) {
        console.error("Failed to fetch posts:", error);
    }
}

document
    .getElementById("discussionForm")
    .addEventListener("submit", async (event) => {
        event.preventDefault();
        const token = localStorage.getItem("token");

        if (!token) {
            alert("You must be logged in to create a discussion.");
            return;
        }

        const title = document.getElementById("discussionTitle").value;
        const content = document.getElementById("discussionContent").value;
        const breed_name = document.getElementById("discussionBreed").value;
        const created_at = new Date().toISOString().replace("Z", "");
        console.log("discussion created at time", created_at);

        const payload = { title, content, breed_name, created_at };

        const response = await fetch("http://localhost:8000/forum/posts", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify(payload),
        });

        if (response.ok) {
            closeModal();
            await fetchAndDisplayPosts();
            alert("Discussion created successfully!");
        } else {
            alert("Failed to create discussion.");
        }
    });

function openModal() {
    const modal = document.getElementById("addDiscussionModal");
    modal.style.display = "block";
}

function closeModal() {
    const modal = document.getElementById("addDiscussionModal");
    modal.style.display = "none";
}

document.addEventListener("DOMContentLoaded", async function () {
    await initializeAutocomplete("Breed", "breedList");
    await initializeAutocomplete("discussionBreed", "discussionBreedList");
    await toggleLoginLogoutButtons();
    await fetchAndDisplayPosts();
    document.querySelector(".close").addEventListener("click", closeModal);
});
