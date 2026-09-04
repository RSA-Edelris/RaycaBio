
import os
workspace = "/home/ubuntu/rayca-sessions/9dea6793-337f-42cf-8e3e-908d9d53ed0e-dc0c221c42d4"
files = sorted(f for f in os.listdir(workspace) if f.startswith('fwd_') and f.endswith('.png'))
for f in files:
    sz = os.path.getsize(os.path.join(workspace, f))
    print(f'{f}  {sz:>8,} bytes')
print(f'\nTotal: {len(files)} files')
