
import acpype
import inspect, pkgutil
# List what's in the top-level module
print(dir(acpype))
print()
# Check for submodules
for mod in pkgutil.iter_modules(acpype.__path__):
    print("submodule:", mod.name)
