from fastapi import FastAPI, HTTPException, Depends
from app.models.text_vectorizer import TextVectorizer
from app.models.image_vectorizer import ImageVectorizer
from app.utils.cache import Cache
from PIL import Image
from io import BytesIO
import numpy as np
import base64

app = FastAPI()

# Dependency Injection
def get_cache():
    return Cache()

@app.post("/vectorize-text/")
async def vectorize_text(text: str, cache: Cache = Depends(get_cache)):
    cache_key = f"text_vector:{text}"
    cached_vector = cache.get(cache_key)
    if cached_vector:
        return {"vector": cached_vector}

    vectorizer = TextVectorizer()
    vector = vectorizer.vectorize(text)
    cache.set(cache_key, vector.tolist())
    return {"vector": vector.tolist()}

@app.post("/vectorize-image/")
async def vectorize_image(image_data: str, cache: Cache = Depends(get_cache)):
    try:
        # Decode base64 image data
        image = Image.open(BytesIO(base64.b64decode(image_data)))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image data")

    cache_key = f"image_vector:{image_data[:30]}"
    cached_vector = cache.get(cache_key)
    if cached_vector:
        return {"vector": cached_vector}

    vectorizer = ImageVectorizer()
    vector = vectorizer.vectorize(image)
    cache.set(cache_key, vector.tolist())
    return {"vector": vector.tolist()}
