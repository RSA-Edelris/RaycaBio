
import importlib.util
spec = importlib.util.spec_from_file_location("pipeline", f"{MMDIR}/pipeline.py")
pipe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipe)

print("Building tleap topologies for all 32 ligands...")
ok, failed = [], []
for name in names:
    try:
        pipe.build_topology(name)
        cpx = (pipe.Path(pipe.MMDIR) / f"{name}_ent" / "complex.prmtop")
        ok.append(name)
        print(f"  OK  {name:<28} complex.prmtop={cpx.stat().st_size//1024}kB")
    except Exception as e:
        failed.append((name, str(e)[:200]))
        print(f"  FAIL {name}: {str(e)[:200]}")

print(f"\nSummary: {len(ok)}/32 OK,  {len(failed)} failed")
