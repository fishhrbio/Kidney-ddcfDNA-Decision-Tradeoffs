# Novelty and data audit

Audit date: 10 November 2026. Scope: targeted primary-literature search and direct public-metadata inspection for the proposed project. This is not a systematic review or proof that no overlapping study exists.

## Verdict

The broad proposal “fractional/absolute discordance has biological meaning” overlaps substantially with established work. A narrower question integrating **classification stability under explicit uncertainty with prespecified molecular association and validation** may add value. No exact matching implementation was identified in the targeted searches, but important full-text/supplementary comparisons remain incomplete.

The primary data lead is useful but not turnkey. GSE305222 provides an expression-resource listing and disease subgroup labels; its inspected standard metadata does not provide the paired numeric blood measurements needed to define discordance.

## Closest prior work and implications

| Primary source | Verified overlap | Implication for proposed claims |
|---|---|---|
| [Using both fraction and quantity, 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8722815/) | Dual-threshold classification and high-total-cfDNA cases missed by fraction alone | Combining measurements and denominator-associated false negatives are established |
| [Combining fraction and quantity, 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9698190/) | Trifecta training/test comparisons, molecular/histological references and a two-threshold algorithm | A new OR rule or uncomplicated paired classifier would not establish novelty |
| [Gauthier et al., 2024](https://pubmed.ncbi.nlm.nih.gov/38150492/) | Molecular processes associated with dd-cfDNA across 604 biopsies and disease states | Broad injury/immune-expression associations are already studied |
| [Erratum to that study](https://pmc.ncbi.nlm.nih.gov/articles/PMC12356554/) | Corrects reported leading multigene-score correlations | Any reproduction must use the correction |
| [Nie et al., 2025](https://pubmed.ncbi.nlm.nih.gov/39941167/) | Four rules in the 50-recipient cohort used in the existing project | Current reconstructed counts are a secondary analysis, not new patient observations |
| [Benning et al., 2026](https://pubmed.ncbi.nlm.nih.gov/42269874/) | Combined continuous score, independent-cohort evaluation and decision-curve analysis | A composite score or net-benefit plot alone is insufficient differentiation |
| [Rejection continuum study, 2026](https://pubmed.ncbi.nlm.nih.gov/41815531/) | Relative, absolute and combined measures associated with molecular/histological activity | Connecting combined measures with activity indices is also established |
| [Treatment follow-up study, 2026](https://pubmed.ncbi.nlm.nih.gov/41968872/) | Fractional/absolute trajectories and total-cfDNA changes after treatment | Treatment-associated denominator effects are not a new mechanism |
| [Time-dependent fraction increase, 2020](https://doi.org/10.1093/clinchem/hvaa175) | Apparent fraction increase associated with changing host cfDNA in stable recipients | Denominator drift is a longstanding concern |
| [ddPCR feasibility study, 2021](https://doi.org/10.3389/fmed.2021.748668) | Low-copy stochastic effects and analytical limitations | Measurement uncertainty is established; a new application must add a specific validated result |

Evidence depth varies: the 2022 full-text retrieval and source extracts, 2024 source extracts/erratum, GEO files, and 2026 combined-model PubMed abstract were inspected. Some article pages encountered browser challenges. The 2026 continuum and treatment records were checked via indexed primary abstracts; complete supplementary-method comparison is outstanding. Published journal records take precedence over preprint counts/versions.

## Direct dataset audit

Primary record: [GSE305222](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE305222). Downloaded the series record, one sample record ([GSM9165408](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9165408)), and the complete metadata header of the [series-matrix file](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE305nnn/GSE305222/matrix/GSE305222_series_matrix.txt.gz). Expression values were not downloaded or analyzed for this audit.

The header contains **604 sample accessions** and three sample-characteristic rows:

| Field | Directly observed contents |
|---|---|
| disease subgroup | ABMR 140; Normal 312; pTCMR 9; cAKI 50; Mixed 34; TCMR 28; pABMR 31 |
| in 300? (yes, no) | yes 297; no 306; blank 1 |
| in 280? (yes, no) | yes 277; no 326; blank 1 |

These are repository labels and counts, not independently re-adjudicated diagnoses. Prefix meanings and cohort flags must be resolved from the source materials; the flags' names do not equal their observed yes-counts. They cannot be assumed to define independent discovery and validation cohorts.

No paired numeric dd-cfDNA fraction/concentration, patient ID, time-after-transplant, or other clinical covariate fields were found in this header's sample characteristics. Their absence from this inspected file does not prove they are unavailable elsewhere. The record lists a raw CEL archive and a processed log2-RMA expression file. The platform ID is GPL13667; the protocol text also names a PrimeView array, creating an annotation detail that must be reconciled before processing.

Metadata-header SHA-256: `7b5dc1f19def46703b42c7c48022cbdea5bf2ee267ac83c6c8daa0cdec4e33ba`. A machine-readable [metadata audit](metadata-audit.json) accompanies this document. The complete downloaded metadata are retained in the local working area rather than included as public-project content.

## Search record and remaining work

Targeted web searches retrieved primary PubMed/PMC, publisher, and GEO records. Query families included:

- `GSE305222 fraction absolute`; `GSE305222 characteristics`; `GSE305222 supplementary metadata`.
- `kidney dd-cfDNA discordant fraction quantity molecular expression discordance Trifecta`.
- `dd-cfDNA fraction quantity discordant transcriptomic signatures threshold instability uncertainty`.
- `dd-cfDNA discordance stability kidney`; `dd-cfDNA discordant gene expression`; `dd-cfDNA threshold perturbation`.
- `donor-derived measurement error absolute fraction kidney`.

Results were screened for kidney-specific paired-measurement, transcriptomic, uncertainty, and validation overlap. Heart-transplant discordance between blood gene-expression panels and dd-cfDNA was not treated as direct evidence about kidney fractional/absolute discordance. Search-engine ranking and incomplete full-text access limit negative conclusions. No exhaustive database export, independent dual screening, or registered systematic search was performed.

Before making a strong novelty claim, inspect the nearest studies' supplementary methods, confirm dataset/cohort overlap, check conference/preprint updates, and determine whether uncertainty-aware discordance/module analyses were already performed under different terminology. The publisher supplement link [TP/C935](https://links.lww.com/TP/C935) could not be resolved by the web tool during this audit; its contents remain unchecked.

## Claims that are and are not supported

Supported now: a coherent computational study can be specified; the current software foundation is reusable; major overlapping prior work exists; the standard GEO metadata lack several required fields.

Not established now: an unprecedented hypothesis, sufficient accessible matched data, independent external validation, statistically detectable molecular differences, a clinically useful classifier, or publishability. This audit preceded the synthetic methods extension; no real molecular analyses, investigator messages, or GitHub publications were performed.
