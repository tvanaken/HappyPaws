const wrapper = document.querySelector(".right_col");
const breedLink = document.querySelector(".breed-link");
const dietLink = document.querySelector(".diet-link");
const photosLink = document.querySelector(".photos-link");
const scheduleLink = document.querySelector(".schedule-link");
const sections = document.querySelectorAll(".right_col .section");

breedLink.addEventListener("click", () => {
    sections.forEach(section => {
        section.classList.remove('active');
    });
    document.querySelector(".breed").classList.add('active');
});

dietLink.addEventListener("click", () => {
    sections.forEach(section => {
        section.classList.remove('active');
    });
    document.querySelector(".diet").classList.add('active');
});

photosLink.addEventListener("click", () => {
    sections.forEach(section => {
        section.classList.remove('active');
    });
    document.querySelector(".photos").classList.add('active');
});

scheduleLink.addEventListener("click", () => {
    sections.forEach(section => {
        section.classList.remove('active');
    });
    document.querySelector(".schedule").classList.add('active');
});