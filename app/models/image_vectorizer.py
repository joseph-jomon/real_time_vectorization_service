from torchvision import models, transforms
from PIL import Image
import torch
import numpy as np

class ImageVectorizer:
    def __init__(self):
        self.model = models.resnet50(pretrained=True)
        self.model.eval()
        self.preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def vectorize(self, image: Image.Image) -> np.ndarray:
        img_t = self.preprocess(image)
        batch_t = torch.unsqueeze(img_t, 0)
        with torch.no_grad():
            output = self.model(batch_t)
        return output.numpy()
