
import gzip

# Read the docked SDF output
sdf_out_path = '/home/ubuntu/rayca-sessions/c29e716e-6774-4a9b-8ead-aba645849be4-01def6985d02/gnina_docked.sdf.gz'
with gzip.open(sdf_out_path, 'rt') as f:
    sdf_out = f.read()

print(f"Output SDF size: {len(sdf_out)} bytes")
print(sdf_out[:3000])
