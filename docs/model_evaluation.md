# Model Evaluation Report

## Model

The system uses a ResNet18 convolutional neural network with transfer learning for crop disease classification.

## Supported Classes

The model classifies 9 crop conditions:

1. Pepper Bell - Bacterial Spot
2. Pepper Bell - Healthy
3. Potato - Early Blight
4. Potato - Late Blight
5. Potato - Healthy
6. Tomato - Early Blight
7. Tomato - Late Blight
8. Tomato - Leaf Mold
9. Tomato - Healthy

## Evaluation Result

Test dataset size: 1,513 images

Test accuracy: **99.80%**

Macro F1-score: **approximately 1.00**

Weighted F1-score: **approximately 1.00**

## Important Evaluation Note

The test set was recreated from the PlantVillage dataset after the original training/validation split was lost. Therefore, the test images may overlap with images used during training.

The reported 99.80% result should therefore be considered a dataset evaluation result rather than a fully independent real-world benchmark.

Performance on real field images may be lower because field conditions can differ from the controlled PlantVillage images.

## Confusion Matrix

The confusion matrix is available at:

`docs/confusion_matrix.png`

## Conclusion

The model demonstrates strong classification performance on the evaluated PlantVillage test images. Further evaluation using completely unseen real-world field images would provide a better estimate of practical performance.
