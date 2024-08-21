from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from PIL import Image
import io

# Import the vectorizer classes
from models.text_vectorizer import TextVectorizer
from models.image_vectorizer import ImageVectorizer

app = FastAPI()

# Initialize vectorizers
text_vectorizer = TextVectorizer()
image_vectorizer = ImageVectorizer()

# Pydantic model for text input
class TextInput(BaseModel):
    text: str

@app.post("/vectorize/text")
async def vectorize_text(input: TextInput):
    result = text_vectorizer.vectorize(input.text)
    return result

@app.post("/vectorize/image")
async def vectorize_image(file: UploadFile = File(...)):
    # Read the image file
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))
    
    result = image_vectorizer.vectorize(image)
    return result
