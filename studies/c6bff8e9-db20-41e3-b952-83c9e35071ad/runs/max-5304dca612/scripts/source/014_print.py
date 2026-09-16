
import matplotlib
print("matplotlib version:", matplotlib.__version__)
from matplotlib.patches import Circle, FancyBboxPatch
import inspect

# Check Circle.__init__ signature
sig = inspect.signature(Circle.__init__)
print("Circle.__init__ params:", list(sig.parameters.keys()))

# Check FancyBboxPatch signature
sig2 = inspect.signature(FancyBboxPatch.__init__)
print("FancyBboxPatch.__init__ params:", list(sig2.parameters.keys()))

# Try instantiating them to verify positional arg order
c = Circle((1.0, 2.0), 0.39, color='red')
print("Circle((x,y), R) => center:", c.center, "radius:", c.radius)

fbp = FancyBboxPatch((0.0, 0.0), 1.0, 2.0, boxstyle="round,pad=0.1")
print("FancyBboxPatch((xy), width, height) => get_x:", fbp.get_x(), "get_width:", fbp.get_width(), "get_height:", fbp.get_height())
