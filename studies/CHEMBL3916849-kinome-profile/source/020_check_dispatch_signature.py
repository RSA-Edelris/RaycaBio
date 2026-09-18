
# Check dispatch signature
import inspect
print(inspect.signature(dispatch))
print()
print(dispatch.__doc__[:1000] if dispatch.__doc__ else "No docstring")
