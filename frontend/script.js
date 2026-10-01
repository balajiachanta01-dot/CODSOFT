const imageInput = document.getElementById("imageInput");
const preview = document.getElementById("preview");
const dropZone = document.getElementById("dropZone");
const selectedFile = document.getElementById("selectedFile");
const predictButton = document.getElementById("predictButton");
const loadingPanel = document.getElementById("loadingPanel");

const result = document.getElementById("result");
const resultPlaceholder = document.querySelector(".result-placeholder");
const resultContent = document.getElementById("resultContent");

const disease = document.getElementById("disease");
const confidence = document.getElementById("confidence");
const confidenceFill = document.getElementById("confidenceFill");

const description = document.getElementById("description");
const symptoms = document.getElementById("symptoms");
const management = document.getElementById("management");
const prevention = document.getElementById("prevention");
const warning = document.getElementById("warning");

const resetButton = document.getElementById("resetButton");
const historyButton = document.getElementById("historyButton");
const historyList = document.getElementById("historyList");

let selectedImage = null;


// -------------------------
// IMAGE SELECTION
// -------------------------

imageInput.addEventListener("change", function () {
    if (this.files.length > 0) {
        handleImage(this.files[0]);
    }
});

function handleImage(file) {

    if (!file.type.startsWith("image/")) {
        showError("Please select a valid image file.");
        return;
    }

    if (file.size > 10 * 1024 * 1024) {
        showError("Image size must be less than 10 MB.");
        return;
    }

    selectedImage = file;

    selectedFile.textContent = `Selected: ${file.name}`;

    const reader = new FileReader();

    reader.onload = function (event) {
        preview.src = event.target.result;
        preview.style.display = "block";
    };

    reader.readAsDataURL(file);

    dropZone.classList.add("has-image");
}


// -------------------------
// DRAG AND DROP
// -------------------------

dropZone.addEventListener("dragover", function (event) {
    event.preventDefault();
    dropZone.classList.add("dragging");
});

dropZone.addEventListener("dragleave", function () {
    dropZone.classList.remove("dragging");
});

dropZone.addEventListener("drop", function (event) {
    event.preventDefault();

    dropZone.classList.remove("dragging");

    const files = event.dataTransfer.files;

    if (files.length > 0) {
        handleImage(files[0]);
    }
});


// -------------------------
// PREDICTION
// -------------------------

predictButton.addEventListener("click", async function () {

    if (!selectedImage) {
        showError("Please select a leaf image first.");
        return;
    }

    const formData = new FormData();
    formData.append("file", selectedImage);

    predictButton.disabled = true;
    predictButton.innerHTML = "✦ Analyzing...";

    loadingPanel.style.display = "flex";

    try {

        const response = await fetch("/predict", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Prediction failed.");
        }

        showResult(data);

    } catch (error) {

        showError(error.message || "Could not analyze the image.");

    } finally {

        predictButton.disabled = false;
        predictButton.innerHTML =
            '<span>✦</span> Analyze Leaf <span class="arrow">→</span>';

        loadingPanel.style.display = "none";
    }
});


// -------------------------
// DISPLAY RESULT
// -------------------------

function showResult(data) {

    resultPlaceholder.classList.add("hidden");
    resultContent.classList.remove("hidden");

    result.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });

    disease.textContent =
        data.display_name || formatDiseaseName(data.disease);

    confidence.textContent =
        `${Number(data.confidence).toFixed(2)}%`;

    description.textContent =
        data.description || "No description available.";

    symptoms.textContent =
        data.symptoms || "No symptom information available.";

    management.textContent =
        data.management || "No management information available.";

    prevention.textContent =
        data.prevention || "No prevention information available.";

    setTimeout(() => {
        confidenceFill.style.width =
            `${Math.min(Number(data.confidence), 100)}%`;
    }, 100);

    if (Number(data.confidence) < 70) {
        warning.style.display = "block";
        warning.textContent =
            "⚠️ The model confidence is relatively low. Consider uploading a clearer leaf image and consult an agricultural expert.";
    } else {
        warning.style.display = "none";
    }
}


// -------------------------
// RESET
// -------------------------

resetButton.addEventListener("click", function () {

    selectedImage = null;
    imageInput.value = "";

    preview.src = "";
    preview.style.display = "none";

    selectedFile.textContent = "";

    confidenceFill.style.width = "0%";

    resultContent.classList.add("hidden");
    resultPlaceholder.classList.remove("hidden");

    document.getElementById("scanner").scrollIntoView({
        behavior: "smooth"
    });
});


// -------------------------
// HISTORY
// -------------------------

historyButton.addEventListener("click", async function () {

    historyButton.disabled = true;
    historyButton.textContent = "Loading...";

    try {

        const response = await fetch("/history");

        if (!response.ok) {
            throw new Error("Could not load history.");
        }

        const data = await response.json();

        if (!data.length) {

            historyList.innerHTML = `
                <div class="empty-history">
                    No prediction history yet.
                </div>
            `;

        } else {

            historyList.innerHTML = data.map(item => `
                <div class="history-item">

                    <strong>
                        ${formatDiseaseName(item.disease)}
                    </strong>

                    <span>
                        ${Number(item.confidence).toFixed(2)}% confidence
                    </span>

                    <small>
                        ${item.created_at}
                    </small>

                </div>
            `).join("");
        }

    } catch (error) {

        historyList.innerHTML = `
            <div class="empty-history">
                Could not load prediction history.
            </div>
        `;

    } finally {

        historyButton.disabled = false;
        historyButton.textContent = "Refresh History ↻";
    }
});


// -------------------------
// HELPERS
// -------------------------

function formatDiseaseName(name) {

    if (!name) {
        return "Unknown condition";
    }

    return name
        .replace("___", " — ")
        .replaceAll("_", " ")
        .replace(",bell", " Bell");
}


function showError(message) {

    warning.style.display = "block";
    warning.textContent = `⚠️ ${message}`;

    resultPlaceholder.classList.remove("hidden");
    resultContent.classList.add("hidden");

    document.getElementById("insights").scrollIntoView({
        behavior: "smooth"
    });
}
