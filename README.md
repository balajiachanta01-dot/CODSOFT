# AI-Based Crop Disease Detection System

An AI-powered web application that detects possible crop diseases from leaf images using a deep learning model.

## Features

- Upload crop leaf images
- AI-based disease prediction
- Confidence percentage
- Disease description
- Symptoms
- Management suggestions
- Prevention suggestions
- Image validation
- Low-confidence warning
- Simple web interface

## Crops Supported

- Tomato
- Potato
- Bell Pepper

## Technologies Used

- Python
- PyTorch
- Torchvision
- ResNet18
- FastAPI
- HTML
- CSS
- JavaScript
- PlantVillage Dataset

## How to Run

Activate the virtual environment:

source venv/bin/activate

Start the server:

uvicorn backend.main:app --reload

Open in Chrome:

http://127.0.0.1:8000

## AI Model

The system uses transfer learning with a ResNet18 convolutional neural network trained on selected PlantVillage crop-disease classes.

## Disclaimer

This system provides AI-based predictions for educational purposes. For accurate agricultural diagnosis and treatment, consult a qualified agricultural expert.

## Future Improvements

- Add more crop diseases
- Improve performance on real-world field images
- Add prediction history
- Add database support
- Deploy the application online
- Add mobile support
