The error you're encountering, `NameError: name 'text_vectorizer' is not defined`, occurs because the `text_vectorizer` variable is not accessible in the `vectorize_text` endpoint. This happens because `text_vectorizer` and `image_vectorizer` are defined within the `lifespan` context manager but are not passed or made available to the endpoints directly.

### Solution: Use `app.state` to Store and Access Models

To fix this, you can store `text_vectorizer` and `image_vectorizer` in `app.state` during the lifespan event. This way, they can be accessed globally within the application, including in your endpoints.

Here's how you can modify your code:

```python
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
    # Load the ML models
    text_vectorizer = TextVectorizer()  # This will load the AI model as soon as the instance of the class is created
    image_vectorizer = ImageVectorizer()
    
    # Store the vectorizers in app.state
    app.state.text_vectorizer = text_vectorizer
    app.state.image_vectorizer = image_vectorizer

    yield  # Allow the app to run

    # Clean up the ML models and release the resources
    print("Releasing resources...")
    text_vectorizer.close()
    image_vectorizer.close()

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
```

### Key Changes:

1. **Storing in `app.state`**: The `text_vectorizer` and `image_vectorizer` objects are stored in `app.state` during the application startup. This makes them accessible from any endpoint.

2. **Accessing Models in Endpoints**: In the `/vectorize/text` endpoint, the `text_vectorizer` is accessed from `app.state`. This resolves the `NameError` because `text_vectorizer` is now defined globally within the application context.

3. **Resource Cleanup**: The `close()` methods are called during the teardown phase (after `yield`), ensuring resources are properly released when the application shuts down.

### Why This Works:

By using `app.state`, you are effectively making `text_vectorizer` and `image_vectorizer` global objects within the FastAPI application. This ensures that they can be accessed from any part of your application, solving the scope issue that led to the `NameError`.