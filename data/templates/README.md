# Matched-input specification

`matched_metadata.csv` is an empty schema, not patient data. Use documented deidentified IDs and compatible blood/biopsy timing. Both partitions are required; patients must not cross partitions. Expression data must be normalized gene × sample values with an exact sample-ID match. Resolve probe mapping and module sources before analysis.

Required molecular specification keys: question, modules (module name to externally prespecified gene list), gene_set_sources, threshold_source, covariates, primary_contrasts, validation_plan, multiplicity_plan. A SHA-256 hash verifies file integrity; it does not establish preregistration. No placeholder gene list is presented as a validated module.

The minimal estimator is incompletely adjusted and is not a substitute for the full data-specific analysis plan.
