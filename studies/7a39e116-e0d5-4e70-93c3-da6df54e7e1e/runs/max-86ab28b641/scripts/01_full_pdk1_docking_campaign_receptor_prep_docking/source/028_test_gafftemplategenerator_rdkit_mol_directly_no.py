
# Test GAFFTemplateGenerator with RDKit mol directly (no openff needed)
from openmmforcefields.generators import GAFFTemplateGenerator
from rdkit.Chem import SDMolSupplier
import inspect

# Check what GAFFTemplateGenerator accepts
sig = inspect.signature(GAFFTemplateGenerator.__init__)
print("GAFFTemplateGenerator.__init__ signature:", sig)

# Check if it has a from_rdkit or molecules_from_rdkit method
for name, method in inspect.getmembers(GAFFTemplateGenerator, predicate=inspect.isfunction):
    if 'rdkit' in name.lower() or 'mol' in name.lower() or 'smiles' in name.lower():
        print(f"  {name}")
