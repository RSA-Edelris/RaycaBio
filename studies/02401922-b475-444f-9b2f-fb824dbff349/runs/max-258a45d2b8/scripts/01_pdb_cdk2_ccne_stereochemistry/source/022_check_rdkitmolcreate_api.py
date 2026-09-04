
# Check RDKitMolCreate API
import inspect
print(inspect.signature(RDKitMolCreate.from_pdbqt_mol))

# Check what a pose looks like
pdbqt_mol2 = PDBQTMolecule(pdbqt_str_docked, is_dlg=False, skip_typing=False)
poses_list = list(pdbqt_mol2)
print(f"Poses: {len(poses_list)}")
p0 = poses_list[0]
ret = RDKitMolCreate.from_pdbqt_mol(p0)
print(f"Return type: {type(ret)}, len: {len(ret) if hasattr(ret,'__len__') else 'n/a'}")
print(ret)
