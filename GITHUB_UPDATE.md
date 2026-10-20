# Replace files in the existing GitHub Pages project

This revised project is prepared for your existing site:
https://ashkinguk.github.io/south-yorkshire-prevention-explorer/

**No repository changes or publication have been made.** The published app.js was read and matched the first-build project exactly before editing.

## Recommended: replace the complete project contents

1. Download and extract the replacement ZIP.
2. Open its `south-yorkshire-explorer` folder.
3. Back up any local admissions CSV you have independently updated.
4. In your existing GitHub repository, replace the matching files with the contents of this folder. Put `index.html` at the **same level as the existing index.html**. Do not upload the ZIP itself, and do not nest a second `south-yorkshire-explorer` folder inside the repository root.
5. Commit when you are ready to publish. Keep your existing Pages branch/folder setting; there is no build or hosting-configuration change.
6. After Pages finishes, refresh the site with Ctrl+F5. Check that the sidebar appears, the percentile setting is in Data & Methods, and both map layers and quadrant axes work.

## Minimum live-site replacements

| Action | Path |
|---|---|
| Replace | index.html |
| Replace | styles.css |
| Replace | core.js |
| Replace | app.js |
| **Add — required** | **refinements.js** |
| Replace | methods.html |
| **Add — required** | **data/msoa_imd_scores.csv** |
| Replace | data/dictionary.csv |
| Replace | data/lsoa_deprivation_audit.csv (now includes LSOA IMD scores) |
| Replace | data/msoa_processed_default.csv (now includes supplementary IMD fields) |
| Replace | QA.md, README.md |
| Add | CHANGELOG.md, GITHUB_UPDATE.md |

Keep the remaining `data/` files: they are still required and were verified unchanged. The ZIP contains them all, so replacing the complete `data/` folder is also safe **unless you have your own newer admissions data**, which you should retain after validating its schema. The browser automatically uses replacement admissions source/periods for the KPI, map, tooltips, shortlist and filters.

## Keep the reproducible source project updated too

Replace `scripts/prepare.py`, `scripts/dictionary.py`, `package.json`, `tests/dom.test.js` and the test-result logs. Add `tests/weighted_imd_test.py`, `tests/refinements.test.js` and `tests/baseline-hashes.json`. Keep the acquisition scripts, raw official responses, other original tests, dependency information and Windows launcher. The ZIP includes the complete set.

A local admissions replacement does not require a rebuild. Do not rerun `prepare.py` after installing a local admissions replacement you wish to retain: that script intentionally regenerates the bundled official snapshot.

## Acceptance check after replacement

With all defaults and South Yorkshire selected, the four cards should show:

- **77 of 171** neighbourhoods.
- **736,488** residents.
- **3** neighbourhoods meeting all three original criteria.
- **59** areas with SAR above 100, with admissions data available for **76 of 77** shortlisted areas.

The secondary row should show **371,700**, **172,594** and **137,889**, respectively. These are separate, overlapping populations with different reference periods.

These expected figures apply to the bundled snapshot, not necessarily to a newer local admissions replacement or changed advanced settings. A full visual browser check remains necessary: this development session supported automated data and DOM tests, but not browser rendering.
