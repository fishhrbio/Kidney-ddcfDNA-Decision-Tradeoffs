# Source data, licensing, and transformations

## Primary evidence

Nie W, Wang Y, Fu Q, et al. Integrating Donor Derived Cell-Free DNA Fraction and Absolute Quantification for Enhanced Rejection Diagnosis in Kidney Transplant Recipients. *Diagnostics*. 2025;15(3):237. Published 21 January 2025. DOI: [10.3390/diagnostics15030237](https://doi.org/10.3390/diagnostics15030237). PMID: 39941167. PMCID: PMC11817499.

- [Primary full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC11817499/) — methods, Tables 1–3, rule definitions, and licensing.
- [Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC11817499/table/diagnostics-15-00237-t001/): 15 rejection and 35 comparator recipients.
- [Table 2](https://pmc.ncbi.nlm.nih.gov/articles/PMC11817499/table/diagnostics-15-00237-t002/): six biopsy phenotype summaries, including ABMR/mixed, TCMR, borderline TCMR, BKVN, IgAN/FSGS, and other.
- [Table 3](https://pmc.ncbi.nlm.nih.gov/articles/PMC11817499/table/diagnostics-15-00237-t003/): four diagnostic rules and reported sensitivity, specificity, PPV, NPV.
- Methods 2.2 and 2.4–2.6: biopsy classifications, total-cfDNA qPCR, targeted SNP sequencing, and calculation of absolute dd-cfDNA from total cfDNA and fraction. Figure 2 caption: cutoffs selected by maximum Youden index. Section 3.4: combined rule definitions.

The study recruited at one center from December 2019 to April 2021. Rejection comprises ABMR, mixed rejection, and TCMR; borderline TCMR is in its comparator group. All four rules share this cohort. We retain the study definitions without implying that comparators have no injury.

## Included files

| File | Observation unit | Transformation |
|---|---|---|
| `published_summary/diagnostic_performance.csv` | One diagnostic rule in the same cohort | Table 3 transcribed; Table 1 denominators and source labels added |
| `published_summary/biopsy_phenotype_summaries.csv` | One biopsy phenotype group | Table 2 transcribed; unreported quartiles blank |
| `processed/reconstructed_counts.csv` | One rule in the same cohort | TP/TN uniquely reconstructed from rounded sensitivity/specificity; FN/FP by subtraction; all four rates recalculated |
| `processed/rate_checks.csv` | One rule-metric comparison | Published versus recalculated rates and percentage-point difference |
| `processed/rounding_sensitivity.csv` | One rounding-tolerance choice | Reconstruct all rules at each tolerance and compare with baseline |
| `processed/quality_report.json` | Project-level summary | Dimensions, exclusions, duplicates, missingness, and cohort counts |
| `processed/environment.json` | Execution environment | Actual Python and analysis-package versions |

The two CSV inputs preserve the published-summary transcription. `INPUT_MANIFEST.json` preserves their original byte counts and SHA-256 checksums. The analysis verifies checksums before calculation; no remote download is needed. The notebook embeds these exact bytes for standalone execution. `.gitattributes` prevents input CSV line-ending normalization by Git.

### Rule labels

- Fraction alone and absolute alone retain Table 3 values at cutoffs 1.08% and 32 copies/mL.
- Table 3 “Double-positive” becomes **Both positive (AND)**.
- Table 3 “Double-negative” means both measurements negative to call a negative result, hence **Either positive (OR)** is the positive rule.
- The project reproduces reported aggregate classifications. It does not resolve behavior exactly at a threshold from patient-level records, change positivity conventions, or refit cutoffs.

## Reuse

The article identifies its license as [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). Original article authors retain credit for measurements and source tables. Transcribed and derived tables and source-derived figure content are shared under the same CC BY 4.0 attribution, with changes described above. MIT licensing of original project code does not relicense third-party material.

The paper states that individual data are available only on request with appropriate authorization because of privacy and ethics restrictions. No individual records, identities, unpublished manuscript, or inferred patient distributions are supplied here. This is not a systematic review or meta-analysis. No new literature search beyond source verification is represented as exhaustive.
