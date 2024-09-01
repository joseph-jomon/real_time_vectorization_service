from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from PIL import Image
import io
from contextlib import asynccontextmanager
# Import the vectorizer classes, this does not load the ai model
from models.text_vectorizer import TextVectorizer
from models.image_vectorizer import ImageVectorizer

@asynccontextmanager
async def lifespan(app: FastAPI):
    #Load the ML model
    text_vectorizer = TextVectorizer()# This will load the ai model as soon as the instance of the class is created
    image_vectorizer = ImageVectorizer()
    yield
    print("code to release resources")
    image_vectorizer.close()
    text_vectorizer.close()
    # Clean up the ML models and release the resources


app = FastAPI(lifespan=lifespan)
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
