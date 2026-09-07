
import inspect
from openmmforcefields import generators

print("openmmforcefields.generators classes:")
for name in dir(generators):
    obj = getattr(generators, name)
    if inspect.isclass(obj):
        print(f"  {name}")
        # show constructor signature
        try:
            sig = inspect.signature(obj.__init__)
            print(f"    __init__: {sig}")
        except:
            pass

# Check GAFF specifically
print("\nGAFFTemplateGenerator methods:")
print([m for m in dir(GAFFTemplateGenerator) if not m.startswith('_')])
