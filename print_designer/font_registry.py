# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
"""Registry of fonts bundled (self-hosted) with Print Designer.

This is the server-side mirror of `LocalFonts` in
`public/js/print_designer/defaultObjects.js`. It exists so the Jinja
templates that build the print/PDF HTML (render_google_fonts.html,
old_print_format.html, header_footer.html, header_footer_old.html) can tell
which font families must NOT get a Google Fonts CDN <link> tag, without
requiring the saved `printHeaderFonts` / `printBodyFonts` / `printFooterFonts`
data (which only ever recorded weight/italic usage, not font source) to
change shape.

When adding a new self-hosted font, update both this dict and the matching
entry in `LocalFonts` (defaultObjects.js) - see README.md "Adding a
self-hosted font".
"""

LOCAL_FONTS = {
	"Noto Sans Arabic": {
		"weight": [400, 500, 600, 700],
		"italic": [],
		"stylesheet": "local_fonts.bundle.css",
	},
	"Noto Kufi Arabic": {
		"weight": [400, 500, 600, 700],
		"italic": [],
		"stylesheet": "local_fonts.bundle.css",
	},
	"Noto Naskh Arabic": {
		"weight": [400, 500, 600, 700],
		"italic": [],
		"stylesheet": "local_fonts.bundle.css",
	},
	"Cairo": {
		"weight": [400, 500, 600, 700],
		"italic": [],
		"stylesheet": "local_fonts.bundle.css",
	},
	"Amiri": {
		"weight": [400, 700],
		"italic": [],
		"stylesheet": "local_fonts.bundle.css",
	},
	"Vazirmatn": {
		"weight": [400, 500, 600, 700],
		"italic": [],
		"stylesheet": "local_fonts.bundle.css",
	},
	"Tajawal": {
		"weight": [400, 500, 700],
		"italic": [],
		"stylesheet": "local_fonts.bundle.css",
	},
}


def is_local_font(font_family: str) -> bool:
	"""Whether `font_family` is bundled locally with Print Designer (as opposed
	to a Google Font fetched from the CDN)."""
	return font_family in LOCAL_FONTS


def filter_local_fonts(fonts: dict | None) -> dict | None:
	"""Strip locally-bundled fonts out of a Google-Fonts-style
	`{family: {weight: [...], italic: [...]}}` dict (as saved on
	`Print Format.print_designer_settings`), so callers can safely build a
	Google Fonts CDN URL from what remains.

	Locally bundled families are still rendered correctly - their
	`@font-face` rules are always included separately via
	`local_fonts.bundle.css` (see render_google_fonts.html).
	"""
	if not fonts:
		return fonts
	return {name: meta for name, meta in fonts.items() if name not in LOCAL_FONTS}
