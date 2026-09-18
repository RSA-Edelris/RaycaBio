
import pandas as pd

# Build R-group annotation dict from source
rg = {
 "A01": ("2-CF3EtO-py5",     "2-pyrrolyl-Bn"),
 "A02": ("2-CF3EtO-py5",     "4-piperazino-Bn"),
 "A03": ("2-CF3EtO-py5",     "4-NMePiperazino-Bn"),
 "A04": ("2-CF3EtO-py5",     "4-morpholino-Bn"),
 "A05": ("2-CF3EtO-py5",     "pyrimidin-5-CH2"),
 "A06": ("2-CF3EtO-py5",     "pyridin-4-CH2"),
 "A07": ("2-CF3EtO-py5",     "4-F-Bn"),
 "A08": ("2-CF3EtO-py5",     "4-CF3-Bn"),
 "A09": ("2-CF3EtO-py5",     "4,4-diF-cHex"),
 "B01": ("benzofuran-2-yl",  "2-pyrrolyl-Bn"),
 "B02": ("benzofuran-2-yl",  "4-piperazino-Bn"),
 "B03": ("benzofuran-2-yl",  "4-morpholino-Bn"),
 "B04": ("benzofuran-2-yl",  "pyrimidin-5-CH2"),
 "B05": ("benzofuran-2-yl",  "4,4-diF-cHex"),
 "C01": ("benzothiophen-2-yl","2-pyrrolyl-Bn"),
 "C02": ("benzothiophen-2-yl","4-piperazino-Bn"),
 "C03": ("benzothiophen-2-yl","4,4-diF-cHex"),
 "D01": ("5-CF3-pyridin-3-yl","2-pyrrolyl-Bn"),
 "D02": ("5-CF3-pyridin-3-yl","4-piperazino-Bn"),
 "D03": ("5-CF3-pyridin-3-yl","4,4-diF-cHex"),
 "E01": ("2-OMe-naphthyl",   "2-pyrrolyl-Bn"),
 "E02": ("2-OMe-naphthyl",   "4-piperazino-Bn"),
 "E03": ("2-OMe-naphthyl",   "4,4-diF-cHex"),
 "F01": ("quinolin-3-yl",    "2-pyrrolyl-Bn"),
 "F02": ("quinolin-3-yl",    "4-piperazino-Bn"),
 "G01": ("4-F-phenyl",       "2-pyrrolyl-Bn"),
 "G02": ("4-F-phenyl",       "4-piperazino-Bn"),
 "G03": ("4-F-phenyl",       "4,4-diF-cHex"),
 "H01": ("2-OMe-pyridin-5-yl","2-pyrrolyl-Bn"),
 "H02": ("2-OMe-pyridin-5-yl","4-piperazino-Bn"),
 "I01": ("4-CF3-phenyl",     "2-pyrrolyl-Bn"),
 "I02": ("4-CF3-phenyl",     "4-piperazino-Bn"),
 "J01": ("furo[2,3-b]pyridin-2-yl","4-piperazino-Bn"),
 "J02": ("benzo[d]isoxazol-3-yl","2-pyrrolyl-Bn"),
 "J03": ("2-CF3EtO-py5",     "3-CN-Bn"),
 "J04": ("2-CF3EtO-py5",     "4-NMe2-Bn"),
 "J05": ("3-Cl-5-CF3-phenyl","2-pyrrolyl-Bn"),
 "J06": ("2-CF3EtO-py5",     "2-(4-MePiperazino)pyrimidin-5-CH2"),
}

des_pass['R1'] = des_pass['name'].map(lambda n: rg[n][0])
des_pass['R2'] = des_pass['name'].map(lambda n: rg[n][1])

print("=== TOP CANDIDATES FOR SYNTHESIS (ADME PASS, RANKED BY VINA) ===\n")
print(f"{'Rank':<5} {'ID':<5} {'R1':<25} {'R2':<22} {'Vina':>7} {'CNN_pKi':>8} "
      f"{'MW':>6} {'logP':>5} {'TPSA':>5} {'RotB':>5}")
print("-"*105)
for _, r in des_pass.iterrows():
    print(f"  {int(r.synth_rank):<3}  {r['name']:<5}  {r.R1:<25}  {r.R2:<22}  "
          f"{r.vina:>7.2f}  {r.cnn_aff:>7.3f}  {r.mw:>6.0f}  {r.logp:>5.2f}  "
          f"{r.tpsa:>5.1f}  {int(r.rotb):>4}")

# Also show actives with docking scores
print("\n\n=== ASMS ACTIVES — DOCKING SCORES ===")
act_m2 = act_m.copy()
act_m2['as_ratio'] = act_m2['name'].map(
    lambda n: next((m.GetProp('AS_ratio') for m in 
                    list(__import__('rdkit').Chem.SDMolSupplier(
                        f'{wd}/batch_actives.sdf')) if m and m.GetProp('_Name')==n), 'N/A'))
print(act_m2[['name','vina','cnn_aff','as_ratio','mw','logp','tpsa']].sort_values('vina').to_string(index=False))
