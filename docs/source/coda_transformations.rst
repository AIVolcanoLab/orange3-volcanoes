CoDA Transformations
=====================

Overview
--------
This widget applies three basic log-ratio transformations to compositional data:
1. **CLR (Centered Log Ratio):** Aitchison (1986).
2. **ALR (Additive Log Ratio):** Aitchison (1986).
3. **ILR (Isometric Log Ratio):** Egozcue et al. (2003).

**Purpose:** Log-ratio transformations enable univariate and multivariate statistical analyses of compositional data (e.g., Hierarchical Clustering).

Input
-----
- **Raw dataset:** Unprocessed dataset.

Errors
------
- Applying the ILR transformation fails if the dataset contains zeros.

Comments
--------
- Add a specific user message emphasizing that the dataset should not contain zeros for log-ratio transformations.
