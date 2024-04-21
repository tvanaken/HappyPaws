const wrapper = document.querySelector(".right_col");
const breedLink = document.querySelector(".breed-link");
const dietLink = document.querySelector(".diet-link");
const healthLink = document.querySelector(".health-link");
const groomingLink = document.querySelector(".grooming-link");
const scheduleLink = document.querySelector(".schedule-link");
const sections = document.querySelectorAll(".right_col .section");
let breeds = [];

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
            .getElementById("dietDescription")
            .querySelector("p").textContent = breed1.nutrition_description;
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

        document.getElementById("prof_pic").querySelector("img").src =
            petDetails.image_url;
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

        await updateDietRecommendations(
            petDetails.breed_id1,
            petDetails.age,
            petDetails.activity_level,
        );
    } else {
        if (!sessionStorage.getItem("addPetModalShown")) {
            document.getElementById("addPetModal").style.display = "block";
            sessionStorage.setItem("addPetModalShown", "true");
        }
    }
}

async function updateDietRecommendations(breedId, age, activityLevel) {
    const foodGrid = document.getElementById("foodGrid");
    const foodDetailsDiv = document.getElementById("foodDetails");
    try {
        const response = await fetch(
            `http://localhost:8000/api/recommended_foods?breedId=${breedId}&age=${age}&activityLevel=${activityLevel}`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
            },
        );

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const foods = await response.json();
        foodGrid.innerHTML = "";
        foodDetailsDiv.innerHTML = "";

        foods.forEach((food) => {
            const foodItemDiv = document.createElement("div");
            foodItemDiv.classList.add("foodItem");

            const image = document.createElement("img");
            image.src = food.image_url;
            image.alt = food.name;
            image.className = "foodImage";
            image.dataset.foodId = food.id;

            const nameParagraph = document.createElement("p");
            nameParagraph.className = "foodName";
            nameParagraph.textContent = food.name;

            foodItemDiv.appendChild(image);
            foodItemDiv.appendChild(nameParagraph);

            image.addEventListener("click", () => displayFoodDetails(food));

            foodGrid.appendChild(foodItemDiv);
        });
    } catch (error) {
        console.error("Failed to fetch recommended foods:", error);
    }
}

function displayFoodDetails(food) {
    const foodDetailsDiv = document.getElementById("foodDetails");
    foodDetailsDiv.innerHTML = `
        <h3>${food.name}</h3><br>
        <p>${food.ingredients}</p><br>
        <table id="nutrient">
            ${renderNutrients(food)}
        </table>
        <a href="${food.site_url}" target="_blank" >
            <button type="submit" style="margin-bottom: 20px">Buy Now</button>
        </a>
    `;
    console.log(food);
}

function renderNutrients(food) {
    const nutrients = [
        "nutrient_crude_protein",
        "nutrient_crude_fat",
        "nutrient_crude_fiber",
        "nutrient_moisture",
        "nutrient_dietary_starch",
        "nutrient_sugars",
        "nutrient_epa",
        "nutrient_dha",
        "nutrient_calcium",
        "nutrient_ash",
        "nutrient_l_carnitine",
        "nutrient_bacillus_coagulants",
        "nutrient_taurine",
        "nutrient_beta_carontene",
        "nutrient_phosphorous",
        "nutrient_niacin",
        "nutrient_chondroitin_sulfate",
        "nutrient_pyridoxine_vitamin_b6",
        "nutrient_vitamin_a",
        "nutrient_vitamin_e",
        "nutrient_ascorbic_acid",
        "nutrient_omega_6",
        "nutrient_omega_3",
        "nutrient_glucosamine",
        "nutrient_zinc",
        "nutrient_selenium",
        "nutrient_microorganisms",
        "nutrient_total_microorganisms",
    ];

    return nutrients
        .map((nutrient) => {
            if (food[nutrient] && food[nutrient].trim() !== "") {
                return `<tr>
                <td>${formatNutrientName(nutrient)}</td>
                <td>${food[nutrient]}</td>
            </tr>`;
            }
            return "";
        })
        .join("");
}

function formatNutrientName(nutrient) {
    return nutrient
        .replace("nutrient_", "")
        .replace(/_/g, " ")
        .split(" ")
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(" ");
}

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

function filterBreeds(inputValue) {
    const filteredBreeds = breeds.filter((breed) =>
        breed.name.toLowerCase().includes(inputValue.toLowerCase()),
    );
    displaySuggestions(filteredBreeds);
}

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

// async function initializeAutocomplete(breedInputId, suggestionsContainerId) {
//     const breedInput = document.getElementById(breedInputId);
//     const suggestionsContainer = document.getElementById(
//         suggestionsContainerId,
//     );

//     breedInput.addEventListener("input", async function () {
//         const inputValue = this.value;
//         if (inputValue.length > 1) {
//             fetch(`/api/breeds?search=${inputValue}`)
//                 .then((response) => response.json())
//                 .then((data) => {
//                     console.log("data", data);
//                     suggestionsContainer.innerHTML = "";
//                     data.forEach((breed) => {
//                         const suggestionItem = document.createElement("div");
//                         suggestionItem.innerHTML = breed.name;
//                         suggestionItem.addEventListener("click", function () {
//                             breedInput.value = this.textContent;
//                             suggestionsContainer.innerHTML = "";
//                         });
//                         suggestionsContainer.appendChild(suggestionItem);
//                     });
//                 })
//                 .catch((error) => console.log("error", error));
//         } else {
//             suggestionsContainer.innerHTML = "";
//         }
//     });
// }

async function toggleLoginLogoutButtons() {
    const token = localStorage.getItem("token");
    const loginButton = document.getElementById("loginButton");
    const logoutButton = document.getElementById("logoutButton");

    if (token) {
        loginButton.style.display = "none";
        logoutButton.style.display = "inline-block";
        logoutButton.addEventListener("click", () => {
            localStorage.removeItem("token");
            sessionStorage.removeItem("addPetModalShown");
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
        daysOfWeek: reminder.daysOfWeek,
        startTime: reminder.startTime,
        endTime: reminder.endTime,
        startRecur: reminder.startRecur,
        endRecur: reminder.endRecur,
        color: reminder.color,
    }));
    const calendarEl = document.getElementById("calendar");
    const tooltip = document.createElement("div");
    tooltip.className = "tooltip";
    document.body.appendChild(tooltip);
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
            right: "dayGridMonth,timeGridWeek",
        },
        initialView: "dayGridMonth",
        height: "auto",
        schedulerLicenseKey: "CC-Attribution-NonCommercial-NoDerivatives",
        events: eventData,
        eventMouseEnter: function (info) {
            tooltip.innerHTML = `<strong>Title:</strong> ${info.event.title}<br>
                                 <strong>Start:</strong> ${info.event.start.toISOString()}<br>
                                 <strong>End:</strong> ${
                                     info.event.end
                                         ? info.event.end.toISOString()
                                         : "N/A"
                                 }<br>`;
            tooltip.style.display = "block";
            tooltip.style.left = info.jsEvent.pageX + 10 + "px";
            tooltip.style.top = info.jsEvent.pageY + 10 + "px";
        },
        eventMouseLeave: function (info) {
            tooltip.style.display = "none";
        },
        eventTextColor: "black",
    });
    await calendar.render();
}

async function getPresignedUrl(file_name) {
    const token = localStorage.getItem("token");
    const response = await fetch(
        `http://localhost:8000/api/s3PresignedUrl?file_name=${file_name}`,
        {
            method: "GET",
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
        const errorBody = await response.text();
        console.error("Failed to upload image to S3:", errorBody);
        throw new Error("Failed to upload image to S3");
    }
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

document.getElementById("calendarSection").addEventListener("click", () => {
    initializeCalendar();
});

document.querySelector("#addPetModal .close").addEventListener("click", () => {
    document.getElementById("addPetModal").style.display = "none";
});

document.getElementById("Birthday").setAttribute("max", todayStr);
document.getElementById("Birthday").setAttribute("min", minDateStr);

document
    .getElementById("addPetForm")
    .addEventListener("submit", async (event) => {
        const submitBtn = document.getElementById("submitBtn");
        submitBtn.innerHTML = 'Loading... <div class="loader"></div>';
        submitBtn.disabled = true;
        document.body.style.cursor = "progress";

        event.preventDefault();

        const token = localStorage.getItem("token");
        const name = document.getElementById("Name").value;
        const breed1 = document.getElementById("Breed").value;
        const breed2 = document.getElementById("Breed2").value;
        const weight = document.getElementById("Weight").value;
        const activity_level = document.getElementById("ActivityLevel").value;
        const birthday = document.getElementById("Birthday").value;
        const bio = document.getElementById("Bio").value;
        const fileInput = document.getElementById("ProfilePicture");
        let file = null;
        let age = null;

        if (fileInput.files.length > 0) {
            file = fileInput.files[0];
        }
        if (birthday) {
            age = today.getFullYear() - new Date(birthday).getFullYear();
        }

        try {
            const file_name = `${name}-${Date.now()}.jpeg`;
            const { url: presignedUrl } = await getPresignedUrl(file_name);
            const image_url = `https://happypawsproject.s3.amazonaws.com/${file_name}`;

            console.log("Uploading image to S3...");
            await uploadImageToS3(file, presignedUrl);
            console.log("Image uploaded to S3.");

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
                    activity_level,
                    birthday,
                    age,
                    bio,
                    image_url,
                }),
            });
            if (response.ok) {
                await displayUserPet();
                showNotification(name + " added successfully!", false);

                name.value = "";
                breed1.value = "";
                breed2.value = "";
                weight.value = "";
                activity_level.value = "";
                birthday.value = "";
                bio.value = "";
                fileInput.value = "";
            }

            document.getElementById("addPetModal").style.display = "none";
        } catch (error) {
            console.error(error);
            showNotification("Failed to add pet. Please try again.", true);
        } finally {
            submitBtn.innerHTML = "Submit";
            submitBtn.disabled = false;
            document.body.style.cursor = "default";
        }
    });

document.getElementById("recurring").addEventListener("change", function () {
    const displayStyle = this.checked ? "block" : "none";
    document.getElementById("recurringOptions").style.display = displayStyle;
});

document.getElementById("frequency").addEventListener("change", function () {
    const displayStyle = this.value === "weekly" ? "block" : "none";
    document.getElementById("dowWrapper").style.display = displayStyle;
});

document.getElementById("Mixed").addEventListener("change", function () {
    const displayStyle = this.checked ? "block" : "none";
    const checkStyle = this.checked ? "none" : "initial";

    document.getElementById("secondBreedContainer").style.display =
        displayStyle;
    document.getElementById("Unknown").style.display = checkStyle;
    document.querySelector('label[for="Unknown"]').style.display = checkStyle;

    if (this.checked) {
        document.getElementById("Breed2").addEventListener("input", (event) => {
            const inputValue = event.target.value;
            if (inputValue.length > 0) {
                filterBreeds(inputValue);
            } else {
                displaySuggestions(breeds);
            }
        });

        document.getElementById("Breed2").addEventListener("focus", () => {
            preloadBreeds();
            displaySuggestions(breeds);
        });

        document.getElementById("Breed2").addEventListener("blur", () => {
            setTimeout(() => {
                document.getElementById("breedList2").innerHTML = "";
            }, 200);
        });
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

        const title = document.getElementById("title").value;
        const startDate = document.getElementById("startDate").value;
        const startTime = document.getElementById("startTime").value;
        const recurring = document.getElementById("recurring").checked;
        const endDate = document.getElementById("endDate").value;
        const endTime = document.getElementById("endTime").value;
        const color = document.querySelector(".select-selected").dataset.value;

        const daysOfWeek = [];
        document.querySelectorAll("#daysOfWeek input").forEach((input) => {
            if (input.checked) {
                daysOfWeek.push(input.value);
            }
        });

        const startDateTime = `${startDate}T${startTime}`;
        const endDateTime = endDate && endTime ? `${endDate}T${endTime}` : null;
        const startDateObj = new Date(startDate);

        startDateObj.setDate(startDateObj.getDate() + 1);

        const payload = {
            title,
            start: startDateTime,
            end: endDateTime,
            daysOfWeek: daysOfWeek.length > 0 ? daysOfWeek : null,
            startRecur: startDate,
            endRecur: recurring
                ? endDate
                : startDateObj.toISOString().split("T")[0],
            startTime: startTime,
            endTime: endTime,
            color: color,
        };

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

        document.getElementById("title").value = "";
        document.getElementById("startDate").value = "";
        document.getElementById("startTime").value = "";
        document.getElementById("endDate").value = "";
        document.getElementById("endTime").value = "";
        document.getElementById("recurring").checked = false;
        document.getElementById("frequency").value = "daily";
        document.getElementById("dowWrapper").style.display = "none";
        document.getElementById("reminderFormModal").style.display = "none";
        document.getElementById("daysOfWeek").style.display = "none";
        document.querySelector(".select-selected").textContent = "Select Color";
        await initializeCalendar();
    });

document
    .querySelector(".select-selected")
    .addEventListener("click", function () {
        const itemsDiv = document.querySelector(".select-items");
        itemsDiv.style.display =
            itemsDiv.style.display === "block" ? "none" : "block";
    });

document.querySelectorAll(".select-items li").forEach((item) => {
    item.addEventListener("click", function () {
        const selectedDiv = document.querySelector(".select-selected");
        selectedDiv.textContent = this.textContent;

        const colorValue = this.getAttribute("data-value");

        selectedDiv.setAttribute("data-value", colorValue);

        selectedDiv.style.backgroundColor = colorValue;

        document.querySelector(".select-items").style.display = "none";
    });
});

document.addEventListener("click", function (e) {
    const select = document.querySelector(".custom-select");
    if (!select.contains(e.target)) {
        document.querySelector(".select-items").style.display = "none";
    }
});

document.getElementById("myPetsLink").addEventListener("mouseenter", async () => {
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

            const addButton = document.createElement("div");
            addButton.innerHTML = "+";
            addButton.classList.add("add-pet-button");
            dropdown.appendChild(addButton);

            addButton.addEventListener("click", (event) => {
                event.stopPropagation();
                document.getElementById("addPetModal").style.display = "block";
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

                await updateDietRecommendations(
                    petDetails.breed_id1,
                    petDetails.age,
                    petDetails.activity_level,
                );

                document
                    .getElementById("breedDescription")
                    .querySelector("h2").textContent = breed1.name;
                document
                    .getElementById("breedDescription")
                    .querySelector("p").textContent = breed1.breed_description;
                document
                    .getElementById("dietDescription")
                    .querySelector("p").textContent =
                    breed1.nutrition_description;
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

                document.getElementById("prof_pic").querySelector("img").src =
                    petDetails.image_url;
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
    //await initializeAutocomplete("Breed", "breedList");
    await preloadBreeds();
    await toggleLoginLogoutButtons();
    await displayUserPet();
});
