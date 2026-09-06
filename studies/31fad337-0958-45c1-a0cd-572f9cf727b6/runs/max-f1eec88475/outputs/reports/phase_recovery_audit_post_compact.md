---
title: "Recovery Audit — Post-Compaction State Verification"
study_id: "31fad337-0958-45c1-a0cd-572f9cf727b6"
run_id: "max-f1eec88475"
phase_goal: "Verify session state is intact after context compaction; confirm all prior phase outputs exist on disk before proceeding to GitHub push."
status: "complete"
date: "2026-09-06"
model: "claude-sonnet-4-6"
---

# Recovery Audit — Post-Compaction State Verification

## Context

Session context was compacted after completion of all computational work (84-compound campaign, NC compound design, NC docking, NC MM-GBSA, combined PDB assembly). This audit verifies that all expected outputs are present on disk before the pending GitHub push.

---

## File Verification

| File | Expected size | On disk | Status |
|:---|:---:|:---:|:---:|
| `cdk2_campaign/CDK2_CyclinE1_NC_complex.pdb` | ~402 KB | 402 KB | CONFIRMED |
| `cdk2_campaign/CDK2_CyclinE1_84compounds_docking_mmgbsa.sdf` | ~375 KB | 375 KB | CONFIRMED |
| `cdk2_campaign/nc_mmgbsa_results.json` | 10 compounds | 10 entries | CONFIRMED |
| `cdk2_campaign/nc_docking_results.json` | 10 compounds | 10 entries | CONFIRMED |
| `cdk2_campaign/poses_all/NC-*_best_pose.sdf` | 10 files | 10 files | CONFIRMED |
| `cdk2_campaign/poses_all_H/NC-*_best_pose_H.sdf` | 10 files | 10 files | CONFIRMED |
| `reports/phase_nc_docking_mmgbsa.md` | present | present | CONFIRMED |
| `reports/phase_new_compound_design_cdk2_cycline1.md` | present | present | CONFIRMED |
| `reports/phase_merged_sdf_84compounds.md` | present | present | CONFIRMED |

## Key Results Re-confirmed

- **NC-010**: best MM-GBSA dG = −84.633 kcal/mol (campaign-wide best), CNN pKi = 8.792, rc=0, gpu=True
- **84-compound SDF**: all compounds annotated with docking + MM-GBSA properties, MM-GBSA rank order
- **Combined PDB**: receptor (chains A+B) + crystal ligand (chain X LIG 900) + NC-001–NC-010 poses (chain X L01–L0A, resSeq 901–910)

## Pending

GitHub push to `RSA-Edelris/RaycaBio` is blocked pending user-provided GitHub PAT (no `gh` CLI, no SSH key with GitHub access, no GITHUB_TOKEN in environment). Awaiting credentials.

---

## Verification

| Claim | Source | Verified value | Result |
|:---|:---|:---|:---:|
| CDK2_CyclinE1_NC_complex.pdb present | `ls -lh` | 402 KB, mtime Sep 6 17:58 | CONFIRMED |
| CDK2_CyclinE1_84compounds_docking_mmgbsa.sdf present | `ls -lh` | 375 KB, mtime Sep 6 14:32 | CONFIRMED |
| 10/10 NC best_pose.sdf present | `ls \| wc -l` | 10 | CONFIRMED |
| 10/10 NC best_pose_H.sdf present | `ls \| wc -l` | 10 | CONFIRMED |
| NC-010 nc_mmgbsa_results.json rank-1 dG | json read | −84.633 kcal/mol, status=S, rc=0 | CONFIRMED |
| All prior phase documents present | `ls reports/*.md` | 20+ documents | CONFIRMED |
