
# Check /dev/shm size inside a container by running a quick shell command via the tool
# We'll use the sanity check result to find the container name, or just test directly
# Check via a lightweight probe
import subprocess, shutil

# The containers run on the platform - let's check local /dev/shm as a proxy
# and look at the CRBN sequence to identify TBD boundaries
crbn_full = "MDWSHPQFEKSAVDENLYFQGGGRMAAEEGGDGRRNMGNPPPPAPAESEEEDDNEMEVEDQDGKEAEKPNMINFDTSLPTSHMYLGSDMEEFHGRTLHDDDSCQVIPVLPHVMVMLIPGQTLPLQLFHPQEVSMVRNLIQKDRTFAVLAYSNVREREAHFGTTAEIYAYREEQEYGIETVKVKAIGRQRFKVLEIRTQSDGIQQAKVQILPERVLPSTMSAVQLQSLSRRHIFPSSKPKVWQDRAFRQWWQKYQKRKFHCASLTSWPPWLYSLYDAETLMERVKRQLHEWDENLKDESLPTNPIDFSYRVAACLPIDDALRIQLLKIGSAIQRLRCELDIMNKCTSLCCKQCQDTEITTKNEIFSLSLCGPMAAYVNPHGYIHETLTVYKACNLNLSGRPSTEHSWFPGYAWTIAQCRICGNHMGWKFTATKKDMSPQKFWGLTRSALLPRIPEAEDELGHDRSPLLCL"

print(f"Full CRBN construct length: {len(crbn_full)}")

# TEV site ends at ENLYFQG (position ~20), actual CRBN starts after GGG
# Find the GGG after ENLYFQ
tev_end = crbn_full.find('ENLYFQGGG') + len('ENLYFQGGG')
crbn_proper = crbn_full[tev_end:]
print(f"CRBN after tag removal (pos {tev_end}): {len(crbn_proper)} residues")
print(f"First 20 of CRBN proper: {crbn_proper[:20]}")

# Human CRBN TBD is approx last 160 residues of the 442-aa protein
# In our construct that maps to ~ last 160 residues of crbn_proper
tbd = crbn_proper[-160:]
print(f"\nTBD (last 160 residues): {len(tbd)} residues")
print(f"TBD sequence: {tbd[:30]}...")

eral_len = len("SIKRSKKNSLALSLTADQMVSALLDAEPPILYSEYDPTRPFSEASMMGLLTNLADRELVHMINWAKRVPGFVDLTLHDQVHLLECAWLEILMIGLVWRSMEHPGKLLFAPNLLLDRNQGKCVEGMVEIFDMLLATSSRFRMMNLQGEEFVCLKSIILLNSGVYTFLSSTLKSLEEKDHIHRVLDKITDTLIHLMAKAGLTLQQQHQRLAQLLLILSHIRHMSNKGMEHLYSMKCKNVVPLSDLLLEMLDAHRLHAPTS")
print(f"\nERalpha length: {eral_len}")
print(f"Reduced total tokens: {eral_len} + {len(tbd)} = {eral_len + len(tbd)}")
