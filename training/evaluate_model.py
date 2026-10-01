import torch
from torchvision import models, datasets, transforms
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score, classification_report

MODEL_PATH = "model/crop_disease_model.pth"
TEST_PATH = "split/test"

device = torch.device("cpu")

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])

checkpoint = torch.load(MODEL_PATH, map_location=device)

classes = checkpoint["classes"]

model = models.resnet18(weights=None)
model.fc = torch.nn.Linear(model.fc.in_features, len(classes))
model.load_state_dict(checkpoint["model_state_dict"])
model.to(device)
model.eval()

dataset = datasets.ImageFolder(TEST_PATH, transform=transform)
loader = DataLoader(dataset, batch_size=32, shuffle=False)

y_true = []
y_pred = []

with torch.no_grad():
    for batch, (images, labels) in enumerate(loader):
        if batch % 10 == 0:
            print(f"Processing batch {batch + 1}/{len(loader)}...", flush=True)
        outputs = model(images)
        predictions = outputs.argmax(dim=1)

        y_true.extend(labels.numpy())
        y_pred.extend(predictions.numpy())

accuracy = accuracy_score(y_true, y_pred)

print(f"\nTest Accuracy: {accuracy * 100:.2f}%\n")

print("Classification Report:")
print(
    classification_report(
        y_true,
        y_pred,
        target_names=dataset.classes,
        zero_division=0
    )
)
