# Project Test Report

## 1. Model Loading Test

**Status:** Passed

The trained ResNet18 model was loaded successfully from the saved model file.

## 2. Image Upload Test

**Status:** Passed

The application successfully accepts crop leaf images through the file upload interface.

## 3. Disease Prediction Test

**Status:** Passed

The AI model successfully predicts supported crop disease classes and displays the prediction confidence.

## 4. Disease Information Test

**Status:** Passed

The application displays disease description, symptoms, management, and prevention information.

## 5. Confidence Display Test

**Status:** Passed

The application displays the model confidence percentage and a visual confidence bar.

## 6. Error Handling Test

**Status:** Passed

The application displays an error when the user attempts to predict without selecting an image.

## 7. Loading State Test

**Status:** Passed

The Predict Disease button changes to an analyzing state while the AI prediction is being processed.

## 8. Supported Crops

- Tomato
- Potato
- Bell Pepper

## 9. Overall Result

The core AI-based crop disease detection system is functioning successfully in the local development environment.

**Note:** Model performance was evaluated on a test split created from the PlantVillage dataset. Because the original train/validation split was later recreated, the reported test accuracy should not be treated as a fully independent benchmark.
