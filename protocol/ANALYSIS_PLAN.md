# Integrated analysis plan

Version 1 — 10 November 2026. This records the scope before any matched molecular associations are examined. It is not a prospective registry entry.

## Three connected components

1. **Published-cohort reconstruction:** retain Nie et al.'s four summary-rule rows, source CSV hashes, figures, executed notebook, and limitations. No novel patient observations are created.
2. **Uncertainty-aware classification:** exact feasibility analysis for coupled bounded log-error scenarios, with a fixed synthetic design grid and a deliberately uncoupled comparator. Implemented and tested.
3. **Molecular association and validation:** preparation functions and a prespecified study framework. Patient matching, externally defined modules, clinical covariates, adequate precision, and independent validation remain data-dependent. No real molecular results are included.

## Primary methodological investigation

**Question:** With equal marginal error ranges, when does an independent fraction/concentration envelope admit classification states excluded by a calculated-concentration model?

For the calculated-concentration model, D=F×T (F as proportion). Perturb log F by eF and log T by eT, so log D changes by eF+eT. The exact bounded solver intersects the fraction-high/low region with the concentration-high/low region. Threshold equality belongs to high. It honors the physical upper bound F≤1.

The comparator permits the same marginal log-fraction interval and log-D interval independently. It is a superset of the coupled feasible set, rather than a probability-matched stochastic alternative. In particular, when eT=0 and both normalized measurements equal one, the coupled model permits only both-low and both-high; the independent envelope also permits both discordant states. This is a mathematical consistency result, not an empirical biological discovery.

**Primary output:** number of extra attainable states in the independent envelope at each design point. Secondary outputs: certified four-state stability and its sensitivity to bound magnitude. The fixed grid uses F/threshold and D/threshold in {0.5,0.8,1,1.2,2}; a=b in {0,0.05,0.1,0.2}. A 1% illustrative fraction threshold makes the fraction ratio numerically equal to fraction percent; concentration is in illustrative threshold units. No grid is weighted as a clinical population.

Uniform simulation is optional and explicitly conditional on an assumed rectangular distribution; it does not estimate an observed patient's true-state probability. Certification requires no distribution. All error ranges are illustrative until supported by assay evidence. No thresholds are transferred across assays.

## Prespecified molecular branch

**Question:** Do prespecified injury/immune module associations reproduce across patient-separated partitions, and how sensitive are descriptions of discordant regions to classification stability?

Required schema: sample_id, patient_id, partition (discovery/validation), fraction_percent, absolute_copies_ml, assay, phenotype. Covariate additions require a locked specification before examining associations. Required expression input is a gene × sample matrix of already normalized gene-level microarray values, with valid externally documented probe mapping. It is not raw RNA-seq counts.

Before running: supply externally defined module lists for endothelial/AMR activity, IFN/cytotoxic activity, and injury/cell cycle with gene-set citations; resolve assay imprecision and sample timing; establish phenotype definitions, cohort overlap, repeat patients, and precision targets. These modules are conceptual categories, not a supplied validated gene signature. `molecular.py` intentionally has no invented clinical gene lists.

Module scoring averages gene z scores using discovery means/SDs only. Missing or invariant genes stop scoring instead of silently changing a module. Patient leakage stops the preparation. The specification hash checks integrity but does not establish when a protocol was registered.

The included minimal association estimator fits log fraction and log absolute jointly, separately within discovery and validation. It reports OLS coefficients and patient-cluster percentile bootstrap intervals with Bonferroni tail allocation over the full reported module × predictor × partition family. It reports no P values, clinical predictions, or causal effects. It requires sufficient bootstrap draws for tail resolution and at least 20 patient clusters per partition as an implementation safeguard, not a proof of adequate power. Percentile coverage remains approximate; effective precision and sample size require assessment before inference.

The minimal estimator is **not the final adjusted biological model**: clinical covariates, nonlinearity, center/time transportability, and prespecified stable-versus-unstable contrasts require a dataset-specific protocol amendment and implementation. Its discovery and validation results are separate estimates; sign agreement alone is not proof of replication. Independent-cohort validation cannot be claimed from within-cohort partitioning.

Use continuous identifiable coordinates. Never include log F, log D and log T unrestricted in the same model if D=F×T. A discordance label is a deterministic summary, not additional measured information. Expression-derived phenotype labels must not be treated as independent validation of the same genes.

## Decision gates

- Matched measurements absent → no molecular association analysis; retain the mathematical methods demonstration.
- No patient crosswalk → no patient-independent validation claim.
- No assay-error calibration → only explicitly hypothetical bounded scenarios.
- Inadequate precision → descriptive analysis or further data acquisition.
- Closest supplementary methods duplicate this design → frame as reproduction/benchmark, revise novelty claims.

The repository is a working integrated research framework. A new validated molecular discovery, publication-level novelty and improved rejection outcomes remain unestablished.
