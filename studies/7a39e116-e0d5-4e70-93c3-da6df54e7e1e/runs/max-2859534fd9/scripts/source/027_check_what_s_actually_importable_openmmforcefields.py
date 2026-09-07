
# Check what's actually importable from openmmforcefields
import openmmforcefields
print("openmmforcefields version:", openmmforcefields.__version__)

# Check submodules
import pkgutil
for m in pkgutil.walk_packages(openmmforcefields.__path__, openmmforcefields.__name__ + "."):
    print(" ", m.name)
