import os, sys, glob
import torch
from omegaconf import OmegaConf
from hydra.utils import instantiate

WEIGHTS = "/projects/u6sp/containers/boltzgen_weights"
BOLTZ2_CKPT = f"{WEIGHTS}/models--boltzgen--boltzgen-1/snapshots/c1be29e1f82ffcc72264f64b993c43fb4e0d17f0/boltz2_conf_final.ckpt"
MOLDIR = f"{WEIGHTS}/datasets--boltzgen--inference-data/snapshots/c3d36fd276e9caf098c75d4113c6d5eb320b1a4c/mols.zip"
RAYCA_OUT = os.environ["RAYCA_OUT"]
YAML_PATH = f"{RAYCA_OUT}/gspt1_crbn_glue.yaml"
OUTDIR = f"{RAYCA_OUT}/ternary_out"
os.makedirs(OUTDIR, exist_ok=True)

# ── Patch: pair_chains_iptm falls back to zeros tensor; merging loop expects dict ──
from boltzgen.model.modules import confidence as conf_mod
_orig = conf_mod.ConfidenceModule.forward

def _patched(self, s_inputs, s, z, x_pred, feats, pred_distogram_logits,
             multiplicity=1, s_diffusion=None, run_sequentially=False, use_kernels=False):
    if run_sequentially and multiplicity > 1:
        assert z.shape[0] == 1
        out_dicts = []
        for i in range(multiplicity):
            sd = s_diffusion[i:i+1] if s_diffusion is not None else None
            out_dicts.append(_patched(
                self, s_inputs, s, z, x_pred[i:i+1], feats, pred_distogram_logits,
                multiplicity=1, s_diffusion=sd, run_sequentially=False, use_kernels=use_kernels))
        out_dict = {}
        for key in out_dicts[0]:
            vals = [out[key] for out in out_dicts]
            if key not in ("pair_chains_iptm", "chain_pair_ipsae") or isinstance(vals[0], torch.Tensor):
                out_dict[key] = torch.cat(vals, dim=0)
            else:
                pd = {}
                for c1 in vals[0]:
                    cd = {c2: torch.cat([v[c1][c2] for v in vals], dim=0) for c2 in vals[0][c1]}
                    pd[c1] = cd
                out_dict[key] = pd
        return out_dict
    return _orig(self, s_inputs, s, z, x_pred, feats, pred_distogram_logits,
                 multiplicity=multiplicity, s_diffusion=s_diffusion,
                 run_sequentially=run_sequentially, use_kernels=use_kernels)

conf_mod.ConfidenceModule.forward = _patched
print("Confidence module patched", flush=True)

# ── Config ────────────────────────────────────────────────────────────────────
CONFIG_DIR = "/opt/boltzgen/venv/lib/python3.12/site-packages/boltzgen/resources/config"
cfg = OmegaConf.load(f"{CONFIG_DIR}/design.yaml")
cfg = OmegaConf.merge(cfg, OmegaConf.create({
    "checkpoint": BOLTZ2_CKPT,
    "output": OUTDIR,
    "name": "gspt1_crbn_glue",
    "diffusion_samples": 3,
    "sampling_steps": 200,
    "recycling_steps": 3,
    "matmul_precision": "high",
    "data": {"cfg": {
        "yaml_path": YAML_PATH,
        "moldir": MOLDIR,
        "output_dir": OUTDIR,
        "multiplicity": 1,
        "diffusion_samples": 3,
        "atom14": True, "atom37": False, "backbone_only": False,
        "design": True, "disulfide_prob": 1.0, "disulfide_on": True,
    }},
    "override": {"masker_args": {"mask": True, "mask_backbone": True}, "validators": None},
}))

task = instantiate(cfg, _recursive_=True)
print(f"predict_set length: {len(task.data.predict_set)}", flush=True)
task.run()
print("Prediction done", flush=True)

# ── CIF → PDB ─────────────────────────────────────────────────────────────────
import gemmi
cifs = sorted(glob.glob(f"{OUTDIR}/**/*.cif", recursive=True))
print(f"\nConverting {len(cifs)} CIF file(s) to PDB ...", flush=True)
for cif_path in cifs:
    try:
        st = gemmi.read_structure(cif_path)
        st.remove_alternative_conformations()
        pdb_path = cif_path.replace(".cif", ".pdb")
        st.write_pdb(pdb_path)
        sz = os.path.getsize(pdb_path)
        print(f"  OK  {os.path.basename(pdb_path)}  ({sz:,} bytes)", flush=True)
    except Exception as e:
        print(f"  FAIL {cif_path}: {e}", flush=True)

print("\n=== All output files ===")
for root, _, files in os.walk(OUTDIR):
    for f in sorted(files):
        p = os.path.join(root, f)
        print(f"  {p}  ({os.path.getsize(p):,} bytes)")
