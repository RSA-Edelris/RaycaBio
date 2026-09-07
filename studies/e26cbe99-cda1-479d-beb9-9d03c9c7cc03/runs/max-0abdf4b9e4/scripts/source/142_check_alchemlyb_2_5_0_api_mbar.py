
# Check alchemlyb 2.5.0 API for MBAR
from alchemlyb.estimators import MBAR
from alchemlyb.parsing.gmx import extract_dHdl
from alchemlyb.preprocessing import slicing, statistical_inefficiency, equilibrium_detection
import inspect

# Quick API check
print("MBAR attributes:", [a for a in dir(MBAR()) if not a.startswith('_')][:20])

# Check if alchemtest has a sample GROMACS dhdl file we could use for a quick test
# Just check imports work
print("\nImports OK. alchemlyb 2.5.0 ready.")

# Check extract_dHdl signature
sig = inspect.signature(extract_dHdl)
print(f"\nextract_dHdl signature: {sig}")

# Check delta_f_ units doc  
src = inspect.getsource(MBAR.fit)
lines = [l for l in src.split('\n') if 'unit' in l.lower() or 'kT' in l or 'kcal' in l.lower()]
print("\nUnit-related lines in MBAR.fit:")
for l in lines[:10]:
    print(l)
