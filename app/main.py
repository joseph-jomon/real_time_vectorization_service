from fastapi import FastAPI, HTTPException
from app.models.text_vectorizer import TextVectorizer
from app.models.image_vectorizer import ImageVectorizer
from PIL import Image
from io import BytesIO
import numpy as np
import base64

app = FastAPI()

# Initialize the vectorizers
text_vectorizer = TextVectorizer()
image_vectorizer = ImageVectorizer()

@app.post("/vectorize-text/")
async def vectorize_text(text: str):
    try:
        vector = text_vectorizer.vectorize(text)
        return {"vector": vector.tolist(), "source": "computed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error vectorizing text: {str(e)}")

@app.post("/vectorize-image/")
async def vectorize_image(image_data: str):
    try:
        # Decode base64 image data
        image = Image.open(BytesIO(base64.b64decode(image_data)))
        vector = image_vectorizer.vectorize(image)
        return {"vector": vector.tolist(), "source": "computed"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image data: {str(e)}")
