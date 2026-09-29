const imageInput = document.getElementById("imageInput");
const preview = document.getElementById("preview");
const predictButton = document.getElementById("predictButton");

const disease = document.getElementById("disease");
const confidence = document.getElementById("confidence");

const description = document.getElementById("description");
const symptoms = document.getElementById("symptoms");
const management = document.getElementById("management");
const prevention = document.getElementById("prevention");

const confidenceFill = document.getElementById("confidenceFill");
const resetButton = document.getElementById("resetButton");


imageInput.addEventListener("change", function () {
    const file = imageInput.files[0];

    if (file) {
        if (!file.type.startsWith("image/")) {
            alert("Please select an image file.");
            imageInput.value = "";
            return;
        }

        if (file.size > 10 * 1024 * 1024) {
            alert("Image size must be less than 10 MB.");
            imageInput.value = "";
            return;
        }

        preview.src = URL.createObjectURL(file);
        preview.style.display = "block";
    }
});


predictButton.addEventListener("click", async function () {

    const file = imageInput.files[0];

    if (!file) {
        alert("Please select a leaf image first.");
        return;
    }

    predictButton.textContent = "🔄 Analyzing...";
    predictButton.disabled = true;

    disease.textContent = "Disease: Analyzing...";
    confidence.textContent = "Confidence: --";

    description.textContent = "AI is analyzing the image...";
    symptoms.textContent = "Please wait...";
    management.textContent = "Please wait...";
    prevention.textContent = "Please wait...";

    confidenceFill.style.width = "0%";

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("/predict", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Prediction failed");
        }

        disease.textContent = "Disease: " + data.name;
        confidence.textContent = "Confidence: " + data.confidence + "%";

        if (data.confidence < 70) {
            confidence.textContent += " ⚠️ Low confidence - please verify this result.";
        }
        confidenceFill.style.width = data.confidence + "%";

        description.textContent = data.description;
        symptoms.textContent = data.symptoms;
        management.textContent = data.management;
        prevention.textContent = data.prevention;

    } catch (error) {

        disease.textContent = "Disease: Error";
        confidence.textContent = "Confidence: --";

        description.textContent = error.message;
        symptoms.textContent = "--";
        management.textContent = "--";
        prevention.textContent = "--";

        confidenceFill.style.width = "0%";

    } finally {

        predictButton.textContent = "Predict Disease";
        predictButton.disabled = false;

    }
});


resetButton.addEventListener("click", function () {

    imageInput.value = "";
    preview.src = "";
    preview.style.display = "none";

    disease.textContent = "Disease: --";
    confidence.textContent = "Confidence: --";
    confidenceFill.style.width = "0%";

    description.textContent = "--";
    symptoms.textContent = "--";
    management.textContent = "--";
    prevention.textContent = "--";
});
