import time
import torch
import numpy as np
from transformers import AutoTokenizer, CLIPTextModelWithProjection

class TextVectorizer:
    def __init__(self, model_name: str = "openai/clip-vit-base-patch32"):
        """
        Initializes the TextVectorizer with the specified model.
        
        Args:
            model_name (str): The name of the pre-trained model to use.
        """
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.text_model = CLIPTextModelWithProjection.from_pretrained(model_name)
        self.text_model.eval()  # Set the model to evaluation mode

    def vectorize(self, text: str) -> dict:
        """
        Generates a text embedding for the given input text.
        
        Args:
            text (str): The input text to vectorize.
        
        Returns:
            dict: A dictionary containing the text embedding, model information, and timestamp.
        """
        # Tokenize the input text
        text_inputs = self.tokenizer(text=text, truncation=True, return_tensors="pt")
        
        # Generate text embedding without computing gradients
        with torch.no_grad():
            text_outputs = self.text_model(**text_inputs)
            text_embedding = text_outputs.text_embeds.squeeze().numpy()
        
        # Prepare the response dictionary
        response = {
            "embedding": text_embedding.tolist(),  # Convert numpy array to list for JSON serialization
            "model": self.model_name,
            "timestamp": int(time.time())
        }
        
        return response
