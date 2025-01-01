Filtering
=========

Overview
--------
This widget allows the user to filter the input data based on three main criteria:
1. **Total oxide weight content (Oxides-Totals):** Filter based on the total weight percentage of oxides.
2. **Cations per formula unit (Cations-Filter):** Filter based on the number of cations per unit formula for clinopyroxenes.
3. **Equilibrium between clinopyroxene and liquid (Equilibrium-Test):** Filter based on existing equilibrium models.

**Details:**
- **Oxides-Totals:** Specify a range around the ideal sum (100 wt%). For example, if the user selects a delta of ±2 wt%, the filter accepts data with oxide totals between 98 and 102%.
- **Cations-Filter:** Specify an absolute delta around the ideal number of cations per formula unit (e.g., 4 ± 0.04 cfu).
- **Equilibrium-Test:** Choose from different equilibrium models (e.g., Kd filter by Putirka 2008, EnFs filter by Mollo 2013). Input data must include chemical compositions, pressure, and temperature.

Input
-----
- **Oxides-Totals:** Cpx and/or Liq compositions.
- **Cations-Filter:** Cpx composition.
- **Equilibrium-Test:** Cpx composition, Liq composition, temperature (T), and pressure (P).

Errors
------
- The filter often fails because the preprocessing step does not generate (or removes) the `Totals` column required by the Oxides-Totals filter.

Comments
--------
- Either enforce the inclusion of a `Totals` column in the input dataset or calculate it as the sum of the oxide weights (wt%).
