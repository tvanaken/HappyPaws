let breeds = [];
/**
 * Preloads the breeds data if it is not already loaded.
 * @returns {Promise<void>} A promise that resolves when the breeds data is loaded.
 */
async function preloadBreeds() {
    if (breeds.length === 0) {
        try {
            const response = await fetch("/api/breeds");
            if (response.ok) {
                breeds = await response.json();
            } else {
                throw new Error("Failed to fetch breeds");
            }
        } catch (error) {
            console.error("Error fetching breeds:", error);
        }
    }
}

/**
 * Filters the breeds based on the given input value.
 * 
 * @param {string} inputValue - The input value to filter the breeds.
 * @returns {void}
 */
function filterBreeds(inputValue) {
    const filteredBreeds = breeds.filter((breed) =>
        breed.name.toLowerCase().includes(inputValue.toLowerCase()),
    );
    displaySuggestions(filteredBreeds);
}


/**
 * Displays suggestions for breeds.
 * 
 * @param {Array<Object>} breeds - An array of breed objects.
 * @returns {void}
 */
function displaySuggestions(breeds) {
    const suggestionsContainer = document.getElementById("breedList");
    suggestionsContainer.innerHTML = "";

    breeds.forEach((breed) => {
        const suggestionItem = document.createElement("div");
        suggestionItem.textContent = breed.name;
        suggestionItem.addEventListener("click", () => {
            document.getElementById("Breed").value = breed.name;
            suggestionsContainer.innerHTML = "";
        });
        suggestionsContainer.appendChild(suggestionItem);
    });
}


document.getElementById("Breed").addEventListener("focus", () => {
    preloadBreeds();
    displaySuggestions(breeds);
});

document.getElementById("Breed").addEventListener("input", (event) => {
    const inputValue = event.target.value;
    if (inputValue.length > 0) {
        filterBreeds(inputValue);
    } else {
        displaySuggestions(breeds);
    }
});

document.getElementById("Breed").addEventListener("blur", () => {
    setTimeout(() => {
        document.getElementById("breedList").innerHTML = "";
    }, 200);
});

document.getElementById("discussionBreed").addEventListener("focus", () => {
    preloadBreeds();
    displaySuggestions(breeds);
});

document
    .getElementById("discussionBreed")
    .addEventListener("input", (event) => {
        const inputValue = event.target.value;
        if (inputValue.length > 0) {
            filterBreeds(inputValue);
        } else {
            displaySuggestions(breeds);
        }
    });

document.getElementById("discussionBreed").addEventListener("blur", () => {
    setTimeout(() => {
        document.getElementById("breedList").innerHTML = "";
    }, 200);
});

/**
 * Displays a notification message.
 * 
 * @param {string} message - The message to be displayed in the notification.
 * @param {boolean} isError - Indicates whether the notification is an error or not.
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
 * Toggles the display of login and logout buttons based on the presence of a token in the local storage.
 * @async
 * @function toggleLoginLogoutButtons
 * @returns {void}
 */
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


/**
 * Fetches user posts from the server and displays them on the UI.
 * @async
 * @function fetchAndDisplayPosts
 * @throws {Error} If there is an HTTP error during the fetch request.
 * @returns {Promise<void>} A promise that resolves when the posts are fetched and displayed.
 */
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
            const userResponse = await fetch(
                `http://localhost:8000/api/users/${post.user_id}`,
                {
                    headers: {
                        "Content-Type": "application/json",
                    },
                },
            );

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

/**
 * Displays posts on the UI.
 * 
 * @param {Array} posts - An array of post objects.
 * @returns {void}
 */
function displayPosts(posts) {
    const discussionsElement = document.getElementById("discussions");
    discussionsElement.innerHTML = "";

    posts.forEach(async (post) => {
        const userResponse = await fetch(
            `http://localhost:8000/api/users/${post.user_id}`,
            {
                headers: {
                    "Content-Type": "application/json",
                },
            },
        );

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

/**
 * Searches for posts based on breed and search input.
 * @async
 * @function searchPosts
 * @returns {Promise<void>} - A promise that resolves when the posts are displayed.
 * @throws {Error} - If there is an error fetching discussions.
 */
async function searchPosts() {
    const breedInput = document.getElementById("Breed").value;
    const searchInput = document.getElementById("search-input").value;

    const url = new URL("http://localhost:8000/forum/posts/filtered");
    if (breedInput) url.searchParams.append("breed_name", breedInput);
    if (searchInput) url.searchParams.append("search", searchInput);

    try {
        const response = await fetch(url);

        if (!response.ok) throw new Error("Failed to fetch discussions");

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
            console.log("Discussion created successfully");
            title.value = "";
            content.value = "";
            breed_name.value = "";
            showNotification("Discussion created successfully", false);
            closeModal();
            await fetchAndDisplayPosts();
        } else {
            showNotification("Failed to create discussion", true);
        }
    });

/**
 * Opens the modal for adding a discussion.
 */
function openModal() {
    const modal = document.getElementById("addDiscussionModal");
    modal.style.display = "block";
}

/**
 * Closes the modal by setting its display property to "none".
 */
function closeModal() {
    const modal = document.getElementById("addDiscussionModal");
    modal.style.display = "none";
}

document.addEventListener("DOMContentLoaded", async function () {
    // await initializeAutocomplete("Breed", "breedList");
    // await initializeAutocomplete("discussionBreed", "discussionBreedList");
    await preloadBreeds();
    await toggleLoginLogoutButtons();
    await fetchAndDisplayPosts();
    document.querySelector(".close").addEventListener("click", closeModal);
});
