import numpy as np, os

WORK = os.environ['AMBER_WORK']
LIGS = ["REF_85C","CPD1","CPD4","CPD7","CPD8"]

def load_last_half(path, col=1):
    try:
        d = np.loadtxt(path, comments='#')
        if d.ndim == 1: d = d[None,:]
        n = max(1, len(d)//2)
        return d[-n:, col]
    except:
        return None

def fmt(arr):
    if arr is None: return '   N/A  '
    return f'{np.mean(arr):5.2f}+/-{np.std(arr):.2f}'

print(f"\n{'Compound':<12} {'LigRMSD(A)':>11} {'CRBN_W380(A)':>13} {'GSPT1_K628(A)':>14} {'PPI(A)':>8}  Verdict")
print('-'*75)
for lig in LIGS:
    rmsd = load_last_half(f'{WORK}/analysis/{lig}_lig_rmsd.dat')
    crbn = load_last_half(f'{WORK}/analysis/{lig}_crbn_anchor.dat')
    gspt = load_last_half(f'{WORK}/analysis/{lig}_gspt1_bridge.dat')
    ppi  = load_last_half(f'{WORK}/analysis/{lig}_ppi_com.dat')
    if rmsd is None:
        verdict = 'NO_DATA'
    elif (np.mean(rmsd)<4.0 and crbn is not None and np.mean(crbn)<10.0
          and gspt is not None and np.mean(gspt)<12.0):
        verdict = 'STABLE_GLUE'
    elif np.mean(rmsd)<4.0 and crbn is not None and np.mean(crbn)<10.0:
        verdict = 'CRBN_only'
    else:
        verdict = 'unstable'
    print(f'{lig:<12} {fmt(rmsd):>11} {fmt(crbn):>13} {fmt(gspt):>14} {fmt(ppi):>8}  {verdict}')
