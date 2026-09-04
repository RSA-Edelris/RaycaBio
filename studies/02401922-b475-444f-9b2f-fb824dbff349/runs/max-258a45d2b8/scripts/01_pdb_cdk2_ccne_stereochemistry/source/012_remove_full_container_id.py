
import subprocess, time

# Remove by full container ID
cid = '5f1a736a884160c8f6d28e119f40f9c71a06aa599e154a6c7eceaf2662318dc8'
r = subprocess.run(['docker', 'rm', '-f', cid], capture_output=True, text=True)
print("rm by ID:", r.stdout.strip(), r.stderr.strip())

# Also check all gnina containers
r2 = subprocess.run(['docker', 'ps', '-a', '--filter', 'name=gnina', '--format', '{{.ID}} {{.Names}} {{.Status}}'],
                    capture_output=True, text=True)
print("gnina containers:", r2.stdout.strip() or "none")
