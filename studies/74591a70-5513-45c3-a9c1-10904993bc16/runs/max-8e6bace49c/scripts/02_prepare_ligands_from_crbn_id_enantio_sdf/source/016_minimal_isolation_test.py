
# minimal isolation test
print("test start")
try:
    from rdkit import Chem as _Chem
    m = _Chem.MolFromSmiles("c1ccccc1")
    print("RDKit ok, benzene:", m.GetNumAtoms(), "atoms")
except Exception as e:
    print("RDKit broken:", type(e).__name__, e)

# check what's in session state that might be problematic
import sys
problem_vars = []
for name in list(globals().keys()):
    obj = globals()[name]
    t = type(obj).__name__
    mod = getattr(type(obj), "__module__", "") or ""
    if any(x in mod for x in ("openmm","pdbfixer","simtk")):
        problem_vars.append((name, t, mod))
print(f"\nOpenMM objects in scope: {len(problem_vars)}")
for n, t, m in problem_vars[:10]:
    print(f"  {n}: {t} from {m}")
