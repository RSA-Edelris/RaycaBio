import os, sys
from pathlib import Path
from omegaconf import OmegaConf
from hydra.utils import instantiate

WEIGHTS = "/projects/u6sp/containers/boltzgen_weights"
BOLTZ2_CKPT = f"{WEIGHTS}/models--boltzgen--boltzgen-1/snapshots/c1be29e1f82ffcc72264f64b993c43fb4e0d17f0/boltz2_conf_final.ckpt"
MOLDIR = f"{WEIGHTS}/datasets--boltzgen--inference-data/snapshots/c3d36fd276e9caf098c75d4113c6d5eb320b1a4c/mols.zip"
RAYCA_OUT = os.environ.get("RAYCA_OUT", "/scratch")
YAML_PATH = f"{RAYCA_OUT}/gspt1_crbn_glue.yaml"
OUTDIR = f"{RAYCA_OUT}/ternary_out"
os.makedirs(OUTDIR, exist_ok=True)

CONFIG_DIR = "/opt/boltzgen/venv/lib/python3.12/site-packages/boltzgen/resources/config"
cfg = OmegaConf.load(f"{CONFIG_DIR}/design.yaml")

overrides = OmegaConf.create({
    "checkpoint": BOLTZ2_CKPT,
    "output": OUTDIR,
    "name": "gspt1_crbn_glue",
    "diffusion_samples": 3,
    "sampling_steps": 200,
    "recycling_steps": 3,
    "matmul_precision": "high",
    "data": {
        "cfg": {
            "yaml_path": YAML_PATH,
            "moldir": MOLDIR,
            "output_dir": OUTDIR,
            "multiplicity": 1,
            "diffusion_samples": 3,
            "atom14": True,
            "atom37": False,
            "backbone_only": False,
            "design": True,
            "disulfide_prob": 1.0,
            "disulfide_on": True,
        }
    },
    "override": {
        "masker_args": {
            "mask": True,
            "mask_backbone": True,
        },
        "validators": None,
    }
})

cfg = OmegaConf.merge(cfg, overrides)
print("=== Config ===")
print(OmegaConf.to_yaml(cfg))
sys.stdout.flush()

print("=== Instantiating task ===")
sys.stdout.flush()
task = instantiate(cfg, _recursive_=True)

print(f"=== predict_set length: {len(task.data.predict_set)} ===")
sys.stdout.flush()

print("=== Running Boltz-2 prediction ===")
sys.stdout.flush()
task.run()
print(f"=== DONE. Results in: {OUTDIR} ===")

import os
for root, dirs, files in os.walk(OUTDIR):
    for f in files:
        fpath = os.path.join(root, f)
        print(f"  OUTPUT: {fpath}  ({os.path.getsize(fpath)} bytes)")
