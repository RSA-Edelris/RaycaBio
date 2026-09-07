
# Close Phase 5 with the final report document
doc = {
    "title": "Molecular Docking and Binding Energy Analysis — 4CI2 / CRBN",
    "summary": (
        "Five structures (3 parent compounds, 2 racemic → enantiomers split) docked into "
        "the CRBN IMiD tri-tryptophan pocket (PDB 4CI2) using gnina GPU. "
        "Best compound: EDS01806218 (1S,2S), Vina −9.08 kcal/mol, CNN pKi 7.43, "
        "ΔG_CNN −10.13 kcal/mol. "
        "EDS01806218 shows 2.3 kcal/mol stereoselectivity advantage for the (1S,2S) isomer. "
        "Five protein-ligand complex PDB files produced. "
        "Full MM-GBSA blocked by missing openff-toolkit; CNN-derived ΔG reported instead."
    ),
    "results": {
        "EDS01357518_ent1": {"vina_kcal_mol": -7.52, "cnn_pose": 0.5577, "pKi": 7.029, "dG_CNN_kcal_mol": -9.58},
        "EDS01357518_ent2": {"vina_kcal_mol": -8.09, "cnn_pose": 0.7692, "pKi": 6.979, "dG_CNN_kcal_mol": -9.52},
        "EDS01806218_ent1": {"vina_kcal_mol": -6.81, "cnn_pose": 0.3036, "pKi": 6.328, "dG_CNN_kcal_mol": -8.63},
        "EDS01806218_ent2": {"vina_kcal_mol": -9.08, "cnn_pose": 0.7395, "pKi": 7.431, "dG_CNN_kcal_mol": -10.13},
        "EDS01889984":      {"vina_kcal_mol": -6.63, "cnn_pose": 0.4955, "pKi": 6.990, "dG_CNN_kcal_mol": -9.53},
    },
    "files": {
        "report": "phase_04_docking_and_binding_energies_final_report.md",
        "complex_pdbs": [f"complex_{lig}.pdb" for lig in
                         ["EDS01357518_ent1","EDS01357518_ent2",
                          "EDS01806218_ent1","EDS01806218_ent2","EDS01889984"]],
        "pose_sdfs": [f"poses_{lig}.sdf" for lig in
                      ["EDS01357518_ent1","EDS01357518_ent2",
                       "EDS01806218_ent1","EDS01806218_ent2","EDS01889984"]],
    }
}
finish(doc)
