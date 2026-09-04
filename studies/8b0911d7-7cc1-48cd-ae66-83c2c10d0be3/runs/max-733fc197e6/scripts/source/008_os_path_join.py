
import subprocess, os

SDF_IN  = "/home/ubuntu/rayca-artifacts/11507a0e2f5e69d5dfa40a62/files/P965_EDELRIS_2 Hits w enantiomers.sdf"
SDF_V2K = os.path.join(WORKDIR, 'ligands_v2000.sdf')

# Convert V3000 -> V2000 with obabel
r = subprocess.run(['obabel', SDF_IN, '-O', SDF_V2K, '--gen3d', '-h'],
                   capture_output=True, text=True)
print("stdout:", r.stdout[:500])
print("stderr:", r.stderr[:500])
print("returncode:", r.returncode)
print("exists:", os.path.exists(SDF_V2K), os.path.getsize(SDF_V2K) if os.path.exists(SDF_V2K) else 0)
