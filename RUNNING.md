# Run and inspect the project

Python 3.12 and the pinned packages in `requirements.txt` reproduce the analyses. From the repository root:

```text
python -m pip install -r requirements.txt
python run_analysis.py
python stability.py
python -m unittest discover -v
```

The first analysis regenerates the original published-summary results. The second produces `results/synthetic_stability_grid.csv`, `results/stability_summary.json`, and the stability figure. The generator also refreshes the browser figure and summary. The original `analysis.ipynb` remains an executed standalone notebook for the published-cohort reconstruction; notebook execution dependencies are in `requirements-notebook.txt`.

Open `docs/index.html` for the cohort guide or `docs/stability.html` for the new scenario explorer. Both work locally without a server; no accounts, uploads or answer storage are required.

`stability.audit_samples` accepts a dataframe with complete sample IDs, fraction percentages and absolute copies/mL plus explicit assay thresholds and log-error bounds. It computes exact feasible states; it does not estimate rejection probabilities. The CLI supports the same audit with explicit thresholds and an output path. To avoid accidental use of demo defaults, the CLI rejects the illustrative default pair 1/1 for file input; the Python API can accept those thresholds if scientifically appropriate.

`molecular.validate_metadata`, `module_scores`, `freeze_specification`, and `association_estimates` provide the preparation and minimal continuous-association API described in [the plan](protocol/ANALYSIS_PLAN.md). They require real matched inputs and externally specified modules. No real-data molecular run is bundled. Complete the data gates and adjusted-model specification before applying them to a research claim.

## Output provenance

| Output | Evidence type |
|---|---|
| `data/processed/*`, figures 01–02, original notebook | Reconstruction of published clinical summaries |
| `results/*`, figure 03, browser stability explorer | Mathematical/synthetic scenarios |
| `protocol/*` | Proposed biological study and documented availability limits |

Do not infer assay precision, cohort instability rates or molecular effects from the synthetic grid. The original four diagnostic rows cannot identify patient-level distance to a cutoff. Source CSVs are byte-preserved and checked against `INPUT_MANIFEST.json`.
