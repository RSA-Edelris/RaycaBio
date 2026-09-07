
import sys
sys.path.insert(0, MMGBSA_DIR)
from mmgbsa_pipeline import prepare_receptor, run_antechamber, run_parmchk2

# Step 0: prepare receptor once
rec_pdb = prepare_receptor()
