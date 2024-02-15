const wrapper = document.querySelector(".right_col");
const breedLink = document.querySelector(".breed-link");
const dietLink = document.querySelector(".diet-link");
const photosLink = document.querySelector(".photos-link");
const scheduleLink = document.querySelector(".schedule-link");
const sections = document.querySelectorAll(".right_col .section");

breedLink.addEventListener("click", () => {
    sections.forEach((section) => {
        section.classList.remove("active");
    });
    document.querySelector(".breed").classList.add("active");
});

dietLink.addEventListener("click", () => {
    sections.forEach((section) => {
        section.classList.remove("active");
    });
    document.querySelector(".diet").classList.add("active");
});

photosLink.addEventListener("click", () => {
    sections.forEach((section) => {
        section.classList.remove("active");
    });
    document.querySelector(".photos").classList.add("active");
});

scheduleLink.addEventListener("click", () => {
    sections.forEach((section) => {
        section.classList.remove("active");
    });
    document.querySelector(".schedule").classList.add("active");
});

var calendar;

async function initializeCalendar() {
    const response = await fetch("http://localhost:8000/api/reminders");
    const reminders = await response.json();
    const eventData = reminders.map((reminder) => {
        return {
            title: reminder.title,
            start: reminder.start,
            end: reminder.end,
            description: "Hello World",
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

var span = document.getElementsByClassName("close")[0];

span.onclick = function () {
    document.getElementById("reminderFormModal").style.display = "none";
};

// Form Submission
document
    .getElementById("reminderForm")
    .addEventListener("submit", async function (event) {
        event.preventDefault();

        const title = document.getElementById("title").value;
        const start = document.getElementById("start").value;
        const end = document.getElementById("end").value;

        const response = await fetch('http://localhost:8000/api/reminders', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ title, start, end }),
        });
        const result = await response.json();

        document.getElementById("reminderFormModal").style.display = "none";

        //await calendar.render();
    });