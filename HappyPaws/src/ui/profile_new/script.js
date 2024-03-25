const wrapper = document.querySelector(".right_col");
const breedLink = document.querySelector(".breed-link");
const dietLink = document.querySelector(".diet-link");
const photosLink = document.querySelector(".photos-link");
const scheduleLink = document.querySelector(".schedule-link");
const sections = document.querySelectorAll(".right_col .section");
var calendar;

breedLink.addEventListener("click", (ev) => {
    ev.preventDefault();
    sections.forEach((section) => {
        section.classList.remove("active");
    });
    document.querySelector(".breed").classList.add("active");
});

dietLink.addEventListener("click", (ev) => {
    ev.preventDefault();
    sections.forEach((section) => {
        section.classList.remove("active");
    });
    document.querySelector(".diet").classList.add("active");
});

photosLink.addEventListener("click", (ev) => {
    ev.preventDefault();
    sections.forEach((section) => {
        section.classList.remove("active");
    });
    document.querySelector(".photos").classList.add("active");
});

scheduleLink.addEventListener("click", (ev) => {
    ev.preventDefault();
    sections.forEach((section) => {
        section.classList.remove("active");
    });
    document.querySelector(".schedule").classList.add("active");
});

document.addEventListener("DOMContentLoaded", async function () {
    await initializeAutocomplete("Breed", "breedList");
    await toggleLoginLogoutButtons();
    await displayUserPet();
});

async function displayUserPet() {
    const token = localStorage.getItem("token");
    if (!token) {
        console.error("User is not logged in.");
        return;
    }
    const response = await fetch("http://localhost:8000/api/pets", {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

    if (!response.ok) {
        const errorMsg = await response.text();
        console.error(`Failed to fetch pets: ${errorMsg}`);
        return;
    }

    const pets = await response.json();
    if (pets.length > 0) {
        const pet = pets[0];

        const breed1Response = await fetch(`/api/breeds/${pet.breed_id1}`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        const breed1Name = await breed1Response.json();

        let breed2Name = { name: "" };
        if (pet.breed_id2) {
            const breed2Response = await fetch(`/api/breeds/${pet.breed_id2}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            breed2Name = await breed2Response.json();
        }

        document.getElementById("petName").textContent = pet.name;
        document.getElementById("petBreed1").textContent = breed1Name.name;
        document.getElementById("petBreed2").textContent = breed2Name.name;
        document
            .querySelector(".left_col .about")
            .querySelectorAll("li")[0].innerHTML = `<span>${pet.weight}</span> Pounds`;
        document
            .querySelector(".left_col .about")
            .querySelectorAll("li")[1].innerHTML = `<span>${pet.age}</span> Years old`;
        document.querySelector(".left_col .bio p").textContent = pet.bio;
    }
}

document
    .getElementById("calendarSection")
    .addEventListener("click", function () {
        initializeCalendar();
    });

document
    .getElementById("addPetLink")
    .addEventListener("click", function (event) {
        event.preventDefault();
        document.getElementById("addPetModal").style.display = "block";
    });

document
    .querySelector("#addPetModal .close")
    .addEventListener("click", function () {
        document.getElementById("addPetModal").style.display = "none";
    });

const today = new Date();
const todayStr = today.toISOString().split("T")[0];

const minDate = new Date(
    today.getFullYear() - 30,
    today.getMonth(),
    today.getDate(),
);
const minDateStr = minDate.toISOString().split("T")[0];

document.getElementById("Birthday").setAttribute("max", todayStr);
document.getElementById("Birthday").setAttribute("min", minDateStr);

document
    .getElementById("addPetForm")
    .addEventListener("submit", async function (event) {
        event.preventDefault();
        const token = localStorage.getItem("token");

        const name = document.getElementById("Name").value;
        const breed1 = document.getElementById("Breed").value;
        const breed2 = document.getElementById("Breed2").value;
        const weight = document.getElementById("Weight").value;
        const birthday = document.getElementById("Birthday").value;
        let age = null;
        const bio = document.getElementById("Bio").value;

        if (birthday) {
            age = today.getFullYear() - new Date(birthday).getFullYear();
        }

        const response = await fetch("http://localhost:8000/api/pets", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({ name, breed1, breed2, weight, birthday, age, bio }),
        });
        const result = await response.json();

        document.getElementById("addPetModal").style.display = "none";
    });

document.getElementById("Mixed").addEventListener("change", function () {
    var displayStyle = this.checked ? "block" : "none";
    document.getElementById("secondBreedContainer").style.display =
        displayStyle;

    if (this.checked) {
        initializeAutocomplete("Breed2", "breedList2");
    }
});


async function initializeAutocomplete(breedInputId, suggestionsContainerId) {
    var breedInput = document.getElementById(breedInputId);
    var suggestionsContainer = document.getElementById(suggestionsContainerId);

    breedInput.addEventListener("input", async function () {
        var inputValue = this.value;
        if (inputValue.length > 1) {
            fetch(`/api/breeds?search=${inputValue}`)
                .then((response) => response.json())
                .then((data) => {
                    console.log("data", data);
                    suggestionsContainer.innerHTML = "";
                    data.forEach((breed) => {
                        var suggestionItem = document.createElement("div");
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
        logoutButton.addEventListener("click", function () {
            localStorage.removeItem("token");
            window.location.href =
                "http://localhost:8000/Login_page/index.html";
        });
    } else {
        loginButton.style.display = "inline-block";
        logoutButton.style.display = "none";
    }
}

async function initializeCalendar() {
    const token = localStorage.getItem("token");
    if (!token) {
        console.error("User is not logged in.");
        return;
    }
    const response = await fetch("http://localhost:8000/api/reminders", {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

    if (!response.ok) {
        const errorMsg = await response.text();
        console.error(`Failed to fetch reminders: ${errorMsg}`);
        return;
    }

    const reminders = await response.json();
    const eventData = reminders.map((reminder) => {
        return {
            title: reminder.title,
            start: reminder.start,
            end: reminder.end,
        };
    });
    console.log(reminders);
    console.log(eventData);
    var calendarEl = document.getElementById("calendar");
    calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: "dayGridMonth",
        height: 650,
        schedulerLicenseKey: "CC-Attribution-NonCommercial-NoDerivatives",
        events: eventData,
    });
    await calendar.render();
}

document
    .getElementById("addReminderBtn")
    .addEventListener("click", function () {
        document.getElementById("reminderFormModal").style.display = "block";
    });

var span = document.querySelector("#reminderFormModal .close");

span.onclick = function () {
    document.getElementById("reminderFormModal").style.display = "none";
};

// Form Submission
document
    .getElementById("reminderForm")
    .addEventListener("submit", async function (event) {
        event.preventDefault();
        const token = localStorage.getItem("token");

        if (!token) {
            alert("You must be logged in to perform this action.");
            return;
        }

        const title = document.getElementById("title").value;
        const start = document.getElementById("start").value;
        let end = document.getElementById("end").value;

        let payload = { title, start };
        if (end) {
            payload.end = end;
        }

        const response = await fetch("http://localhost:8000/api/reminders", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            const errorMsg = await response.text();
            alert(`Failed to create reminder: ${errorMsg}`);
            return;
        }

        document.getElementById("reminderFormModal").style.display = "none";

        await initializeCalendar();
    });

document
    .getElementById("myPetsLink")
    .addEventListener("click", async function () {
        const dropdown = document.getElementById("petDropdown");

        const token = localStorage.getItem("token");
        if (token) {
            const response = await fetch("/api/pets", {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            if (response.ok) {
                const pets = await response.json();
                dropdown.innerHTML = "";
                pets.forEach((pet) => {
                    const petElement = document.createElement("div");
                    petElement.textContent = pet.name;
                    petElement.dataset.petId = pet.id;
                    dropdown.appendChild(petElement);
                });
            } else {
                console.error("Failed to fetch pets");
            }
        }
    });

document
    .getElementById("petDropdown")
    .addEventListener("click", async function (event) {
        let petId = event.target.dataset.petId;
        if (petId) {
            const token = localStorage.getItem("token");
            const response = await fetch(`/api/pets/${petId}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            if (response.ok) {
                const petDetails = await response.json();
                console.log(petDetails);

                const breed1Response = await fetch(`/api/breeds/${petDetails.breed_id1}`, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                const breed1Name = await breed1Response.json();

                let breed2Name = { name: "" };
                if (petDetails.breed_id2) {
                    const breed2Response = await fetch(`/api/breeds/${petDetails.breed_id2}`, {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    });
                    breed2Name = await breed2Response.json();
                }

                document.getElementById("petName").textContent =
                    petDetails.name;
                document.getElementById("petBreed1").textContent =
                    breed1Name.name;
                document.getElementById("petBreed2").textContent =
                    breed2Name.name;
                document
                    .querySelector(".left_col .about")
                    .querySelectorAll(
                        "li",
                    )[0].innerHTML = `<span>${petDetails.weight}</span> Pounds`;
                document
                    .querySelector(".left_col .about")
                    .querySelectorAll(
                        "li",
                    )[1].innerHTML = `<span>${petDetails.age}</span> Years old`;
                document.querySelector(".left_col .bio p").textContent =
                    petDetails.bio; 
            }
        }
    });
