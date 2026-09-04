
import sys, os, pickle
sys.path.insert(0, '/home/ubuntu/rayca-runtime/.mamba/envs/rayca/lib/python3.11/site-packages')
import parmed as pmd
import openmm as mm
import openmm.app as app

wd = '/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a'
prep_dir = '/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a/prepared_system'

print("Loading AMBER topology...")
parm = pmd.load_file(wd + '/complex_solv.prmtop', wd + '/complex_solv.inpcrd')
print(f"  atoms: {len(parm.atoms)}, residues: {len(parm.residues)}")

print("Creating OpenMM system...")
system = parm.createSystem(
    nonbondedMethod=app.PME,
    nonbondedCutoff=0.9 * mm.unit.nanometers,
    constraints=app.HBonds,
    rigidWater=True,
)
print("  forces:", [type(f).__name__ for f in system.getForces()])

with open(prep_dir + '/openmm_system.xml', 'w') as f:
    f.write(mm.XmlSerializer.serialize(system))
print("  system.xml written")

with open(prep_dir + '/openmm_topology.pkl', 'wb') as f:
    pickle.dump(parm.topology, f)
print("  topology.pkl written")

integrator = mm.LangevinMiddleIntegrator(300*mm.unit.kelvin, 1.0/mm.unit.picosecond, 0.002*mm.unit.picoseconds)
sim = app.Simulation(parm.topology, system, integrator)
sim.context.setPositions(parm.positions)
state = sim.context.getState(getPositions=True)
with open(prep_dir + '/system_state.xml', 'w') as f:
    f.write(mm.XmlSerializer.serialize(state))
print("  state.xml written")

for fn in sorted(os.listdir(prep_dir)):
    print(f"  {fn}: {os.path.getsize(prep_dir+'/'+fn)//1024} KB")
print("DONE")
