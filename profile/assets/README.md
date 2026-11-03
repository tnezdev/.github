# Organization profile banner

`workbench.png` is the selected Workbench composition, aligned with the current tnezdev identity. The profile introduction remains unchanged.

## Brand source

Reference: `tnezdev/brand` at revision `0ecee6ba7f503c635d18a5c525533b9da6bf8ee8`, specifically `BRAND.md`, `TYPOGRAPHY.md`, and the current `index.html` application board. Historical palette and underline studies are not used.

Surface: a public GitHub organization introduction. Treatment: Printed red, dark. This banner stays dark in either GitHub theme, like the reference's fixed-dark title treatment; it does not restyle GitHub's surrounding interface.

Applied roles: navy `#18243B` background, stone `#F2F0EB` primary text, `#B5C0D0` secondary text, `#F17864` accent, and `#42516C` decorative separators. DM Sans replaces the provisional DejaVu type. The name uses weight 550 and -.04em tracking.

The open chevron preserves the reference's 100-unit coordinate system, points `28,22 72,50 28,78`, 8-unit stroke, rounded caps and joins, and right-facing orientation. Its dimensions and spacing scale with the reference lockup. Optical alignment is measured against the actual lowercase ink at export size rather than reapplying a CSS line-box offset to raster coordinates.

The two-path decoration and dark Workbench layout are retained. The provisional green/gold palette and improvised arrow are removed. The two routes are composition-specific decoration, not an alternate identity mark.

## Reproduce

From the repository root, with Python and Pillow available:

    python scripts/render_workbench.py

Verified with Pillow 12.3.0. The renderer uses the bundled, unmodified DM Sans variable font and no network or system-font dependency. `fonts/OFL.txt` carries the font's SIL Open Font License. The output is a 2400 × 660 PNG; the font is rasterized so the README does not depend on custom font loading.

## Verification and limits

The renderer checks text bounds, PNG dimensions/decoding, and solid-color contrast: primary text/background 13.61:1; secondary text/background 8.43:1; accent/background 5.62:1. Decorative separators are not essential UI boundaries.

Actual exports were visually reviewed at 1200, 768, 390, and 320 pixels wide. No clipping, overlap, or chevron alignment defects were found. Small supporting lettering is not independently readable at narrow phone widths: the banner is a fixed raster composition, not a responsive text layout. The introduction repeats that information in ordinary README text, and the image has descriptive alt text. No unique information depends on the decoration or tiny lettering.

The PNG and local Markdown link are checked; this does not certify every GitHub client or substitute for review of the rendered PR. The profile remains unmerged pending approval.
