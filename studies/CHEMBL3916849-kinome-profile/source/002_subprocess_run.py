
import subprocess
result = subprocess.run(['find', '/data', '/home', '/opt', '-name', '*.sqlite', '-o', '-name', 'chembl*'], 
                      capture_output=True, text=True, timeout=15)
print(result.stdout[:3000])
print("STDERR:", result.stderr[:500])
