
# Write the fixed receptor PDB with corrected HIS → HID/HIE naming
out_lines = []
for line in lines:
    if not line.startswith(('ATOM', 'HETATM')):
        out_lines.append(line)
        continue
    res_name = line[17:20].strip()
    if res_name != 'HIS':
        out_lines.append(line)
        continue
    chain = line[21]
    resseq = line[22:26].strip()
    new_name = his_rename.get((chain, resseq), 'HIE')
    # Replace columns 17-19 (0-indexed) with new name, padded to 3 chars
    new_line = line[:17] + new_name.ljust(3) + line[20:]
    out_lines.append(new_line)

rec_out.write_text('\n'.join(out_lines) + '\n')
print(f"Written {rec_out} ({rec_out.stat().st_size} bytes)")

# Verify
import subprocess
r = subprocess.run(
    ['grep', '-c', 'HIS', str(rec_out)],
    capture_output=True, text=True
)
print(f"Remaining HIS: {r.stdout.strip()}")
r2 = subprocess.run(['grep', '-c', 'HID', str(rec_out)], capture_output=True, text=True)
r3 = subprocess.run(['grep', '-c', 'HIE', str(rec_out)], capture_output=True, text=True)
print(f"HID lines: {r2.stdout.strip()}, HIE lines: {r3.stdout.strip()}")
