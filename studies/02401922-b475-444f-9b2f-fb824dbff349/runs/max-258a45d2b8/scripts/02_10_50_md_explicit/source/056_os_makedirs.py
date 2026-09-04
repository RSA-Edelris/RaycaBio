
import parmed as pmd
import openmm as mm
import openmm.app as app
import pickle, os

wd = '/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a'
prep_dir = f'{wd}/prepared_system'
os.makedirs(prep_dir, exist_ok=True)

print("Loading AMBER topology...")
parm = pmd.load_file(f'{wd}/complex_solv.prmtop', f'{wd}/complex_solv.inpcrd')
print(f"  atoms: {len(parm.atoms)}, residues: {len(parm.residues)}")

print("Creating OpenMM system (PME, HBonds constraints)...")
system = parm.createSystem(
    nonbondedMethod=app.PME,
    nonbondedCutoff=0.9 * mm.unit.nanometers,
    constraints=app.HBonds,
    rigidWater=True,
)
print(f"  forces: {[type(f).__name__ for f in system.getForces()]}")

print("Serialising system XML...")
with open(f'{prep_dir}/openmm_system.xml', 'w') as f:
    f.write(mm.XmlSerializer.serialize(system))

print("Pickling topology...")
with open(f'{prep_dir}/openmm_topology.pkl', 'wb') as f:
    pickle.dump(parm.topology, f)

print("Building state from initial coordinates...")
integrator = mm.LangevinMiddleIntegrator(
    300 * mm.unit.kelvin, 1.0 / mm.unit.picosecond,
    0.002 * mm.unit.picoseconds)
simulation = app.Simulation(parm.topology, system, integrator)
simulation.context.setPositions(parm.positions)
state = simulation.context.getState(getPositions=True)
with open(f'{prep_dir}/system_state.xml', 'w') as f:
    f.write(mm.XmlSerializer.serialize(state))

for fn in os.listdir(prep_dir):
    sz = os.path.getsize(f'{prep_dir}/{fn}')
    print(f"  {fn}: {sz/1024:.0f} KB")
print("Done — prepared_system ready.")
