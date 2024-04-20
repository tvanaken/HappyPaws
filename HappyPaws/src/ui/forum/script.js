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
                Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const posts = await response.json();

        const discussionsElement = document.getElementById("discussions");
        discussionsElement.innerHTML = "";

        posts.forEach(async (post) => {
            const userResponse = await fetch(`http://localhost:8000/api/users/${post.user_id}`, {
                headers: {
                    "Content-Type": "application/json",
                },
            });

            let username = await userResponse.json();
            username = username.email.split("@")[0];
            const postElement = document.createElement("div");

            postElement.className = "post";
            postElement.innerHTML = `
                <h3>${post.title}</h3><br>
                <p>${post.content}</p><br>
                <small>Breed: ${post.breed_name || "N/A"}</small><br>
                <small style="text-align: right;", "align-self: right;">Posted by: ${username}</small>`;

            postElement.addEventListener("click", () => {
                window.location.href = `http://localhost:8000/forum/post.html?postId=${post.id}`;
            });

            discussionsElement.appendChild(postElement);
        });
    } catch (error) {
        console.error("Failed to fetch posts:", error);
    }
}

function displayPosts(posts) {

    const discussionsElement = document.getElementById("discussions");
    discussionsElement.innerHTML = "";

    posts.forEach(async (post) => {
        const userResponse = await fetch(`http://localhost:8000/api/users/${post.user_id}`, {
            headers: {
                "Content-Type": "application/json",
            },
        });

        let username = await userResponse.json();
        username = username.email.split("@")[0];
        const postElement = document.createElement("div");

        postElement.className = "post";
        postElement.innerHTML = `
        <h3>${post.title}</h3><br>
        <p>${post.content}</p><br>
        <small>Breed: ${post.breed_name || "N/A"}</small><br>
        <small style="text-align: right;", "align-self: right;">Posted by: ${username}</small>`;

        postElement.addEventListener("click", () => {
            window.location.href = `http://localhost:8000/forum/post.html?postId=${post.id}`;
        });

        discussionsElement.appendChild(postElement);    
    });
}

async function searchPosts() {
    const breedInput = document.getElementById("Breed").value;
    const searchInput = document.getElementById("search-input").value;

    const url = new URL("http://localhost:8000/forum/posts/filtered");
    if (breedInput) url.searchParams.append("breed_name", breedInput);
    if (searchInput) url.searchParams.append("search", searchInput);

    try {

        const response = await fetch(url);

        if (!response.ok) 
            throw new Error("Failed to fetch discussions");

        const discussions = await response.json();
        displayPosts(discussions);

    } catch (error) {
        console.error("Error fetching discussions:", error);
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
