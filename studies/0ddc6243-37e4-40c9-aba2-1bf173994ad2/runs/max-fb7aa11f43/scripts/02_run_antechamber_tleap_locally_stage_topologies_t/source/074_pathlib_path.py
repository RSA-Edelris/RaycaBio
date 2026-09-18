
import pathlib, re

gaff2_dat = pathlib.Path("/home/ubuntu/rayca-runtime/.mamba/envs/rayca/dat/leap/parm/gaff2.dat")
text = gaff2_dat.read_text()

# Find DIHE section
dihe_start = text.index("DIHE")
dihe_end   = text.index("\n\n", dihe_start)
dihe_block = text[dihe_start:dihe_end]

# Show first few lines to understand format
print("FORMAT SAMPLE:")
for l in dihe_block.splitlines()[:5]:
    print(repr(l))

# Search for entries
print("\nSearching for c1 / ce-n / ns / X-X torsion analogues:")
for l in dihe_block.splitlines()[1:]:
    if not l.strip(): continue
    # atom types are first 11 chars, space-separated with dashes
    m = re.match(r'^(\S+)-(\S+)-(\S+)-(\S+)\s', l)
    if not m: continue
    t = tuple(m.groups())
    if any(x in t for x in ('c1','X')) or \
       (t[0] in ('c','ce') and t[2] in ('n','ns')) or \
       (t[1] in ('c','ce') and t[2] in ('n','ns')):
        print(l)
