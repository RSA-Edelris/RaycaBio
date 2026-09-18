
import inspect
from Bio.PDB import Superimposer
from Bio.PDB.SVDSuperimposer import SVDSuperimposer

print("=== Superimposer.set_atoms sig ===")
print(inspect.signature(Superimposer.set_atoms))

print("\n=== SVDSuperimposer.get_rotran source ===")
print(inspect.getsource(SVDSuperimposer.get_rotran))

print("\n=== SVDSuperimposer.get_transformed source ===")
print(inspect.getsource(SVDSuperimposer.get_transformed))

print("\n=== SVDSuperimposer.run (last 20 lines) ===")
src = inspect.getsource(SVDSuperimposer.run)
print('\n'.join(src.split('\n')[-25:]))
