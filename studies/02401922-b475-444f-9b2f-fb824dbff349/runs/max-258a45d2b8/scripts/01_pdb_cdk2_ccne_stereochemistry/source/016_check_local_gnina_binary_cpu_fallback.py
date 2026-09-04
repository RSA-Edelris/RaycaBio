
import subprocess
# Check local gnina binary (CPU fallback)
r = subprocess.run(['which', 'gnina'], capture_output=True, text=True)
print('gnina binary:', r.stdout.strip() or 'not found')

# Check smina (gnina predecessor, often installed alongside)
r2 = subprocess.run(['which', 'smina'], capture_output=True, text=True)
print('smina binary:', r2.stdout.strip() or 'not found')

# Check autodock vina
r3 = subprocess.run(['which', 'vina'], capture_output=True, text=True)
print('vina binary:', r3.stdout.strip() or 'not found')

# Check if gnina container image can be pulled/run differently
# List docker images available
r4 = subprocess.run(['docker', 'images', '--format', '{{.Repository}}:{{.Tag}}'],
                    capture_output=True, text=True)
imgs = [l for l in r4.stdout.strip().split('\n') if 'gnina' in l.lower() or 'dock' in l.lower()]
print('docking images:', imgs or 'none found')
