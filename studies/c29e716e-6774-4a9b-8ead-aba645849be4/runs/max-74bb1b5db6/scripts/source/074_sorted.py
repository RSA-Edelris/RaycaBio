
import json, glob

ws = '/home/ubuntu/rayca-sessions/c29e716e-6774-4a9b-8ead-aba645849be4-01def6985d02'

# Read all autodock-vina result files in order
result_files = sorted(glob.glob(f'{ws}/autodock-vina-results*.json'))
print("Result files found:")
for rf in result_files:
    with open(rf) as f:
        d = json.load(f)
    print(f"  {rf.split('/')[-1]}: best={d.get('best_affinity_kcal_mol')} | {d.get('summary','')[:80]}")
