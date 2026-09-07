
import json, os

WF_JOURNAL = "/home/ubuntu/.claude/projects/-home-ubuntu-rayca-sessions-74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e/1f061ffd-3f88-4145-9734-5371128e7cb5/subagents/workflows/wf_51656335-806/journal.jsonl"

# ── collect 29 results from workflow journal ──────────────────────────────────
all_scores = {}
with open(WF_JOURNAL) as f:
    for line in f:
        try:
            obj = json.loads(line.strip())
            if obj.get('type') == 'result' and 'result' in obj:
                r = obj['result']
                if isinstance(r, dict) and 'name' in r:
                    all_scores[r['name']] = {
                        'affinity':        r.get('best_affinity_kcal_mol'),
                        'cnn_affinity':    r.get('best_cnn_affinity'),
                        'cnn_pose_score':  r.get('best_cnn_pose_score'),
                        'num_poses':       r.get('num_poses'),
                        'gpu_used':        r.get('gpu_used'),
                    }
        except:
            pass

print(f"From workflow journal: {len(all_scores)} entries")

# ── add 3 direct runs ─────────────────────────────────────────────────────────
for name, res in missing_results.items():
    out = res.get('output', {})
    all_scores[name] = {
        'affinity':       out.get('best_affinity_kcal_mol'),
        'cnn_affinity':   out.get('best_cnn_affinity'),
        'cnn_pose_score': out.get('best_cnn_pose_score'),
        'num_poses':      out.get('num_poses'),
        'gpu_used':       out.get('gpu_used'),
    }

print(f"Total after adding 3 direct runs: {len(all_scores)} entries")

# ── sort by Vina affinity ─────────────────────────────────────────────────────
ranked = sorted(all_scores.items(), key=lambda x: x[1]['affinity'] or 0)
print("\nRank  Compound                   Vina(kcal/mol)  CNN_aff   CNN_pose")
print("-" * 65)
for i, (name, s) in enumerate(ranked, 1):
    print(f"{i:3d}  {name:27s}  {s['affinity']:>8.2f}   {s['cnn_affinity']:>6.3f}  {s['cnn_pose_score']:>8.4f}")

# save to file for later use
with open(f"{WORK}/docking_scores_all32.json", 'w') as f:
    json.dump(all_scores, f, indent=2)
print("\nSaved docking_scores_all32.json")
