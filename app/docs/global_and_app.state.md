The documentation you provided from FastAPI does not explicitly mention using `app.state` in conjunction with lifespan events. Instead, it uses a global dictionary (`ml_models`) to store and access the machine learning models. The example demonstrates a simple way to manage models and resources without using `app.state`.

### Key Points from the Documentation:

1. **Global Variable for Storage**:
   - In the example, `ml_models` is a global dictionary used to store the machine learning model. This dictionary is accessible from within the lifespan function as well as the endpoints.
   - The model is added to the dictionary before the `yield` and cleared after the `yield`.

2. **Lifespan Context Manager**:
   - The code before `yield` runs during the application startup (e.g., loading models).
   - The code after `yield` runs during the shutdown phase (e.g., releasing resources).

### Using `app.state` vs. Global Variables

- **Global Variables (as shown in the documentation)**:
  - This approach is simple and straightforward. It uses a global variable (e.g., `ml_models`) to store resources that need to be accessed across the application.
  - The variable is accessible from anywhere in the code, making it easy to use.

- **`app.state` (an alternative approach)**:
  - `app.state` is a more structured way to store and manage application-wide state. It avoids using global variables and ties the stored resources directly to the FastAPI application instance.
  - This can be beneficial in more complex applications where you want to avoid potential issues with global state or need to encapsulate resources within the application instance.

### When to Use `app.state`:

- **Encapsulation**: If you prefer to encapsulate resources within the FastAPI application and avoid global variables, `app.state` is a good choice.
- **Complex Applications**: For more complex applications, `app.state` can help keep things organized and prevent unintended side effects from using global variables.
- **Multi-instance Applications**: If you're running multiple instances of your FastAPI application (e.g., in a multi-tenant setup), `app.state` ensures that each instance manages its own resources independently.

### When Global Variables Are Sufficient:

- **Simple Applications**: In simpler applications where you have a straightforward use case, like the example in the documentation, global variables might be sufficient.
- **Quick Prototyping**: For quick prototypes or small projects, using a global variable like `ml_models` can be a faster and easier approach.

### Summary

- **The documentation example** shows the use of a global dictionary (`ml_models`) for storing and managing resources.
- **`app.state`** is not required but is a more organized alternative, especially useful in larger or more complex applications.
- **Choose based on your needs**: For simple cases, a global variable is fine. For more structured or complex applications, `app.state` might be preferable.

So, while the documentation doesn't specifically recommend `app.state`, it's an alternative you can consider based on the complexity and requirements of your application.