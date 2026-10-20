# GitHub Pages update — version 2.1

This is a focused update to the existing polished dashboard. Nothing has been published or changed in your repository.

## Replace these four live files

Extract the ZIP, open its `south-yorkshire-explorer` folder, and replace the matching files at the same level as the current index.html in your GitHub repository:

1. **index.html** — MSOA wording, revised axis selector labels and default selection.
2. **app.js** — consistent area wording, including Area Explorer and the displayed data dictionary.
3. **refinements.js** — dynamic quintile/custom-percentage explanations, weighted-IMD default, clearer quadrant labels and benchmark tooltips.
4. **methods.html** — updated Data & Methods explanations.

Replace all four together. **Do not upload the ZIP itself or nest an extra project folder.** Keep the existing GitHub Pages publishing branch/folder setting. There is no build step.

## Documentation and development files

Also replace README.md, QA.md, CHANGELOG.md, GITHUB_UPDATE.md, package.json, tests/refinements.test.js and the supplied test logs. Add tests/terminology.test.js and tests/terminology-results.txt.

No replacement of data/, scripts/, core.js or styles.css is required: all were verified byte-for-byte unchanged. The complete ZIP includes these files for convenience. If you have installed your own newer admissions CSV, keep it; these interface changes do not require reverting to the bundled snapshot.

## After committing your update

Wait for GitHub Pages to finish, then refresh with Ctrl+F5. Verify:

- Cards use “MSOAs meeting targeting criteria”, “Residents in selected MSOAs” and “MSOAs meeting all three criteria”.
- The explanation describes the highest South Yorkshire quintile by default.
- Both quadrant pages initially show the population-weighted average IMD 2025 score.
- The horizontal ethnicity line shows **24.51%**, with its full cutoff and calculation available through the information tooltip.
- The vertical average-score line shows **29.11**, explicitly described as a supplementary descriptive benchmark.
- Switching to the concentration percentage shows its original **72.82%** cutoff and leaves targeting flags unchanged.
- Advanced 10% or 30% settings update explanations to the custom percentage, and Reset restores 20% and the average-score axis.

With the bundled snapshot and default filters, totals remain **77 of 171 MSOAs**, **736,488 residents**, **3 MSOAs meeting all three criteria**, and **59 with SAR >100**, with admissions coverage **76 of 77**. Your own admissions replacement may change the admissions figures.

Automated analytical and DOM interaction tests passed. Actual browser visual testing was unavailable; check the page in your intended browser after replacement.
