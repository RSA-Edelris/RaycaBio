
import subprocess, sys

# Check boltz importable
result = subprocess.run([sys.executable, '-c', 'import boltz; print(boltz.__version__)'],
                       capture_output=True, text=True)
print("boltz import:", result.stdout.strip() or result.stderr.strip()[:200])

# Check the YAML input is still present
import os
yaml_path = '/home/ubuntu/rayca-sessions/2d89c255-6bf5-4e5c-a4fb-99e4f253a979-1320c8c41b74/ARV471_ERalpha_CRBN_boltz_input.yaml'
print(f"Input YAML exists: {os.path.exists(yaml_path)}")

# Check GPU availability (cpu-only expected)
result2 = subprocess.run([sys.executable, '-c', 
    'import torch; print("CUDA:", torch.cuda.is_available(), "| device_count:", torch.cuda.device_count())'],
    capture_output=True, text=True)
print(result2.stdout.strip() or result2.stderr.strip()[:200])
