Yes, your understanding is correct. The issue arises because the `text_vectorizer` (and `image_vectorizer`) variables are declared inside the `lifespan` function, making them local to that function. As local variables, they are not accessible outside the `lifespan` function, which is why you're getting the `NameError` when trying to access `text_vectorizer` in your endpoint.

### Why This Happens

- **Local Scope**: Variables declared inside a function (like `text_vectorizer` inside the `lifespan` function) are only accessible within that function. They do not exist outside the function, so you can't directly access them in your endpoint.

- **Global Access**: If you want to use the `text_vectorizer` in your endpoint, it needs to be stored somewhere that the entire application can access, such as in a global variable (like in the FastAPI documentation example) or in `app.state`.

### Solutions

1. **Use `app.state`**:
   - Store the `text_vectorizer` in `app.state` so it can be accessed from any part of your FastAPI application, including your endpoints.
   
2. **Global Variable (like in the documentation)**:
   - Use a global variable to store the `text_vectorizer`, making it accessible throughout your application.

### Example with `app.state`

```python
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from PIL import Image
import io
from contextlib import asynccontextmanager
from models.text_vectorizer import TextVectorizer
from models.image_vectorizer import ImageVectorizer

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML models and store them in app.state for global access
    text_vectorizer = TextVectorizer()  # This loads the AI model
    image_vectorizer = ImageVectorizer()
    
    app.state.text_vectorizer = text_vectorizer
    app.state.image_vectorizer = image_vectorizer

    yield  # Application runs

    # Cleanup resources during shutdown
    text_vectorizer.close()
    image_vectorizer.close()

app = FastAPI(lifespan=lifespan)

class TextInput(BaseModel):
    text: str

@app.post("/vectorize/text")
async def vectorize_text(input: TextInput):
    # Access the vectorizer from app.state
    text_vectorizer = app.state.text_vectorizer
    result = text_vectorizer.vectorize(input.text)
    return result
```

### Key Points

- **Local Variables**: Declaring `text_vectorizer` inside `lifespan` makes it a local variable, which means it's only accessible within that function.
- **Global Access**: By storing