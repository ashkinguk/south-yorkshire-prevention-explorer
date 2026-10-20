# QA summary — 20 October 2026

**Result:** Core analytical checks and automated DOM interaction checks passed. All three targeting datasets and all 171 boundaries are present. Admissions SAR is available for 170 unchanged MSOAs. One merged MSOA is explicitly unavailable. Actual browser visual, pointer and responsive-layout checks were not possible in this session.

## Data checks completed

| Check | Result |
|---|---|
| Expected geography universe | 171 unique 2021 MSOAs: Barnsley 30; Doncaster 39; Rotherham 32; Sheffield 70 |
| Codes, names and Places | Complete; Commons v2.3 names and original ONS names retained |
| Core source joins | 171/171 names, population, ethnicity, deprivation and geometry; no duplicate MSOAs |
| Population period | Nomis metadata latest 2024; every retrieved population row is 2024 |
| Male ages | 5,985 rows = 171 × 35 single ages; age codes 141–175 verified as ages 40–74; male sex code 1 |
| Population denominator | All ages code 0, sex total code 0; measures=20100 |
| Published LAD benchmarks | Exact agreement for each Place; differences all zero |
| Ethnicity | TS021 / NM_2041_1; all 19 leaf categories retained; 19-category sum equals total in all 171 areas |
| Ethnicity definitions | Minority = total minus category 1; non-White = total minus categories 1–5; no aggregate categories added to leaves |
| IMD | Official national deciles 1–2, with valid deciles 1–10 throughout; supplied File 7 mid-2022 total population |
| LSOA denominator joins | All 860 South Yorkshire 2021 LSOAs map exactly once; match entire IMD LAD subset; no truncated ArcGIS response |
| Numeric validity | All percentages 0–100; positive denominators; male count below total; no fabricated missing observations |
| Boundaries | 171 unique feature codes, exactly equal to the names/data universe |
| Admissions source | Indicator 93227; persons/all ages, MSOA only, no category breakdown; latest returned sortable period selected |
| Admissions definition | CSV metadata verifies indirectly standardised ratio; full metadata retained |
| Admissions correspondence | ONS exact-fit lookup: 170 U (unchanged), two M predecessor records for one merged 2021 area |
| SAR transfer | Only identical-code unchanged areas transferred; all 170 available; no population-weighted SAR averaging |
| Missing SAR | E02007002 is blank with explanation, not zero; does not affect targeting |

### Published population benchmark comparison

| Place | Sum of MSOAs | Nomis LAD total | Difference |
|---|---:|---:|---:|
| Barnsley | 251,770 | 251,770 | 0 |
| Doncaster | 319,765 | 319,765 | 0 |
| Rotherham | 276,595 | 276,595 | 0 |
| Sheffield | 582,493 | 582,493 | 0 |
| South Yorkshire | 1,430,623 | 1,430,623 (sum of LADs) | 0 |

All-area men aged 40–74: **282,531**.

### Default targeting reproduction

Linear-interpolated 80th percentiles across all 171 MSOAs; inclusive >= comparisons on unrounded values:

| Measure | Cutoff |
|---|---:|
| Deprivation percentage | 72.81648675171736% |
| Ethnic minority percentage | 24.505661652864628% |
| Men aged 40–74 count | 1,971 |

Criteria count distribution: 94 meet zero, 52 meet one, 22 meet two and 3 meet three. ANY: **77**. ALL: **3**. Default ANY cohort: **736,488** total residents and **137,889** men aged 40–74. These population groups overlap and are not additive.

## Automated application checks completed

`node tests/core.test.js`: **11 test groups passed**.

- JavaScript flags for every MSOA match independently calculated Python baseline flags.
- Inclusive ties, quantile interpolation, thresholds at 1/10/20/30/50/100%, all eight criterion subsets and both matching rules.
- Place filtering retains the original South Yorkshire thresholds.
- Search by name/code, empty results and no-selected-criteria behaviour.
- CSV quoting, commas, newlines, Unicode and text-formula protection; round-trip parsing.
- Admissions coverage, null versus zero, required columns, numeric values, duplicate/unknown codes and incompatible geography.
- Partial upload warnings and rejection of mixed source periods.

`tests/dom.test.js` with jsdom: **7 test groups passed**.

- Initial load: 77 shortlist rows, interactive map shapes, bubbles and matching KPI.
- Place and ANY/ALL controls synchronise table, map, chart and KPI counts.
- Area selection updates details; adding comparisons updates the comparison table.
- Focus filtering and CSV Blob generation are wired correctly.
- Count view, sorting, navigation and SVG zoom controls respond.
- Temporary upload refreshes SAR/period; warns about missing areas; invalid upload retains prior data; restore works.
- Empty-state messaging and zero uncaught application errors.

JavaScript syntax checks passed. Python preparation assertions passed. Source files, download paths and local links were checked. ZIP integrity was tested after creation.

## Verification limits and remaining browser acceptance checklist

jsdom is not a real browser and does not render or measure layout. No screenshot, browser-preview or responsive-layout pass is claimed. The supported browser-control capability was unavailable, so no unsupported browser route was used.

Before wider distribution, run the local server described in README.md and check:

1. At desktop width, the map and quadrant appear side by side; at narrow/mobile width they stack and filters remain usable.
2. Hover and keyboard-focus map areas/bubbles; confirm the correct neighbourhood and exact values. Pan, zoom and Fit; test real pointer interactions.
3. Search and select a known area; compare its displayed values with the processed CSV.
4. Switch Place, threshold, criterion checkboxes and ANY/ALL; confirm table/map/chart/KPI consistency visually.
5. Download filtered CSV through the browser; confirm saved encoding, headers, rows and current provenance in Excel or a text editor.
6. Upload a valid local admissions CSV, then duplicate-code/invalid-geography files; verify the browser file picker, rejection message and restore control.
7. Verify all four tabs and the four-area comparison on the actual devices used by colleagues.

## Known analytical limitations

- Admissions period 2016/17–2020/21 is old and includes pandemic disruption; it is context, not a targeting flag or undiagnosed hypertension estimate.
- Wickersley South, Bramley South & Whiston (E02007002) merges E02001599/E02001601. Published observed and expected counts are withheld; the SAR cannot be recomputed reliably. Missing value is intentional.
- Core datasets use different reference periods: mid-2024, Census 2021 and IMD 2025 with mid-2022 denominators.
- Data describe residents/areas, not registered GP populations or individual eligibility. Some residents of deprived LSOAs will not personally be deprived.
- Top-percentile selection includes ties and is sensitive to chosen thresholds; no guarantee that exactly the requested fraction qualifies.
- Official geography has been generalised for web display. Do not use the displayed polygons for property-level decisions.
- The browser verifies the schema and geography labels of replacement admissions data but cannot prove the quality of a user's local calculation.
- The downloaded default processed CSV is a baseline snapshot. Use live export after changing thresholds or uploading replacement data.
