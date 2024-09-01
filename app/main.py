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
    # Store the vectorizers in app.state
    app.state.text_vectorizer = text_vectorizer
    app.state.image_vectorizer = image_vectorizer
    yield # Allow the app to run

    #Clean up the ML models and release the resources
    image_vectorizer.close()
    text_vectorizer.close()
    # Clean up the ML models and release the resources


app = FastAPI(lifespan=lifespan)
# Pydantic model for text input
class TextInput(BaseModel):
    text: str

@app.post("/vectorize/text")
async def vectorize_text(input: TextInput):
    # Access the model from app.state
    text_vectorizer = app.state.text_vectorizer
    result = text_vectorizer.vectorize(input.text)
    return result

@app.post("/vectorize/image")
async def vectorize_image(file: UploadFile = File(...)):
    # Read the image file
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))
    image_vectorizer = app.state.image_vectorizer
    result = image_vectorizer.vectorize(image)
    return result
