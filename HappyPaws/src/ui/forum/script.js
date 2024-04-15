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

document
    .getElementById("addDiscussionModal")
    .addEventListener("click", async (event) => {
        if (event.target === this) {
            closeModal();
        }
    });

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
        const breed_id = document.getElementById("discussionBreed").value;
        const created_at = new Date().toISOString().replace("Z", "");
        console.log("discussion created at time", created_at);

        const payload = { title, content, breed_id, created_at };

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
    document
        .getElementById("createDiscussion")
        .addEventListener("click", openModal);
    document.querySelector(".close").addEventListener("click", closeModal);
    document
        .querySelector(".modal-content button")
        .addEventListener("click", submitDiscussion);
});
