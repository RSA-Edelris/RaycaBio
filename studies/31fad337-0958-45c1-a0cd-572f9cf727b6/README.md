# CDK2-CyclinE1 PPI Inhibitor Campaign

**Study ID:** 31fad337-0958-45c1-a0cd-572f9cf727b6  
**Target:** CDK2-CyclinE1 protein-protein interface  
**Date:** 2026-09-06  
**Platform:** Rayca (model: claude-sonnet-4-6)

## Summary

Virtual screening and SAR analysis of 84 compounds against the CDK2-CyclinE1 PPI interface,
followed by rational design, docking, and MM-GBSA scoring of 10 new candidates (NC-001 to NC-010).

## Key Results

| Metric | Value |
|:---|:---:|
| Compounds screened (docking) | 84 |
| Compounds with MM-GBSA | 84 |
| Designed follow-up compounds | 10 (NC-001 to NC-010) |
| Best campaign compound (docking) | CTX-1020732, CNN pKi = 8.931 |
| Best campaign compound (MM-GBSA) | CTX-1020732, dG = −83.2 kcal/mol |
| Best new compound (MM-GBSA) | **NC-010, dG = −84.6 kcal/mol** (benzothiophene core) |
| Best new compound (docking) | NC-010, CNN pKi = 8.792 |

NC-010 (benzothiophene core, O→S substitution) is the highest-scoring compound in the combined 94-compound set by MM-GBSA.

## Runs

| Run | Description |
|:---|:---|
| [max-f1eec88475](runs/max-f1eec88475/) | Full campaign: receptor prep, 84-compound docking + MM-GBSA, SAR analysis, 10 NC compound design, NC docking + MM-GBSA, combined complex PDB |
