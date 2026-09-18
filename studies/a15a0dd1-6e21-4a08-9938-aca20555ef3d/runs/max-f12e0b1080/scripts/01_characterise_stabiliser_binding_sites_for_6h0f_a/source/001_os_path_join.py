
import subprocess, os, urllib.request, gzip, shutil

session_dir = "/home/ubuntu/rayca-sessions/a15a0dd1-6e21-4a08-9938-aca20555ef3d-d5f60ea7d2e1"
struct_dir = os.path.join(session_dir, "structures")
os.makedirs(struct_dir, exist_ok=True)

def fetch_pdb(pdb_id, out_dir):
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    out_path = os.path.join(out_dir, f"{pdb_id}.pdb")
    if not os.path.exists(out_path):
        urllib.request.urlretrieve(url, out_path)
    return out_path

p6h0f = fetch_pdb("6H0F", struct_dir)
p2o98 = fetch_pdb("2O98", struct_dir)
print("Downloaded:", p6h0f)
print("Downloaded:", p2o98)
print("Sizes:", os.path.getsize(p6h0f), os.path.getsize(p2o98))
