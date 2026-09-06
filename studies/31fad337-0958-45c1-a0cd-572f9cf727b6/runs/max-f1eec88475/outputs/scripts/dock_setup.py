
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from modulon.governance.toolkit import run_aidd_tool

WDIR    = Path("/home/ubuntu/rayca-sessions/31fad337-0958-45c1-a0cd-572f9cf727b6-0505c6de016f/cdk2_campaign")
REC     = str(WDIR / "receptor_raw.pdb")
LIG_DIR = str(WDIR / "ligands_prepared")
CK_FILE = WDIR / "docking_checkpoint.json"

BOX = dict(boxX=30.57, boxY=5.37, boxZ=-25.80, width=35, height=30, depth=31,
           numModes=5, cnnScoring="rescore", exhaustiveness=8, seed=42)

ALL_LIGANDS = ["CTX-1020903","CTX-1020667","CTX-1019480","CTX-1020747","CTX-1020518",
               "CTX-1020810","CTX-1020516","CTX-1020741","CTX-1020750","CTX-1020734",
               "CTX-1019758","CTX-1019473","CTX-1020456","CTX-1020698","CTX-1020800",
               "CTX-1020670","CTX-1020696","CTX-1020743","CTX-1020565","CTX-1020749",
               "CTX-1020453","CTX-1020459","CTX-1020669","CTX-1020562","CTX-1020582",
               "CTX-1019613","CTX-1017233","CTX-1020454","CTX-1020695","CTX-1020748",
               "CTX-1020517","CTX-1020520","CTX-1020740","CTX-1019471","CTX-1020753",
               "CTX-1020671","CTX-1020697","CTX-1020566","CTX-1019757","CTX-1020882",
               "CTX-1020458","CTX-1020746","CTX-1020733","CTX-1020521","CTX-1019496",
               "CTX-1020842","CTX-1020440","CTX-1020838","CTX-1019813","CTX-1020555",
               "CTX-1020523","CTX-1020441","CTX-1019660","CTX-1020799","CTX-1019904",
               "CTX-1020817","CTX-1019630","CTX-1020739","CTX-1020816","CTX-1020732",
               "CTX-1020755","CTX-1020772","CTX-1020742","CTX-1020771","CTX-1020811",
               "CTX-1020795","CTX-1020699","CTX-1020770","CTX-1020745","CTX-1020818",
               "CTX-1020744","CTX-1020766","CTX-1020735","CTX-1020759","CTX-1020769",
               "CTX-1020902","CTX-1020912","CTX-1020754","CTX-1020685","CTX-1020726",
               "CTX-1020845","CTX-1020752","CTX-1020767","CTX-1020751"]

def load_checkpoint():
    return json.loads(CK_FILE.read_text())

def save_checkpoint(ck):
    CK_FILE.write_text(json.dumps(ck, indent=2))

def dock_one(name, ck):
    try:
        r = run_aidd_tool("gnina", {
            "proteinFile": REC, "ligandFile": f"{LIG_DIR}/{name}.sdf", **BOX})
        o = r.get("output", {})
        return {"name": name,
                "best_affinity":     o.get("best_affinity_kcal_mol"),
                "best_cnn_affinity": o.get("best_cnn_affinity"),
                "best_cnn_pose":     o.get("best_cnn_pose_score"),
                "num_poses":         o.get("num_poses", 0),
                "gpu_used":          o.get("gpu_used", False),
                "output_file":       o.get("output_file", ""),
                "poses":             o.get("poses", []),
                "error":             ""}
    except Exception as e:
        return {"name": name, "best_affinity": None, "best_cnn_affinity": None,
                "best_cnn_pose": None, "num_poses": 0, "gpu_used": False,
                "output_file": "", "poses": [], "error": str(e)}

def run_batch(batch_names):
    ck = load_checkpoint()
    with ThreadPoolExecutor(max_workers=15) as ex:
        futures = {ex.submit(dock_one, n, ck): n for n in batch_names}
        for fut in as_completed(futures):
            r = fut.result()
            ck[r["name"]] = r
            save_checkpoint(ck)
            print(f"  {r['name']}: Vina={r['best_affinity']}  CNN={r['best_cnn_affinity']}  err={r['error']!r}")
    return ck

def pending_ligands():
    ck = load_checkpoint()
    return [n for n in ALL_LIGANDS if ck.get(n, {}).get("best_affinity") is None]
