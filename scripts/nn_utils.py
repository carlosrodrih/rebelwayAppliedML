import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", device)

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(28*28, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10)
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

class NNUtils:
    
    # Lista de clases de Fashion MNIST
    class_names = [
        'T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
        'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot'
    ]

    @staticmethod
    def predict(model_path: str, image: Image.Image):
        if not isinstance(model_path, str):
            raise TypeError("Invalid model path.")
        if not isinstance(image, Image.Image):
            raise TypeError("Invalid image format.")

        # Load model
        model = Net().to(device)
        model.load_state_dict(torch.load(model_path, map_location=device))
        model.eval()

        # Transform image
        transform = transforms.Compose([
            transforms.Resize((28,28)),
            transforms.Grayscale(num_output_channels=1),
            transforms.ToTensor()
        ])
        img_tensor = transform(image).unsqueeze(0).to(device)

        # Inference
        with torch.inference_mode():
            output = model(img_tensor)
            prediction = torch.argmax(output, dim=1).item()

        prediction_name = NNUtils.class_names[prediction]
        print(f"Prediction: {prediction_name}")

        return prediction_name
