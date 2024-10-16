import torch
import torchvision.transforms as transforms
from torchvision.models import resnet34
from PIL import Image

# Sử dụng mô hình pre-trained Resnet34
class EmbeddingModel:
    def __init__(self):
        self.model = resnet34(pretrained=True)
        self.model.eval() 

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)), 
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def embed(self, image_path):
        image = Image.open(image_path).convert("RGB")
        image_tensor = self.transform(image).unsqueeze(0) 

        with torch.no_grad():
            embedding = self.model(image_tensor).numpy().flatten()  
        return embedding.tolist()  
