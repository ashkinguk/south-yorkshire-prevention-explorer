# Change log

## 2.1.0 — focused terminology and quadrant refinement

- Replaced interface geography references with MSOA/area terminology while retaining Commons Library friendly names and ONS codes.
- Explained the default as the highest South Yorkshire quintile (Q5, highest values), with separate rankings, approximate 20% coverage and ties. Custom advanced percentages use accurate percentage wording instead.
- Set the population-weighted average IMD score as the default on both charts and on reset. Preserved the concentration-percentage alternative.
- Clarified four quadrant labels and added accessible information tooltips showing the meaning and values of the ethnicity targeting cutoff and descriptive IMD benchmark.
- Updated Data & Methods to distinguish national LSOA deprivation quintiles from South Yorkshire MSOA targeting quintiles.
- Verified every data file, processing script, core calculation file and CSS file remains byte-for-byte unchanged. Existing and focused interaction checks pass.


## 2.0.0 — 20 October 2026

- Applied the supplied mock-up's visual direction: desktop sidebar, navy/blue/teal palette, spacious cards, icons, larger KPI figures, restrained borders and shadows. No official NHS logo or endorsement claim added.
- Moved the analyst percentile control into collapsed Advanced targeting settings in Data & Methods; retained the top-20% defaults and exact original classifications. Replaced visible ANY/ALL wording with plain-English options.
- Reworked the four KPI definitions, including the selected-geography denominator, original-three overlap and emergency admissions above England=100 with availability coverage.
- Added a smaller three-population breakdown with periods and an overlap explanation.
- Added a continuous admissions map layer anchored at 100, hatched missing data, and a distinct highlight/restrict health filter. Admissions remains outside population targeting.
- Added reproducible population-weighted average IMD 2025 scores from the existing 860 official LSOA scores and supplied mid-2022 populations. No changes to the primary deprivation concentration measure.
- Added shared quadrant X-axis controls, four explanatory quadrant labels, restrained overlap shading, correct reference lines by axis, a proportional bubble-size legend, and admissions in tooltips. Score-mode reference is the fixed full-SY weighted mean, explicitly descriptive.
- Improved shortlist columns, sorting, original-three/selected-criteria labelling and admissions coverage. Preserved selection, comparisons, CSV exports and session uploads; enriched exports with supplementary measure and filter provenance.
- Added the supplementary score to Area Explorer with a correctly weighted South Yorkshire comparison. No SAR average is calculated.
- Preserved all six original source data files byte-for-byte, all 171 MSOAs, all original geography mappings and raw data.
- Extended automated tests for weighted scores, KPI totals, axis switching, health controls, map colours, missing data, exports and replacements. Actual browser visual QA remains unavailable.
