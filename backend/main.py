from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image, UnidentifiedImageError
from backend.model import predict
import io
import os

app = FastAPI(title="AI Crop Disease Detection System")

frontend_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "frontend"
)

app.mount("/static", StaticFiles(directory=frontend_path), name="static")


disease_info = {
    "Tomato___Late_blight": {
        "description": "A fungal-like disease that causes dark lesions on tomato leaves and fruit.",
        "symptoms": "Dark brown or black spots, leaf yellowing, and rapid leaf damage.",
        "management": "Remove infected plant parts and use appropriate fungicide according to local agricultural guidance.",
        "prevention": "Avoid prolonged leaf wetness, provide good spacing, and use healthy planting material."
    },
    "Tomato___Early_blight": {
        "description": "A fungal disease that commonly affects tomato leaves and stems.",
        "symptoms": "Brown circular spots with concentric rings and yellowing around affected areas.",
        "management": "Remove infected leaves and improve airflow around plants.",
        "prevention": "Avoid overhead watering and maintain good field sanitation."
    },
    "Tomato___Leaf_Mold": {
        "description": "A fungal disease that mainly affects tomato leaves under humid conditions.",
        "symptoms": "Yellow patches on the upper leaf surface and olive-green mold underneath.",
        "management": "Remove affected leaves and improve ventilation.",
        "prevention": "Reduce humidity and avoid wetting leaves."
    },
    "Tomato___healthy": {
        "description": "The model detected a healthy tomato leaf.",
        "symptoms": "No major disease symptoms detected.",
        "management": "Continue normal crop care and monitoring.",
        "prevention": "Maintain proper watering, nutrition, sanitation, and pest monitoring."
    },
    "Potato___Early_blight": {
        "description": "A fungal disease that causes lesions on potato leaves.",
        "symptoms": "Brown spots with concentric rings and yellowing of surrounding tissue.",
        "management": "Remove severely affected foliage and use appropriate fungicide when recommended.",
        "prevention": "Maintain plant nutrition, sanitation, and avoid prolonged leaf wetness."
    },
    "Potato___Late_blight": {
        "description": "A serious disease of potato caused by Phytophthora infestans.",
        "symptoms": "Dark water-soaked lesions on leaves and rapid plant deterioration.",
        "management": "Remove infected material and follow local agricultural recommendations for disease control.",
        "prevention": "Use healthy seed, provide good airflow, and avoid prolonged moisture on foliage."
    },
    "Potato___healthy": {
        "description": "The model detected a healthy potato leaf.",
        "symptoms": "No major disease symptoms detected.",
        "management": "Continue normal crop care and monitoring.",
        "prevention": "Use healthy planting material and maintain good field sanitation."
    },
    "Pepper,_bell___Bacterial_spot": {
        "description": "A bacterial disease that can affect pepper leaves and fruit.",
        "symptoms": "Small dark spots on leaves and lesions on fruit.",
        "management": "Remove severely infected plant material and follow local agricultural guidance.",
        "prevention": "Use disease-free seed and avoid spreading water from infected plants."
    },
    "Pepper,_bell___healthy": {
        "description": "The model detected a healthy bell pepper leaf.",
        "symptoms": "No major disease symptoms detected.",
        "management": "Continue normal crop care and monitoring.",
        "prevention": "Maintain proper watering, nutrition, sanitation, and pest monitoring."
    }
}


@app.get("/")
def home():
    return FileResponse(
        os.path.join(frontend_path, "index.html")
    )


@app.post("/predict")
async def predict_disease(file: UploadFile = File(...)):

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a valid image file."
        )

    image_data = await file.read()

    try:
        image = Image.open(io.BytesIO(image_data))
        image.verify()
        image = Image.open(io.BytesIO(image_data))

    except (UnidentifiedImageError, OSError):
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid image."
        )

    disease, confidence = predict(image)

    info = disease_info.get(
        disease,
        {
            "description": "Information is not available for this prediction.",
            "symptoms": "Please consult an agricultural expert.",
            "management": "Please consult an agricultural expert.",
            "prevention": "Follow standard crop health practices."
        }
    )

    return {
        "prediction": disease,
        "name": disease.replace("___", " - ").replace("_", " "),
        "confidence": round(confidence, 2),
        "description": info["description"],
        "symptoms": info["symptoms"],
        "management": info["management"],
        "prevention": info["prevention"]
    }
