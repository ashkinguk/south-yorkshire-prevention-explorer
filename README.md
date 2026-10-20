# South Yorkshire Prevention Grants Explorer — revised dashboard

A static, dependency-free web application with real official data for 171 2021 MSOAs across Barnsley, Doncaster, Rotherham and Sheffield. Prepared 20 October 2026. This revision has not been deployed or uploaded to an external repository. The existing published site remains unchanged.

## Start locally

1. Extract the ZIP to a folder.
2. Install Python 3.10+ if needed.
3. Open a terminal in the extracted `south-yorkshire-explorer` folder and run:

```sh
python -m http.server 8000 --bind 127.0.0.1
```

4. Open **http://localhost:8000** in Edge, Chrome, Firefox or Safari. On Windows, `start-windows.bat` runs the same server using `py`.
5. Keep the terminal open while using the app; press Ctrl+C to stop.

Do not simply double-click index.html: browsers normally block CSV fetches from file:// URLs. No internet connection is needed to use the delivered app after extraction; scripts and styles are local. Links to original sources require internet access.

## What is included

- Four tabs: Overview, Area Explorer, Quadrant, and Data & Methods.
- Synchronised Place, criterion, percentile, ANY/ALL and search controls; count/percentage table views.
- Choropleth of actual ONS MSOA polygons; bubble quadrant, thresholds, tooltips, click/keyboard selection and pan/zoom. Up to four areas can be compared.
- Sortable shortlist; export current rows with flags, cutoffs, filter provenance and admissions source/period.
- Browser-local replacement admissions CSV with full-file validation, missing-area warning, rejection rollback and restore. Uploaded bytes never leave the browser.
- Complete official-source raw responses, processed CSVs, dictionary, methodology, reproducible Python scripts and tests.

The delivered data pass core QA and automated DOM interaction checks. Actual browser rendering and responsive layout were **not tested** because this session had no supported preview capability. Please perform the short browser acceptance checklist in QA.md before distributing to colleagues.

## Files

| Path | Purpose |
|---|---|
| index.html / styles.css / app.js | Static user interface; refinements.js extends existing views |
| core.js | Shared CSV parsing, thresholds, filters, validation and export logic |
| methods.html | Source definitions and analytical method shown in the application |
| data/msoa_names.csv | Master 171-area list with friendly and ONS names |
| data/msoa_population.csv | Mid-2024 population and men aged 40–74 |
| data/msoa_ethnicity.csv | Census 2021 ethnicity totals and 19 constituent categories |
| data/msoa_deprivation.csv | IMD 2025 deprived population and percentage, mid-2022 denominator |
| data/msoa_admissions.csv | SAR, reference period, source and geography audit fields |
| data/msoa_imd_scores.csv | Supplementary population-weighted average IMD 2025 score |
| data/msoa_boundaries.geojson | ONS 2021 web-optimised boundary geometry |
| data/msoa_processed_default.csv | Delivered snapshot joined at default top-20%, all-three-selected settings |
| data/lsoa_deprivation_audit.csv | All 860 LSOAs, deciles, denominators and MSOA mappings |
| data/msoa_geography_correspondence.csv | ONS exact-fit 2011→2021 MSOA correspondence |
| data/admissions_definition.json | Published OHID definition, methodology and caveats |
| data/dictionary.csv | Data dictionary, also displayed in the app |
| data/qa.json | Machine-readable core QA results |
| raw/ | Retrieved source responses; retained for reproducibility |
| scripts/sources.json | Exact download URLs and API parameters |
| scripts/acquire.py / scripts/prepare.py | Retrieve sources / rebuild processed files and assert data quality |
| tests/ | Logic and optional DOM tests |

## Replace admissions data permanently

Make a backup of `data/msoa_admissions.csv`, then replace that file. No JavaScript changes or build step are needed. Reload the browser (hard refresh if needed).

Required header:

```csv
MSOA21CD,admissions_sar,period,source,geography
```

Use official **2021** MSOA codes, at most one row per code, one nonempty period and source across the file, and `MSOA2021` in every geography field. SAR must be blank or a finite non-negative number; blank means unavailable and zero means an observed zero ratio. Missing areas are permitted for a session upload and explicitly warned about. For a permanent file, ideally include all 171 master codes, leaving unavailable SAR values blank. Optional confidence limits and provenance columns are retained but not required by the upload feature.

Before saving a permanent replacement, test it using the Data & Methods upload control: this performs identical schema/value/code validation and reports missing codes. A successful session upload is temporary and does not write to disk. A local replacement must already be harmonised to 2021 MSOAs and represent the same all-cause, all-age, persons SAR measure with England=100. Schema checks cannot validate its clinical definition or the quality of your harmonisation. Do not insert patient-level records.

Replacing admissions changes Area Explorer, selection panels, comparisons and live exports. It never changes targeting flags. The supplied `msoa_processed_default.csv` is a **baseline audit snapshot**, not a live merged file; use the app's export for results incorporating replacement admissions. `prepare.py` rebuilds the original admissions snapshot from raw OHID data, overwriting permanent replacements: back those up first.

## Refresh official source data

Python scripts use only the standard library; no pip packages are needed.

```sh
python scripts/acquire.py
python scripts/prepare.py
python scripts/dictionary.py
node tests/core.test.js
```

The first command reuses cached raw files. To redownload the pinned snapshot URLs:

```sh
python scripts/acquire.py --refresh
```

To request the latest population year for the MSOAs and the matching LAD benchmark:

```sh
python scripts/acquire.py --latest-population
python scripts/prepare.py
```

Read `acquisition_log.json`: failures retain old cache files, exit nonzero and must not be treated as a complete refresh. A changed source schema or partial geography causes preparation to fail rather than fabricate data. The pipeline checks the same 171 MSOAs (2021 boundaries). Names use the Commons latest URL; IMD is pinned to the specified 2025 File 7 release. The admissions endpoint returns all published periods; preparation chooses the latest MSOA period and applies the official unchanged-boundary correspondence. Changed/merged geographies remain unavailable without defensible observed/expected counts.

On a new release, review the source metadata, periods, geographic coverage, QA and benchmark comparisons. Update narrative dates in methods.html, README.md, dictionary and footer to match. Tests comparing 77 ANY / 3 ALL and the delivered admissions coverage are **snapshot regression tests**; review and update these expected values only after validating a new release. Browser KPI/area population labels read the period from the population CSV. Run `scripts/prepare.py` after acquisition, not after a local admissions replacement you wish to keep.

To replace any core CSV directly, retain the column names and include each master MSOA exactly once. Supply counts and percentages consistently (same reference period and denominator within each measure). The browser rejects incomplete joins and invalid numeric values, but rerun independent analytical QA after changes. Do not mix new ethnicity counts with an old census denominator or new IMD flags with unrelated population weights.

## Tests

```sh
node --check app.js
node tests/core.test.js
```

Optional DOM smoke tests (Node 20+; requires a development-only package):

```sh
npm install --no-save jsdom
node tests/dom.test.js
```

jsdom tests exercise the page structure and event handlers, not browser rendering, layout, real pointer geometry or file-saving UX. Runtime app dependencies: none. Node is only needed for tests, not to serve the app.

## Deploy later, when authorised

The website is plain HTML/CSS/JavaScript. No compilation or backend is required. For any static host, copy `index.html`, `styles.css`, `core.js`, `app.js`, `refinements.js`, `methods.html`, `QA.md` and the complete `data/` folder while preserving their relative paths. The `raw/`, scripts and tests directories are not required by the live website.

For GitHub Pages, after you choose a repository and authorise publication, place those files at the root of the selected publishing branch, then enable Pages for that branch/root in the repository settings. The app uses relative paths and works under a repository subpath. Check the host's file-size rules and organisational publishing requirements. This project has not created a repository, registered a Site or deployed anything.

## Analytical interpretation

Default flags: top 20% of the **South Yorkshire MSOA distribution**, using inclusive linear-interpolated percentile cutoffs. Deprivation and ethnicity use percentages; men aged 40–74 uses a count. Ties can admit more than 20% of MSOAs. Place filters never recompute cutoffs. No composite risk score, z-score, forecast or hypertension prevalence estimate is created.

Core reference periods differ: population mid-2024; ethnicity Census 2021; deprivation IMD 2025 with its supplied mid-2022 population denominator. Admissions is 2016/17–2020/21, not contemporary service utilisation. The three population groups overlap, and total residents in matching areas are not unique grant beneficiaries.

## Attribution

ONS and OS data © Crown copyright and database right; Open Government Licence as applicable. Commons Library neighbourhood names: Open Parliament Licence. OHID Public health profiles: Crown copyright, accessed 20 October 2026. Original source links and published admissions metadata are retained in the project. No NHS endorsement or official publication status is implied.

## Revision 2 — replacing your GitHub Pages files

Read **GITHUB_UPDATE.md** for the exact replacement list. This ZIP keeps the original folder structure and adds `refinements.js` and `data/msoa_imd_scores.csv`; neither can be omitted. There is still no build step.

The visible percentile control is now inside the collapsed Advanced targeting settings in Data & Methods. The default stays 20%. New controls: map layer, quadrant X-axis, and a separate admissions highlight/restriction filter. The shortlist shows deprivation and ethnicity percentages, the chosen men count/percentage, admissions SAR, and all three original flags plus selected-criteria count. All original datasets, geography joins and targeting thresholds are preserved.

New tests:

```sh
python tests/weighted_imd_test.py
node tests/refinements.test.js
```

The second needs the same development-only jsdom package as the original DOM tests. The independent Python test verifies all 171 score calculations using Decimal arithmetic and checks that the six original source files are unchanged. The baseline hash checks deliberately fail on an intended later data refresh: review and update the baseline only after independently validating the replacement release.
