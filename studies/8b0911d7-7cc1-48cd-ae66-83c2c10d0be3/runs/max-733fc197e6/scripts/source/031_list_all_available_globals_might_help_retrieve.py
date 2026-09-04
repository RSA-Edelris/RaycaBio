
# List all available globals that might help retrieve container artifacts
import builtins
g = {k: type(v).__name__ for k, v in globals().items() if not k.startswith('__')}
# Focus on callables
callables = {k: v for k, v in globals().items() if callable(v) and not k.startswith('__')}
print("Callable globals:", list(callables.keys()))
