# Audit: add_interactions — docking_viewer.html

Audited file: `docking_viewer.html`  
File size: ~292 KB  
Audit date: 2026-09-03  

---

## Verification

| # | Check | Status | Evidence |
|:--|:------|:------:|:---------|
| 1 | `const INTERACTIONS` defined once with all 6 keys | PASS | Defined once at line 5670; keys EDS01357518_ent1 (5671), EDS01357518_ent2 (5682), EDS01806218_ent1 (5693), EDS01806218_ent2 (5705), EDS01889984 (5718), crystal_lvy (5729) all present |
| 2 | Each entry has `hbonds` and `pistack` arrays | PASS | All 6 keys contain `"hbonds": [...]` and `"pistack": [...]`; crystal_lvy has an empty pistack array `[]`, which is valid |
| 3 | Each hbond/pistack entry has `start`, `end` (both with x/y/z), and `label` fields | PASS | All entries follow the pattern `{start:{x:…,y:…,z:…}, end:{x:…,y:…,z:…}, label:"…"}`; verified across ent1/ent2/crystal_lvy hbonds and pistack entries |
| 4 | `let showInteractions` state variable exists | PASS | Line 5753: `let showInteractions = true;` |
| 5 | `viewer.removeAllShapes()` called inside `rebuildScene()` | PASS | `rebuildScene()` starts at line 5828; `viewer.removeAllShapes();` is at line 5831, third line of the function body |
| 6 | `function drawInteractions(data)` defined; calls `viewer.addLine` for hbonds and `viewer.addCylinder` for pistack | PASS | Function defined at line 5892; `viewer.addLine({...})` at line 5898 (hbond loop); `viewer.addCylinder({...})` at line 5921 (pistack loop) |
| 7 | `function toggleInteractions()` defined and flips `showInteractions` | PASS | Defined at line 5941; line 5942: `showInteractions = !showInteractions;` |
| 8 | `drawInteractions(...)` called inside `rebuildScene()` after pose models are loaded | PASS | Pose models loaded in lines 5850–5864; `drawInteractions(INTERACTIONS[currentCompound])` called at line 5885, before the final `viewer.render()` at line 5887 |
| 9 | Button with `id="btn-interactions"` exists in controls bar HTML | PASS | Line 254: `<button class="btn active" id="btn-interactions" onclick="toggleInteractions()">H-bond / π</button>` |
| 10 | H-bond lines use color `#06b6d4`; π-stack cylinders use color `#c026d3` | PASS | Line 5900: `color: '#06b6d4', dashed: true, linewidth: 2`; line 5923: `color: '#c026d3', opacity: 0.8` |
| 11 | Distance labels added at midpoint of H-bond lines | PASS | Lines 5902–5916: midpoint computed from `(hb.start + hb.end)/2`, Euclidean distance `d` calculated, `viewer.addLabel(hb.label + ' ' + d + 'Å', {position: mid, …})` called |
| 12 | `drawInteractions` also called from `toggleInteractions()` | PASS | Line 5944: `drawInteractions(currentCompound ? INTERACTIONS[currentCompound] : null);` |

---

All 12 checks passed. The interaction overlay (H-bonds and π-stacking) was correctly implemented: the data structure is complete and well-formed for all six compounds, the draw/toggle logic is wired up properly, and colors, labels, and scene lifecycle calls all conform to the specification.
