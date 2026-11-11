# Proposed research framework: stability and molecular interpretation of kidney dd-cfDNA discordance

Prepared 10 November 2026. Status: biological-study framework with an implemented hypothetical stability extension. Real molecular analyses await data; publication awaits review.

## Executive assessment

The existing project is a sound reproducible worked example of published diagnostic tradeoffs. A defensible research extension would investigate **whether fractional/absolute discordance is stable enough to interpret biologically, and which molecular associations remain reproducible when threshold and measurement uncertainty are considered**.

This is a candidate methodological and biological contribution. A targeted literature audit did not identify an exact match for this integrated design, but does not establish first-in-field novelty. Closely related molecular, combined-measurement, and denominator-confounding studies already exist. The project should not claim a new biomarker, a newly discovered denominator effect, or a superior rejection test on the basis of the current foundation.

The principal feasibility constraint is data, rather than coding. Direct inspection of GSE305222's series-matrix metadata found 604 samples and disease labels, but no matched numeric fractional/absolute dd-cfDNA fields or patient identifiers. Its expression files alone cannot answer the proposed question. Article supplements, sample crosswalks, or authorized investigator-provided data must resolve that gap before the molecular study can proceed. See the [audit](NOVELTY_AUDIT.md).

## 1. Working title and scientific question

**Working title:** “Threshold stability and molecular interpretation of fractional–absolute dd-cfDNA discordance in kidney transplantation.”

**Primary question:** How frequently does fractional/absolute classification change under explicitly defined threshold and analytical-uncertainty scenarios?

**Conditional biological question:** Among samples with robustly discordant measurements, are prespecified biopsy-expression patterns reproducible across validation partitions or independent cohorts, after accounting for available clinical context?

“Robust” here means stable under the stated scenarios. It does not mean the result is clinically correct. Without an empirically supported assay-error model, perturbations are sensitivity scenarios, not calibrated probabilities about a patient's true state.

## 2. Corrected conceptual foundation

Let F be donor fraction expressed as a proportion, D donor-derived concentration, and T total cfDNA concentration in compatible units. For assays that calculate absolute concentration, D = F × T. Equivalently, log D = log F + log T for positive values.

Consequences for the design:

- The discordance category is a deterministic function of F, D, and thresholds. It cannot contain information unavailable in the pair F and D. Any improvement after adding it to a restricted model reflects representation/model specification, not new measured biology.
- Do not simultaneously interpret unrestricted coefficients for log F, log D, and log T when the identity holds: they are linearly dependent. Select an identifiable parameterization, such as log F and log T, or log D and log T.
- Threshold geometry alone creates some apparent separation. A high-D/low-F region necessarily implies sufficiently high T when the identity holds. Observing that relationship does not prove a mechanism or establish novelty.
- Independently measured D and F may have different error structures. Determine the assay's actual measurement chain before choosing equations, covariance assumptions, or perturbations.
- Estimated total cfDNA from D/F is derived, not an independent validation measurement; division of group medians cannot recover patient-level T.

## 3. Specific aims and endpoints

### Aim 1: Reconstruct an auditable paired-sample dataset

Create a documented mapping among sample IDs, biopsy-expression profiles, blood measurements, assay information, and clinical/reference labels. Preserve all source labels, units, missingness, exclusions, and repeated-patient relationships.

Deliverables: data dictionary, cohort-flow table, sample-match report, assay provenance table, overlap map, and a record of variables unavailable for adjustment. This is infrastructure, not the novelty claim.

### Aim 2: Quantify classification stability

At assay-appropriate prespecified thresholds, classify samples into both-low, fraction-only-high, absolute-only-high, and both-high groups. Report their sizes and outcome composition. Keep the two discordant directions separate.

**Primary endpoint:** the proportion of samples whose four-state classification changes under each prespecified perturbation scenario, with patient-aware uncertainty intervals where patient IDs are available. Also report stability separately in the two discordant groups and rejection phenotypes.

Distinguish three sources of variation:

1. Analytical imprecision: use assay-specific repeatability/validation evidence or technical replicates if available.
2. Threshold choice: evaluate a prespecified, assay-compatible range, separately from analytical noise.
3. Biological denominator variation: model as a hypothetical biological scenario, not as measurement error or observed longitudinal change unless longitudinal data exist.

Use the coupled measurement equations when appropriate, propagate correlated error, and label unsupported error magnitudes as illustrative assumptions. Never reuse Nie et al.'s performance estimates after changing its cutoffs. Never treat thresholds from different assays as interchangeable.

### Aim 3: Test limited, prespecified molecular associations

Conditional on sufficient matched data, evaluate a small set of externally defined modules: endothelial/AMR-associated activity, cytotoxic/IFN-associated activity, and injury/cell-cycle activity. Freeze gene lists, probe mapping, score calculation, contrasts, and multiplicity handling before examining associations with discordance.

Primary biological analysis: model each module score against continuous identifiable cfDNA coordinates and available clinical covariates. Describe discordant groups as interpretable regions of that surface. A secondary comparison can ask whether stable and unstable discordant groups show different patterns; do not equate this with independent biological information.

Report effect sizes, confidence intervals, and multiplicity-adjusted results across the prespecified module/contrast family. Account for nonlinear relationships where sample size permits. Include time after transplant, assay/center, treatment timing, biopsy indication, renal function, and disease phenotype only when valid metadata and sufficient information support adjustment. Report analyses without unavailable covariates as incompletely adjusted.

Genome-wide discovery is optional and explicitly exploratory, with gene-level false-discovery control and separate validation. Do not use molecular labels derived from the same expression features as independent proof that a gene-expression association predicts rejection.

## 4. Data requirements and decision gates

| Required element | Why it matters | Current status |
|---|---|---|
| Matched F and D with units, sample timing and assay method | Defines discordance and measurement chain | Not present in inspected GSE305222 metadata |
| Expression matrix and probe annotation | Supports module analysis | GEO lists processed expression and raw CEL resources; matrix contents not fully audited |
| Reliable sample crosswalk | Prevents incorrect pairing | Needs verification |
| Deidentified patient ID/repeat-sample map | Prevents patient leakage and false precision | Not present in inspected metadata |
| Reference-label definitions and provenance | Distinguishes molecular labels from histology | Disease subgroup labels present; operational meanings require confirmation |
| Analytical precision or replicate data | Calibrates error propagation | Not yet established |
| Clinical covariates and treatment/biopsy timing | Supports biological interpretation | Not present in inspected characteristics |
| Independent validation cohort or defensible internal partitions | Tests reproducibility | Not established |

**Gate A — access:** inspect remaining supplements/crosswalks and reuse conditions. If matched blood values cannot be obtained, stop the molecular branch. Author contact requires a separately authorized message; no message has been sent.

**Gate B — design:** audit overlap and repeat samples, then conduct a precision/power assessment using group sizes and a stated smallest effect of interest. Freeze the endpoint hierarchy and covariates. There is no universal sample-count cutoff that establishes adequacy.

**Gate C — validation:** lock transformations, modules, thresholds, and model choices before evaluation. If only internal validation is possible, label results internally validated or exploratory; do not describe a held-out subset of the same cohort as external validation.

**Gate D — novelty:** review full texts and supplements of closest studies before asserting novelty. If they already implement the integrated question, revise the claim to a benchmark/replication or seek approval for a materially different question.

## 5. Statistical and computational safeguards

- Prefer interpretable models over a high-dimensional classifier trained on a small dataset. The current four-row summary dataset cannot train or validate a patient-level model.
- Split by patient. Where metadata permit, assess center/time-based transportability. Cohort flags named “in 300” and “in 280” are not automatically independent validation cohorts.
- Fit any learned normalization, feature selection, imputation, hyperparameters, and calibration within training folds. Document that released RMA values may already have been jointly preprocessed; assess that limitation before predictive claims.
- Use expression methods appropriate to normalized microarray intensities, not RNA-seq count models. Resolve the record's GPL13667/protocol-description discrepancy against platform annotation and CEL headers before preprocessing.
- Preserve missing labels. Do not collapse pABMR, pTCMR, Mixed, or cAKI into a binary rejection label without documented definitions and a prespecified rationale.
- Use patient-clustered resampling/uncertainty estimation when repeated observations exist. If patient membership is unavailable, obtain it or limit claims; do not assume 604 independent people.
- Do not optimize thresholds on the evaluation set or select gene modules because they produce a preferred contrast. Maintain an explicit separation between confirmation and exploration.
- Keep diagnostic classification, biopsy-confirmed rejection, treatment response, and graft survival as distinct endpoints. No improvement in graft outcomes can be claimed from this cross-sectional analysis.

## 6. Feasible fallback if matched data remain unavailable

A narrower **measurement-coupled simulation study** can explore how donor DNA, recipient DNA, and correlated analytical error influence rule stability. It would include an identifiable generative model, documented literature-based ranges, limiting-case tests, and comparisons against simple analytical expectations.

Success would mean a reproducible methodological result about assumptions and failure regions, not a clinically validated rule. Simulations alone cannot establish molecular injury signatures or actual changes in rejection detection. A dashboard or simulation visualization alone would remain a tool rather than a novel biological finding.

An across-study aggregate analysis is another possible extension, but requires a separate eligibility/overlap audit and adequate comparable paired-rule summaries. The four existing rows cannot be treated as four independent studies. Neither fallback is an automatic substitution for the molecular plan; a changed scope returns for review.

## 7. Proposed implementation outline after approval

1. **Resolve data access and freeze the protocol.** Audit supplements, create an availability map, verify assay definitions, assess precision, and finish the closest-study comparison. Output: go/no-go report before substantial model development.
2. **Build reproducible ingestion and QC.** Version the schema and transformations; preserve checksums; test sample matching, units, missingness, repeat-patient grouping, and coupling identities.
3. **Implement the stability analysis.** Separate threshold sensitivity, analytical error, and biological scenarios. Test zero-noise and other known limiting cases. Quantify Monte Carlo error where simulation is used.
4. **Run prespecified module analyses.** Only if Gate A passes; validate preprocessing and probe annotations and retain the planned multiplicity family.
5. **Validate and interpret.** Execute patient-aware internal validation and external replication if available. Report null results and uncertainty without changing the question to chase significance.
6. **Prepare a reviewable research release.** Produce analysis notebooks, figures, results tables, scientific README, limitations, references, dependency specification, and tests. Publish only authorized, redistributable data; otherwise provide retrieval instructions and derived artifacts as permitted.

Suggested eventual repository structure: `protocol/`, `src/`, `tests/`, `notebooks/`, `data/README.md`, `results/`, `figures/`, and `docs/`. No new repository, implementation pipeline, or research result is created by this proposal.

## 8. Expected figures and manuscript outline

Planned figures: study/sample flow; F–D plane with thresholds and uncertainty; classification-stability curves by perturbation scenario; prespecified molecular effect estimates; validation comparison. A diagram should distinguish measured quantities from calculated quantities.

Manuscript outline: clinical/measurement problem; closest prior work and precise contribution; cohort and assay provenance; stability methods; module/validation methods; results in the prespecified order; interpretation and alternative explanations; limitations and reproducibility. A null association or unstable discordance result can still be informative if the design is adequate and claims are proportionate.

The companion narrative review can introduce the measurement problem and link to this work. The research study must distinguish its new analyses from the review and from the original investigators' measurements. Journal suitability and publication novelty remain matters for later assessment, not promised outcomes.

## 9. Current implementation status

The integrated release implements the hypothetical stability analysis, synthetic design-grid experiment, browser explorer, and molecular preparation/minimal association APIs. See ANALYSIS_PLAN.md for the exact implemented scope. Matched molecular data, adjusted biological models and external validation remain outstanding. The biological branch must satisfy its data gates before research claims can be evaluated. No repository publication is claimed.
