from transformers import CLIPVisionModelWithProjection, AutoFeatureExtractor
import time
import torch
import numpy as np
from datasets import Dataset, Image as DatasetsImage
from torch.utils.data import DataLoader
import copy
from PIL import Image
from tqdm import tqdm


class ImageVectorizer:
    def __init__(self, model_name: str = "openai/clip-vit-base-patch32"): # models are loaded in the __init__ of the class. that means This will load the model as soon as the instance is created
        self.model_name = model_name
        self.vision_model = CLIPVisionModelWithProjection.from_pretrained(model_name) #model loading takes place here
        self.extractor = AutoFeatureExtractor.from_pretrained(model_name) # model loading takes place here also
        self.vision_model.to(torch.device("cpu"))
        self.vision_model.eval()

    def vectorize(self, image: Image.Image) -> dict:
        # Convert the PIL image to the datasets Image format
        ds = Dataset.from_dict({"Image": [image]}).cast_column("Image", DatasetsImage())
        
        # Extract the image tensors
        def image_preprocessing(example):
            extracted = self.extractor(
                images=[e.convert('RGB') for e in example["Image"]],
                return_tensors="pt"
            )
            return extracted

        ds2 = copy.deepcopy(ds)
        ds2.set_transform(image_preprocessing)

        #Create DataLoader for batched processing
        image_dl = DataLoader(ds2, batch_size=36, shuffle=False, num_workers=0)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # Generate the visual embedding    
        outputs = []
        for batch in tqdm(image_dl):
            with torch.no_grad():
                embedding = self.vision_model(batch['pixel_values'].to(device)).image_embeds.squeeze()
                outputs.append(embedding.to("cpu"))
        vision_embeddings = np.vstack(outputs)
        vision_embeddings_normed = vision_embeddings / np.linalg.norm(vision_embeddings, axis=1)[:, np.newaxis]



        
        # Prepare the response
        response = {
            "embedding": vision_embeddings_normed.tolist(),
            "model": self.model_name,
            "timestamp": int(time.time())
        }
        
        return response
    def close(self):
        print(f"implement code to release the resources for {self.model_name}")
