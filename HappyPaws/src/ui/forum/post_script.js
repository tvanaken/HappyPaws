/* eslint-disable camelcase */
/* eslint-disable prefer-const */
/* eslint-disable no-undef */
/* eslint-disable no-use-before-define */
document.addEventListener("DOMContentLoaded", async () => {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const postId = urlParams.get("postId");

    await toggleLoginLogoutButtons();
    await fetchPostDetails(postId);
});

/**
 * Displays a notification message on the UI.
 * 
 * @param {string} message - The message to be displayed in the notification.
 * @param {boolean} isError - Indicates whether the notification is an error message.
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
    }, 3000);
}

/**
 * Converts URLs and web addresses in the input text into clickable links.
 * 
 * @param {string} inputText - The text to be linkified.
 * @returns {string} - The linkified text.
 */
async function linkify(inputText) {
    let replacedText; let replacePattern1; let
        replacePattern2;
    replacePattern1 = /(\b(https?|ftp):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/gim;
    replacedText = inputText.replace(
        replacePattern1,
        '<a href="$1" style="color: blue" target="_blank">Link</a>',
    );
    replacePattern2 = /(^|[^\/])(www\.[\S]+(\b|$))/gim;
    replacedText = replacedText.replace(
        replacePattern2,
        '$1<a href="http://$2" style="color: blue" target="_blank">Link</a>',
    );

    return replacedText;
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
            window.location.href = "http://localhost:8000/Login_page/index.html";
        });
    } else {
        loginButton.style.display = "inline-block";
        logoutButton.style.display = "none";
    }
}

/**
 * Fetches post details and comments from the server.
 * 
 * @param {string} postId - The ID of the post to fetch details for.
 * @returns {Promise<void>} - A promise that resolves when the post details and comments are fetched successfully.
 * @throws {Error} - If there is an error fetching the post details or comments.
 */
async function fetchPostDetails(postId) {
    try {
        console.log(postId);
        const postResponse = await fetch(
            `http://localhost:8000/forum/posts/${postId}`,
            {
                headers: {
                    "Content-Type": "application/json",
                },
            },
        );
        const commentResponse = await fetch(
            `http://localhost:8000/forum/posts/${postId}/comments`,
            {
                headers: {
                    "Content-Type": "application/json",
                },
            },
        );

        if (!postResponse.ok || !commentResponse.ok) {
            throw new Error("Failed to fetch post details");
        }

        const post = await postResponse.json();
        const comments = await commentResponse.json();
        console.log(post);

        const postDiv = document.getElementById("post-container");

        postDiv.innerHTML = `
            <h3>${post.title}</h3>
            <p>${post.content}</p>
            <small>Breed: ${post.breed_name || "N/A"}</small>
        `;

        const commentsDiv = document.getElementById("comments-container");
        commentsDiv.innerHTML = "";
        comments.forEach((comment) => {
            const commentElement = document.createElement("div");
            commentElement.className = "comment";
            commentElement.innerHTML = `
                <p>${comment.content}</p>
                <small>${new Date(comment.created_at).toLocaleString()}</small>
            `;

            commentsDiv.appendChild(commentElement);
        });
    } catch (error) {
        console.error("Failed to fetch post details:", error);
    }
}


/**
 * Appends a comment to the comments container.
 * 
 * @param {Object} comment - The comment object to be appended.
 * @param {string} comment.content - The content of the comment.
 * @param {string} comment.created_at - The creation date of the comment.
 * @returns {void}
 */
async function appendComment(comment) {
    console.log(comment);
    const commentsDiv = document.getElementById("comments-container");
    const commentElement = document.createElement("div");
    commentElement.className = "comment";
    commentElement.innerHTML = `
        <p>${comment.content}</p>
        <small>${new Date(comment.created_at).toLocaleString()}</small>
    `;
    commentsDiv.appendChild(commentElement);
}

/**
 * Sends a POST request to create a new comment for a specific post in the forum.
 * @param {string} postId - The ID of the post to add the comment to.
 * @param {string} token - The authorization token for the request.
 * @param {object} payload - The payload containing the comment data.
 * @returns {Promise<Response>} - A Promise that resolves to the response of the request.
 */
document
    .getElementById("comment-form")
    .addEventListener("submit", async (event) => {
        event.preventDefault();

        const token = localStorage.getItem("token");
        if (!token) {
            alert("Please login to comment");
            return;
        }

        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const postId = urlParams.get("postId");

        const contentInput = document.getElementById("comment-text").value;
        const content = await linkify(contentInput);

        if (!content) {
            showNotification("Comment cannot be empty", true);
            return;
        }
        const created_at = new Date().toISOString().replace("Z", "");

        const payload = { content, created_at };

        const response = await fetch(
            `http://localhost:8000/forum/posts/${postId}/comments`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify(payload),
            },
        );
        if (response.ok) {
            const newComment = await response.json();
            document.getElementById("comment-text").value = "";
            showNotification("Comment added successfully", false);
            await appendComment(newComment);
        } else {
            showNotification("Failed to add comment", true);
        }
    });
