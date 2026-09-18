
import shutil, pathlib

BASE    = pathlib.Path('/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b')
SYS_DIR = BASE / 'md' / 'systems'
STAGE   = BASE / 'md' / 'stage'
STAGE.mkdir(exist_ok=True)

LIGS = ['REF_85C','CPD1','CPD4','CPD7','CPD8','CPD9','CPD10','CPD11','CPD12']

stage_files = []
for lig in LIGS:
    for ext in ['prmtop', 'inpcrd']:
        src = SYS_DIR / lig / f'system.{ext}'
        dst = STAGE / f'{lig}.{ext}'
        shutil.copy2(src, dst)
        stage_files.append(str(dst))
        print(f"  {dst.name} ({dst.stat().st_size//1024} KB)")

print(f"\n{len(stage_files)} files ready to stage, total {sum(pathlib.Path(f).stat().st_size for f in stage_files)/1e6:.0f} MB")
