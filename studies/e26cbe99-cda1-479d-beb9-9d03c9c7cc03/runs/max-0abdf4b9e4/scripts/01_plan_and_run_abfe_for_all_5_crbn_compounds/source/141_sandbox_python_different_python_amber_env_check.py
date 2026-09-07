
# The sandbox Python is different from PYTHON (AMBER env)
# Check sandbox directly
import sys
print("Sandbox Python:", sys.executable)

try:
    import alchemlyb
    print("alchemlyb:", alchemlyb.__version__)
except ImportError:
    print("alchemlyb: not available in sandbox")

try:
    import pymbar
    print("pymbar:", pymbar.__version__)
except ImportError:
    print("pymbar: not available in sandbox")

try:
    import numpy
    print("numpy:", numpy.__version__)
except ImportError:
    print("numpy: not available in sandbox")

try:
    import scipy
    print("scipy:", scipy.__version__)
except ImportError:
    print("scipy: not available in sandbox")

try:
    import MDAnalysis
    print("MDAnalysis:", MDAnalysis.__version__)
except ImportError:
    print("MDAnalysis: not available in sandbox")
