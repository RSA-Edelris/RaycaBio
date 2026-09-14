
inputs2 = {
    "name": "ARV471_ERalpha_CRBN_ternary",
    "sequences": [
        {
            "protein": {
                "id": "A",
                "sequence": "SIKRSKKNSLALSLTADQMVSALLDAEPPILYSEYDPTRPFSEASMMGLLTNLADRELVHMINWAKRVPGFVDLTLHDQVHLLECAWLEILMIGLVWRSMEHPGKLLFAPNLLLDRNQGKCVEGMVEIFDMLLATSSRFRMMNLQGEEFVCLKSIILLNSGVYTFLSSTLKSLEEKDHIHRVLDKITDTLIHLMAKAGLTLQQQHQRLAQLLLILSHIRHMSNKGMEHLYSMKCKNVVPLSDLLLEMLDAHRLHAPTS"
            }
        },
        {
            "protein": {
                "id": "B",
                "sequence": "MDWSHPQFEKSAVDENLYFQGGGRMAAEEGGDGRRNMGNPPPPAPAESEEEDDNEMEVEDQDGKEAEKPNMINFDTSLPTSHMYLGSDMEEFHGRTLHDDDSCQVIPVLPHVMVMLIPGQTLPLQLFHPQEVSMVRNLIQKDRTFAVLAYSNVREREAHFGTTAEIYAYREEQEYGIETVKVKAIGRQRFKVLEIRTQSDGIQQAKVQILPERVLPSTMSAVQLQSLSRRHIFPSSKPKVWQDRAFRQWWQKYQKRKFHCASLTSWPPWLYSLYDAETLMERVKRQLHEWDENLKDESLPTNPIDFSYRVAACLPIDDALRIQLLKIGSAIQRLRCELDIMNKCTSLCCKQCQDTEITTKNEIFSLSLCGPMAAYVNPHGYIHETLTVYKACNLNLSGRPSTEHSWFPGYAWTIAQCRICGNHMGWKFTATKKDMSPQKFWGLTRSALLPRIPEAEDELGHDRSPLLCL"
            }
        },
        {
            "ligand": {
                "id": "C",
                "smiles": canonical   # RDKit-canonical ARV-471
            }
        }
    ],
    "modelSeeds": [42],
    "seed": 42,
    "diffusion_samples": 3,
    "output_format": "pdb",
    "use_msa_server": False,
    "dialect": "alphafold3",
    "version": 1
}

print("Retrying protacfold with canonical SMILES...")
result2 = run_aidd_tool('protacfold', inputs2, gpu=True)
print("rc:", result2.get('rc'))
print("summary:", result2.get('summary'))
