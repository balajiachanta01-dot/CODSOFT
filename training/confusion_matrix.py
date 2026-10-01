import torch
from torchvision import models, datasets, transforms
from torch.utils.data import DataLoader
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

MODEL_PATH = "model/crop_disease_model.pth"
TEST_PATH = "split/test"

device = torch.device("cpu")

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
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
    for images, labels in loader:
        outputs = model(images)
        predictions = outputs.argmax(dim=1)

        y_true.extend(labels.numpy())
        y_pred.extend(predictions.numpy())

cm = confusion_matrix(y_true, y_pred)

plt.figure(figsize=(12, 10))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    xticklabels=classes,
    yticklabels=classes
)

plt.xlabel("Predicted Label")
plt.ylabel("Actual Label")
plt.title("Crop Disease Detection - Confusion Matrix")
plt.xticks(rotation=45, ha="right")
plt.yticks(rotation=0)
plt.tight_layout()

plt.savefig("docs/confusion_matrix.png", dpi=300)

print("Confusion matrix saved to: docs/confusion_matrix.png")
