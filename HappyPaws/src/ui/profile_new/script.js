const wrapper = document.querySelector(".right_col");
const breedLink = document.querySelector(".breed-link");
const dietLink = document.querySelector(".diet-link");
const healthLink = document.querySelector(".health-link");
const groomingLink = document.querySelector(".grooming-link");
const scheduleLink = document.querySelector(".schedule-link");
const sections = document.querySelectorAll(".right_col .section");

let calendar;
const today = new Date();
const todayStr = today.toISOString().split("T")[0];
const minDate = new Date(
    today.getFullYear() - 30,
    today.getMonth(),
    today.getDate(),
);
const minDateStr = minDate.toISOString().split("T")[0];

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

healthLink.addEventListener("click", (ev) => {
    ev.preventDefault();
    sections.forEach((section) => {
        section.classList.remove("active");
    });
    document.querySelector(".health").classList.add("active");
});

groomingLink.addEventListener("click", (ev) => {
    ev.preventDefault();
    sections.forEach((section) => {
        section.classList.remove("active");
    });
    document.querySelector(".grooming").classList.add("active");
});

scheduleLink.addEventListener("click", (ev) => {
    ev.preventDefault();
    sections.forEach((section) => {
        section.classList.remove("active");
    });
    document.querySelector(".schedule").classList.add("active");
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
        const petDetails = pets[0];

        const breed1Response = await fetch(
            `/api/breeds/${petDetails.breed_id1}`,
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            },
        );
        const breed1 = await breed1Response.json();

        document
            .getElementById("breedDescription")
            .querySelector("h2").textContent = breed1.name;
        document
            .getElementById("breedDescription")
            .querySelector("p").textContent = breed1.breed_description;
        document
            .getElementById("healthDescription")
            .querySelector("h2").textContent = "Health (" + breed1.name + ")";
        document
            .getElementById("healthDescription")
            .querySelector("p").textContent = breed1.health_description;
        document
            .getElementById("groomingDescription")
            .querySelector("h2").textContent = "Grooming (" + breed1.name + ")";
        document
            .getElementById("groomingDescription")
            .querySelector("p").textContent = breed1.groom_description;

        let breed2 = { name: "" };
        if (petDetails.breed_id2) {
            const breed2Response = await fetch(
                `/api/breeds/${petDetails.breed_id2}`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                },
            );
            breed2 = await breed2Response.json();

            if (breed2Response.ok) {
                if (!secondBreedName || !secondBreedDescription) {
                    const breedDescriptionSection =
                        document.getElementById("breedDescription");
                    const breedHealthSection =
                        document.getElementById("healthDescription");
                    const breedGroomingSection = document.getElementById(
                        "groomingDescription",
                    );

                    secondBreedName = document.createElement("h2");
                    secondBreedNameHealth = document.createElement("h2");
                    secondBreedNameGroom = document.createElement("h2");
                    secondBreedDescription = document.createElement("p");
                    secondHealthDescription = document.createElement("p");
                    secondGroomDescription = document.createElement("p");

                    secondBreedName.setAttribute("id", "secondBreedName");
                    secondBreedNameHealth.setAttribute(
                        "id",
                        "secondBreedNameHealth",
                    );
                    secondBreedNameGroom.setAttribute(
                        "id",
                        "secondBreedNameGroom",
                    );
                    secondBreedDescription.setAttribute(
                        "id",
                        "secondBreedDescription",
                    );
                    secondHealthDescription.setAttribute(
                        "id",
                        "secondHealthDescription",
                    );
                    secondGroomDescription.setAttribute(
                        "id",
                        "secondGroomDescription",
                    );

                    breedDescriptionSection.appendChild(secondBreedName);
                    breedDescriptionSection.appendChild(secondBreedDescription);
                    breedHealthSection.appendChild(secondBreedNameHealth);
                    breedHealthSection.appendChild(secondHealthDescription);
                    breedGroomingSection.appendChild(secondBreedNameGroom);
                    breedGroomingSection.appendChild(secondGroomDescription);
                }

                secondBreedName.style.display = "";
                secondBreedNameHealth.style.display = "";
                secondBreedNameGroom.style.display = "";
                secondBreedDescription.style.display = "";
                secondHealthDescription.style.display = "";
                secondGroomDescription.style.display = "";
                secondBreedName.textContent = breed2.name;
                secondBreedNameHealth.textContent =
                    "Health (" + breed2.name + ")";
                secondBreedNameGroom.textContent =
                    "Grooming (" + breed2.name + ")";
                secondBreedDescription.textContent = breed2.breed_description;
                secondHealthDescription.textContent = breed2.health_description;
                secondGroomDescription.textContent = breed2.groom_description;
            }
        } else if (secondBreedName && secondBreedDescription) {
            secondBreedName.style.display = "none";
            secondBreedNameHealth.style.display = "none";
            secondBreedNameGroom.style.display = "none";
            secondBreedDescription.style.display = "none";
            secondHealthDescription.style.display = "none";
            secondGroomDescription.style.display = "none";
            secondBreedName.textContent = "";
            secondBreedNameHealth.textContent = "";
            secondBreedNameGroom.textContent = "";
            secondBreedDescription.textContent = "";
            secondHealthDescription.textContent = "";
            secondGroomDescription.textContent = "";
            document.getElementById("petBreed2").textContent = "";
        }

        document.getElementById("petName").textContent = petDetails.name;
        document.getElementById("petBreed1").textContent = breed1.name;
        document.getElementById("petBreed2").textContent = breed2.name;
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
        document.querySelector(".left_col .bio p").textContent = petDetails.bio;
    }
}

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
    const eventData = reminders.map((reminder) => ({
        title: reminder.title,
        start: reminder.start,
        end: reminder.end,
    }));
    console.log(reminders);
    console.log(eventData);
    const calendarEl = document.getElementById("calendar");
    calendar = new FullCalendar.Calendar(calendarEl, {
        customButtons: {
            addReminder: {
                text: "Add Reminder",
                click: function () {
                    document.getElementById("reminderFormModal").style.display =
                        "block";
                },
            },
        },
        headerToolbar: {
            left: "prev,next today addReminder",
            center: "title",
            right: "dayGridMonth,timeGridWeek,timeGridDay",
        },
        initialView: "dayGridMonth",
        height: 650,
        schedulerLicenseKey: "CC-Attribution-NonCommercial-NoDerivatives",
        events: eventData,
    });
    await calendar.render();
}

async function getPresignedUrl(fileName) {
    const token = localStorage.getItem("token");
    const response = await fetch(
        "http://localhost:8000/api/s3PresignedUrl?fileName=${fileName}",
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        },
    );
    if (!response.ok) {
        throw new Error("Failed to fetch pre-signed URL");
    }
    return response.json();
}

async function uploadImageToS3(file, presignedUrl) {
    const response = await fetch(presignedUrl, {
        method: "PUT",
        headers: {
            "Content-Type": "image/jpeg",
        },
        body: file,
    });
    if (!response.ok) {
        throw new Error("Failed to upload image to S3");
    }
}

document.getElementById("calendarSection").addEventListener("click", () => {
    initializeCalendar();
});

document.getElementById("addPetLink").addEventListener("click", (event) => {
    event.preventDefault();
    document.getElementById("addPetModal").style.display = "block";
});

document.querySelector("#addPetModal .close").addEventListener("click", () => {
    document.getElementById("addPetModal").style.display = "none";
});

document.getElementById("Birthday").setAttribute("max", todayStr);
document.getElementById("Birthday").setAttribute("min", minDateStr);

document
    .getElementById("addPetForm")
    .addEventListener("submit", async (event) => {
        event.preventDefault();

        const token = localStorage.getItem("token");
        const name = document.getElementById("Name").value;
        const breed1 = document.getElementById("Breed").value;
        const breed2 = document.getElementById("Breed2").value;
        const weight = document.getElementById("Weight").value;
        const birthday = document.getElementById("Birthday").value;
        let age = null;
        const bio = document.getElementById("Bio").value;
        const fileInput = document.getElementById("ProfilePicture");

        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
        }
        if (birthday) {
            age = today.getFullYear() - new Date(birthday).getFullYear();
        }

        try {
            const fileName = `${name}-${Date.now()}.jpeg`;
            const { url: presignedUrl } = await getPresignedUrl(fileName);

            await uploadImageToS3(file, presignedUrl);

            const response = await fetch("http://localhost:8000/api/pets", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({
                    name,
                    breed1,
                    breed2,
                    weight,
                    birthday,
                    age,
                    bio,
                    imageUrl: presignedUrl.split("?")[0],
                }),
            });
            const result = await response.json();
            if (response.ok) {
                await displayUserPet();
            }

            document.getElementById("addPetModal").style.display = "none";
        } catch (error) {
            console.error(error);
            alert("Failed to add pet or image.");
        }
    });

document.getElementById("Mixed").addEventListener("change", function () {
    const displayStyle = this.checked ? "block" : "none";
    const checkStyle = this.checked ? "none" : "initial";

    document.getElementById("secondBreedContainer").style.display =
        displayStyle;
    document.getElementById("Unknown").style.display = checkStyle;
    document.querySelector('label[for="Unknown"]').style.display = checkStyle;

    if (this.checked) {
        initializeAutocomplete("Breed2", "breedList2");
    }
});

document.getElementById("Unknown").addEventListener("change", function () {
    const displayStyle = this.checked ? "none" : "block";
    const checkStyle = this.checked ? "none" : "initial";
    const mixedLabel = document.querySelector('label[for="Mixed"]');
    document.getElementById("breedContainer").style.display = displayStyle;
    document.getElementById("secondBreedContainer").style.display =
        displayStyle;
    document.getElementById("Mixed").style.display = checkStyle;
    mixedLabel.style.display = checkStyle;

    if (!this.checked) {
        document.getElementById("secondBreedContainer").style.display = "none";
        document.getElementById("Breed").value = "";
    } else {
        document.getElementById("Breed").value = "Unknown";
    }
});

const span = document.querySelector("#reminderFormModal .close");

span.onclick = function () {
    document.getElementById("reminderFormModal").style.display = "none";
};

document
    .getElementById("reminderForm")
    .addEventListener("submit", async (event) => {
        event.preventDefault();
        const token = localStorage.getItem("token");

        if (!token) {
            alert("You must be logged in to perform this action.");
            return;
        }

        const fileInput = document.getElementById("ProfilePicture");
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            try {
                const { url, fileName } = await getPresignedUrl(file.name);
                await uploadImageToS3(file, url);
            } catch (error) {
                console.error(error);
                alert("Failed to upload profile picture.");
                return;
            }
        }

        const title = document.getElementById("title").value;
        const start = document.getElementById("start").value;
        const end = document.getElementById("end").value;

        const payload = { title, start };
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

document.getElementById("myPetsLink").addEventListener("click", async () => {
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
    .addEventListener("click", async (event) => {
        const { petId } = event.target.dataset;
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

                const breed1Response = await fetch(
                    `/api/breeds/${petDetails.breed_id1}`,
                    {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    },
                );
                const breed1 = await breed1Response.json();
                console.log(breed1);

                document
                    .getElementById("breedDescription")
                    .querySelector("h2").textContent = breed1.name;
                document
                    .getElementById("breedDescription")
                    .querySelector("p").textContent = breed1.breed_description;

                document
                    .getElementById("healthDescription")
                    .querySelector("h2").textContent =
                    "Health (" + breed1.name + ")";
                document
                    .getElementById("healthDescription")
                    .querySelector("p").textContent = breed1.health_description;

                document
                    .getElementById("groomingDescription")
                    .querySelector("h2").textContent =
                    "Grooming (" + breed1.name + ")";
                document
                    .getElementById("groomingDescription")
                    .querySelector("p").textContent = breed1.groom_description;

                let breed2 = { name: "" };
                if (petDetails.breed_id2) {
                    const breed2Response = await fetch(
                        `/api/breeds/${petDetails.breed_id2}`,
                        {
                            headers: {
                                Authorization: `Bearer ${token}`,
                            },
                        },
                    );
                    if (breed2Response.ok) {
                        breed2 = await breed2Response.json();

                        if (!secondBreedName || !secondBreedDescription) {
                            const breedDescriptionSection =
                                document.getElementById("breedDescription");
                            const breedHealthSection =
                                document.getElementById("healthDescription");
                            const breedGroomingSection =
                                document.getElementById("groomingDescription");

                            secondBreedName = document.createElement("h2");
                            secondBreedNameHealth =
                                document.createElement("h2");
                            secondBreedNameGroom = document.createElement("h2");
                            secondBreedDescription =
                                document.createElement("p");
                            secondHealthDescription =
                                document.createElement("p");
                            secondGroomDescription =
                                document.createElement("p");

                            secondBreedName.setAttribute(
                                "id",
                                "secondBreedName",
                            );
                            secondBreedNameHealth.setAttribute(
                                "id",
                                "secondBreedNameHealth",
                            );
                            secondBreedNameGroom.setAttribute(
                                "id",
                                "secondBreedNameGroom",
                            );
                            secondBreedDescription.setAttribute(
                                "id",
                                "secondBreedDescription",
                            );
                            secondHealthDescription.setAttribute(
                                "id",
                                "secondHealthDescription",
                            );
                            secondGroomDescription.setAttribute(
                                "id",
                                "secondGroomDescription",
                            );

                            breedDescriptionSection.appendChild(
                                secondBreedName,
                            );
                            breedDescriptionSection.appendChild(
                                secondBreedDescription,
                            );
                            breedHealthSection.appendChild(
                                secondBreedNameHealth,
                            );
                            breedHealthSection.appendChild(
                                secondHealthDescription,
                            );
                            breedGroomingSection.appendChild(
                                secondBreedNameGroom,
                            );
                            breedGroomingSection.appendChild(
                                secondGroomDescription,
                            );
                        }

                        secondBreedName.style.display = "";
                        secondBreedNameHealth.style.display = "";
                        secondBreedNameGroom.style.display = "";
                        secondBreedDescription.style.display = "";
                        secondHealthDescription.style.display = "";
                        secondGroomDescription.style.display = "";
                        secondBreedName.textContent = breed2.name;
                        secondBreedNameHealth.textContent =
                            "Health (" + breed2.name + ")";
                        secondBreedNameGroom.textContent =
                            "Grooming (" + breed2.name + ")";
                        secondBreedDescription.textContent =
                            breed2.breed_description;
                        secondHealthDescription.textContent =
                            breed2.health_description;
                        secondGroomDescription.textContent =
                            breed2.groom_description;
                    }
                } else if (secondBreedName && secondBreedDescription) {
                    secondBreedName.style.display = "none";
                    secondBreedNameHealth.style.display = "none";
                    secondBreedNameGroom.style.display = "none";
                    secondBreedDescription.style.display = "none";
                    secondHealthDescription.style.display = "none";
                    secondGroomDescription.style.display = "none";
                    secondBreedName.textContent = "";
                    secondBreedNameHealth.textContent = "";
                    secondBreedNameGroom.textContent = "";
                    secondBreedDescription.textContent = "";
                    secondHealthDescription.textContent = "";
                    secondGroomDescription.textContent = "";
                    document.getElementById("petBreed2").textContent = "";
                }

                document.getElementById("petName").textContent =
                    petDetails.name;
                document.getElementById("petBreed1").textContent = breed1.name;
                document.getElementById("petBreed2").textContent = breed2.name;
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

document.addEventListener("DOMContentLoaded", async () => {
    await initializeAutocomplete("Breed", "breedList");
    await toggleLoginLogoutButtons();
    await displayUserPet();
});
