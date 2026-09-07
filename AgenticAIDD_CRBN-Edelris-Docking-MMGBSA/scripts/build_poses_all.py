#!/usr/bin/env python3
"""
Build poses_all.sdf — all top-5 docking poses for every compound in the session.

Sources:
  best_poses2/*.sdf          — 22 CRBN_ID_enantio_2 stereoisomers (10 poses each → take top 5)
  poses/*.sdf.gz             — 32 EDEL-CRBN compounds  (5 poses each)

Added SD tags per record (injected as raw text, no RDKit re-write):
  Compound_Name              — identifier
  Pose_Rank                  — 1..5

For the 22-compound set, per-pose gnina scores from docking2_results.json are also injected:
  Docking_Affinity_kcal_mol
  CNN_Affinity
  CNN_Pose_Score
"""

import gzip, json
from pathlib import Path

BASE     = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")
OUT_FILE = BASE / "poses_all.sdf"

docking2 = json.loads((BASE / "docking2_results.json").read_text())

def split_sdf(text):
    """Split SDF text into individual record strings.

    Handles gnina's embedded-$$$$ contamination: gnina writes a $$$$ inside
    the property block (between biological tags and its own score tags), then a
    real $$$$ at the end.  Any fragment that contains no 'M  END' has no mol
    block and is a contaminated continuation of the previous record — it is
    merged back rather than kept as a separate entry.
    """
    raw = []
    current = []
    for line in text.splitlines():
        if line.strip() == "$$$$":
            if current:
                raw.append("\n".join(current))
                current = []
        else:
            current.append(line)
    if current:
        raw.append("\n".join(current))

    # Merge contaminated (mol-less) fragments into the preceding real record.
    records = []
    for frag in raw:
        if "M  END" in frag:
            records.append(frag)
        else:
            if records:
                records[-1] = records[-1] + "\n\n" + frag
    return records

def inject_tags(record_text, tags: dict) -> str:
    """Append SD tag blocks to a mol record.

    Normalise the record to end with exactly one blank line so the first
    injected tag is always separated from any existing property values by
    a blank line, as required by the SDF spec.
    """
    tag_block = "\n".join(
        f"> <{k}>\n{v}\n" for k, v in tags.items()
    )
    # SDF requires a blank line after the last property value before $$$$
    return record_text.rstrip("\n") + "\n\n" + tag_block + "\n$$$$\n"

total = 0
with open(OUT_FILE, "w") as out:

    # ── 22 CRBN_ID_enantio_2 stereoisomers ─────────────────────────────────
    sdf_files = sorted((BASE / "best_poses2").glob("*_poses.sdf"))
    for sdf_path in sdf_files:
        name = sdf_path.stem.replace("_poses", "")
        text = sdf_path.read_text()
        records = split_sdf(text)

        # Per-pose scores from docking2_results.json
        dock = docking2.get(name, {})
        pose_scores = {p["rank"]: p for p in dock.get("poses", [])}

        for rank, rec in enumerate(records[:5], start=1):  # top 5 only
            ps = pose_scores.get(rank, {})
            tags = {
                "Compound_Name":             name,
                "Pose_Rank":                 str(rank),
                "Docking_Affinity_kcal_mol": str(ps.get("affinity", "N/A")),
                "CNN_Affinity":              str(ps.get("cnn_affinity", "N/A")),
                "CNN_Pose_Score":            str(ps.get("cnn_pose_score", "N/A")),
            }
            out.write(inject_tags(rec, tags))
            total += 1

    print(f"22-compound set: {total} poses written")

    # ── 32 EDEL-CRBN compounds ───────────────────────────────────────────────
    gz_files = sorted((BASE / "poses").glob("*.sdf.gz"))
    gz_total = 0
    for gz_path in gz_files:
        # Derive compound name from filename (strip _poses.sdf.gz)
        stem = gz_path.name
        for suffix in ("_poses.sdf.gz", ".sdf.gz"):   # longest first
            if stem.endswith(suffix):
                stem = stem[: -len(suffix)]
                break
        name = stem

        with gzip.open(gz_path, "rt") as fh:
            text = fh.read()
        records = split_sdf(text)

        for rank, rec in enumerate(records[:5], start=1):
            tags = {
                "Compound_Name": name,
                "Pose_Rank":     str(rank),
            }
            out.write(inject_tags(rec, tags))
            gz_total += 1

    print(f"32-compound set: {gz_total} poses written")

total_all = total + gz_total
print(f"\nTotal records: {total_all}  (expected 22×5 + 32×5 = {22*5 + 32*5})")
print(f"Output: {OUT_FILE}  ({OUT_FILE.stat().st_size:,} bytes)")

# Quick sanity: count $$$$ separators
sdf_text = OUT_FILE.read_text()
n_records = sdf_text.count("$$$$")
print(f"$$$$ count in output: {n_records}  ({'OK' if n_records == total_all else 'MISMATCH'})")
