const wrapper = document.querySelector(".right_col");
const breedLink = document.querySelector(".breed-link");
const dietLink = document.querySelector(".diet-link");
const photosLink = document.querySelector(".photos-link");
const scheduleLink = document.querySelector(".schedule-link");
const sections = document.querySelectorAll(".right_col .section");

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

        const name = document.getElementById("Name").value;
        const breed = document.getElementById("Breed").value;
        const weight = document.getElementById("Weight").value;
        const birthday = document.getElementById("Birthday").value;

        const response = await fetch("http://localhost:8000/api/pets", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ name, breed, weight, birthday }),
        });
        const result = await response.json();

        document.getElementById("addPetModal").style.display = "none";
    });

document.addEventListener("DOMContentLoaded", async function () {

    function initializeAutocomplete(breedInputId, suggestionsContainerId) {

        var breedInput = document.getElementById(breedInputId);
        var suggestionsContainer = document.getElementById(suggestionsContainerId);

        breedInput.addEventListener("input", async function () {
            var inputValue = this.value;
            if (inputValue.length > 1) {
                fetch(`/api/breeds?search=${inputValue}`)
                    .then(response => response.json())
                    .then(data => {
                        console.log('data', data);
                        suggestionsContainer.innerHTML = '';
                        data.forEach(breed => {
                            var suggestionItem = document.createElement('div');
                            suggestionItem.innerHTML = breed.name; // Assuming breed.to_dict() includes a 'name' field
                            suggestionItem.addEventListener('click', function() {
                                breedInput.value = this.textContent;
                                suggestionsContainer.innerHTML = '';
                            });
                            suggestionsContainer.appendChild(suggestionItem);
                        });
                    })
                    .catch(error => console.log('error', error));
            } else {
                suggestionsContainer.innerHTML = '';
            }
        });
    }

    // Initialize autocomplete for the first breed input
    initializeAutocomplete("Breed", "breedList");

    // Handle "Mixed" checkbox changes
    document.getElementById("Mixed").addEventListener("change", function () {
        var displayStyle = this.checked ? "block" : "none";
        document.getElementById("secondBreedContainer").style.display = displayStyle;

        // Initialize autocomplete for the second breed input if "Mixed" is checked
        if (this.checked) {
            initializeAutocomplete("Breed2", "breedList2");
        }
    });
    toggleLoginLogoutButtons();
});

function toggleLoginLogoutButtons() {

    const token = localStorage.getItem("token");
    const loginButton = document.getElementById("loginButton");
    const logoutButton = document.getElementById("logoutButton");

    if (token) {
        loginButton.style.display = "none";
        logoutButton.style.display = "block";
        logoutButton.addEventListener("click", function () {
            localStorage.removeItem("token");
            window.location.href = "http://localhost:8000/Login_page/index.html"
        });
    } else {
        loginButton.style.display = "block";
        logoutButton.style.display = "none";
    }
}

var calendar;

async function initializeCalendar() {
    const response = await fetch("http://localhost:8000/api/reminders");
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
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: "dayGridMonth",
        height: 650,
        schedulerLicenseKey: "CC-Attribution-NonCommercial-NoDerivatives",
        events: eventData,
    });
    calendar.render();
}

// Calendar scripts
document.addEventListener("DOMContentLoaded", initializeCalendar);

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

        console.log("Script running...");

        const token = localStorage.getItem("token");
        if (!token) {
            alert("You must be logged in to perform this action.");
            return;
        }

        console.log("Token found...");
        console.log(token);

        const title = document.getElementById("title").value;
        const start = document.getElementById("start").value;
        const end = document.getElementById("end").value;

        const response = await fetch("http://localhost:8000/api/reminders", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({ title, start, end }),
        });

        console.log("Response received...");
        console.log(response);

        if (!response.ok) {
            const errorMsg = await response.text();
            alert(`Failed to create reminder: ${errorMsg}`);
            return;
        }

        const result = await response.json();
        console.log(result);

        document.getElementById("reminderFormModal").style.display = "none";

        //await calendar.render();
    });
