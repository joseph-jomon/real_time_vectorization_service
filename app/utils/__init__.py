# app/utils/__init__.py

# Expose Cache class directly
#from .cache import Cache
"""
When to Use a Non-Empty __init__.py

Creating a Simplified API:
If you want to provide users with a simpler or more cohesive API, you might import specific classes or functions into __init__.py to expose them at the package level. This is useful for larger packages where you want to hide internal details and present a clean interface.

Package Initialization:
In some cases, you might need to run some initialization code when your package is imported. This could include setting up logging, configuring settings, or loading resources. __init__.py is the place to do this.


Backward Compatibility:
If you’re refactoring a package and want to maintain backward compatibility, you might use __init__.py to continue exposing certain classes or functions in the same way they were before the refactor.
Conclusion
"""