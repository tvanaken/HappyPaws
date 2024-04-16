document.addEventListener("DOMContentLoaded", async () => {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const postId = urlParams.get("postId");

    await toggleLoginLogoutButtons();
    await fetchPostDetails(postId);
});

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

async function fetchPostDetails(postId) {
    try {
        const response = await fetch(
            `http://localhost:8000/forum/posts/${postId}`,
            {
                headers: {
                    "Content-Type": "application/json",
                },
            },
        );
        if (!response.ok) {
            throw new Error("Failed to fetch post details");
        }

        const post = await response.json();

        const postDiv = document.getElementById("post-container");

        postDiv.innerHTML = `
            <h3>${post.title}</h3>
            <p>${post.content}</p>
            <small>Breed: ${post.breed_name || "N/A"}</small>
        `;

        const commentsDiv = document.getElementById("comments-container");
        commentsDiv.innerHTML = "";
        post.comments.forEach((comment) => {
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

async function appendComment(comment) {
    const commentsDiv = document.getElementById("comments-container");
    const commentElement = document.createElement("div");
    commentElement.className = "comment";
    commentElement.innerHTML = `
        <p>${comment.content}</p>
        <small>${new Date(comment.created_at).toLocaleString()}</small>
    `;
    commentsDiv.appendChild(commentElement);
}

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

        const content = document.getElementById("comment-text").value;
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
        if (!response.ok) {
            alert("Failed to add comment");
            return;
        } else {
            const newComment = await response.json();
            await appendComment(newComment);
        }
    });
