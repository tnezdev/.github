# Organization profile header

`workbench-light.png` and `workbench-dark.png` are theme-aware, transparent versions of the selected Workbench composition. The profile introduction remains unchanged.

## Brand source and application

Reference: `tnezdev/brand` at revision `0ecee6ba7f503c635d18a5c525533b9da6bf8ee8`, specifically `BRAND.md`, `TYPOGRAPHY.md`, and the current `index.html` application board. Historical palette and underline studies are not used.

Surface: a public GitHub organization introduction. Each treatment uses the complete matching Printed red role set. The original green/gold palette and improvised arrow are not used. DM Sans remains local and unmodified; the name uses weight 550 and -.04em tracking.

The open chevron preserves the 100-unit coordinate system, points `28,22 72,50 28,78`, 8-unit stroke, rounded caps and joins, and right-facing orientation. Its dimensions and spacing scale with the reference lockup. Optical alignment is measured against actual lowercase ink at export size rather than reapplying a CSS line-box offset to raster coordinates.

The wordmark and two-path decoration remain. Small labels, byline, tagline, grid, and bottom rule were removed to reduce clutter; the prose below already carries that information. The two paths are decoration, not a second identity mark.

The brand surface color fades to transparency on all four edges, with a longer fade at the bottom. Foreground type and marks stay opaque. This is an alpha fade of the selected background role, not an additional hue palette. The larger identity and removal of repeated metadata give the header more breathing room.

## GitHub integration

`profile/README.md` uses GitHub-supported `picture`/`source` markup and an image with `width="100%"`. Dark and light source media select the appropriate export; the fallback is light. Alt text names the identity, while the full introduction remains ordinary accessible README text.

Full width means the README content column, not the entire browser or organization page. GitHub still owns the surrounding container and padding. No inline CSS, page-background manipulation, or negative margins are shipped.

## Reproduce

With Python and Pillow available, run from the repository root:

    python scripts/render_workbench.py

Verified with Pillow 12.3.0. The renderer uses the bundled DM Sans variable font and no network or system-font dependency. `fonts/OFL.txt` carries the original SIL Open Font License. Both outputs are 2400 × 600 RGBA PNGs.

## Verification and limits

Verified exact role agreement with both brand palettes, byte-identical regeneration, valid RGBA exports, fully transparent outer edges, in-bounds identity lettering, and unchanged introduction text. Primary identity and accent contrast remain above 4.5:1 across the fade when composited onto white, default-dark, and dimmed-dark page-color samples. This does not certify every custom or accessibility theme.

GitHub's Markdown API preserves the picture sources and full-width attribute. Before upload, that sanitized content and the exact exports were previewed inside GitHub's live README layout, using fresh page loads for each emulated color scheme. At 1280, 390, and 320px viewport widths in both light and dark, the image selected the correct asset, matched the content-column width, and introduced no page or paragraph overflow. The actual content widths were 846, 309, and 239px respectively. Desktop and phone screenshots were visually reviewed.

These checks exercise desktop-browser responsive layouts, not every native GitHub client or high-contrast theme. The raster header contains only the identity and decoration; supporting copy is no longer reduced to tiny image text. Publication remains subject to the consuming PR's approval.
