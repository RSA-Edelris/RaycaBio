
# Search all scripts in subdirectories for box/center params
import glob

all_scripts = glob.glob(os.path.join(ws, '**', '*.py'), recursive=True)
print(f"Total scripts: {len(all_scripts)}")

for s in sorted(all_scripts):
    try:
        txt = open(s).read()
        if any(k in txt for k in ('centerX','centerY','sizeX','boxX','center_x','size_x','boxCenter','box_center')):
            print(f"\n=== {os.path.relpath(s, ws)} ===")
            for line in txt.splitlines():
                if any(k in line for k in ('center','size','box','X','Y','Z')):
                    stripped = line.strip()
                    if stripped and not stripped.startswith('#'):
                        print(f"  {stripped}")
    except:
        pass
