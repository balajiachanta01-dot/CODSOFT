import torch
from torchvision import models

MODEL_PATH = "model/crop_disease_model.pth"

checkpoint = torch.load(MODEL_PATH, map_location="cpu")

classes = checkpoint["classes"]

model = models.resnet18(weights=None)
model.fc = torch.nn.Linear(model.fc.in_features, len(classes))
model.load_state_dict(checkpoint["model_state_dict"])

print("Model loaded successfully!")
print("Number of classes:", len(classes))
print("Classes:")

for i, name in enumerate(classes, 1):
    print(f"{i}. {name}")
