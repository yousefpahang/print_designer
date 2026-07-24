# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
import os
import re
import unittest

from print_designer.font_registry import LOCAL_FONTS, filter_local_fonts, is_local_font

# app root: apps/print_designer/print_designer/
APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_ROOT = os.path.join(APP_ROOT, "public")

# family -> (slug, [weight-name pairs used in the shipped filenames])
EXPECTED_LOCAL_FONTS = {
	"Noto Sans Arabic": {
		"slug": "noto-sans-arabic",
		"weight": [400, 500, 600, 700],
		"italic": [],
		"files": {
			400: "NotoSansArabic-Regular.woff2",
			500: "NotoSansArabic-Medium.woff2",
			600: "NotoSansArabic-SemiBold.woff2",
			700: "NotoSansArabic-Bold.woff2",
		},
	},
	"Noto Kufi Arabic": {
		"slug": "noto-kufi-arabic",
		"weight": [400, 500, 600, 700],
		"italic": [],
		"files": {
			400: "NotoKufiArabic-Regular.woff2",
			500: "NotoKufiArabic-Medium.woff2",
			600: "NotoKufiArabic-SemiBold.woff2",
			700: "NotoKufiArabic-Bold.woff2",
		},
	},
	"Noto Naskh Arabic": {
		"slug": "noto-naskh-arabic",
		"weight": [400, 500, 600, 700],
		"italic": [],
		"files": {
			400: "NotoNaskhArabic-Regular.woff2",
			500: "NotoNaskhArabic-Medium.woff2",
			600: "NotoNaskhArabic-SemiBold.woff2",
			700: "NotoNaskhArabic-Bold.woff2",
		},
	},
	"Cairo": {
		"slug": "cairo",
		"weight": [400, 500, 600, 700],
		"italic": [],
		"files": {
			400: "Cairo-Regular.woff2",
			500: "Cairo-Medium.woff2",
			600: "Cairo-SemiBold.woff2",
			700: "Cairo-Bold.woff2",
		},
	},
	"Amiri": {
		"slug": "amiri",
		"weight": [400, 700],
		"italic": [],
		"files": {
			400: "Amiri-Regular.woff2",
			700: "Amiri-Bold.woff2",
		},
	},
	"Vazirmatn": {
		"slug": "vazirmatn",
		"weight": [400, 500, 600, 700],
		"italic": [],
		"files": {
			400: "Vazirmatn-Regular.woff2",
			500: "Vazirmatn-Medium.woff2",
			600: "Vazirmatn-SemiBold.woff2",
			700: "Vazirmatn-Bold.woff2",
		},
	},
	"Tajawal": {
		"slug": "tajawal",
		"weight": [400, 500, 700],
		"italic": [],
		"files": {
			400: "Tajawal-Regular.woff2",
			500: "Tajawal-Medium.woff2",
			700: "Tajawal-Bold.woff2",
		},
	},
}

# Templates that must load local_fonts.bundle.css so its @font-face rules
# reach every surface that renders print/PDF content.
TEMPLATES_REQUIRING_LOCAL_FONT_CSS = [
	"print_designer/page/print_designer/jinja/macros/render_google_fonts.html",
	"print_designer/page/print_designer/jinja/old_print_format.html",
	"print_designer/page/print_designer/jinja/header_footer.html",
	"print_designer/page/print_designer/jinja/header_footer_old.html",
]


class TestFontRegistry(unittest.TestCase):
	def test_all_expected_local_fonts_are_registered(self):
		"""Every family this task bundles must appear in the selector registry
		(LOCAL_FONTS) with the exact weight metadata requested."""
		for family, expected in EXPECTED_LOCAL_FONTS.items():
			self.assertIn(family, LOCAL_FONTS, f"{family} missing from LOCAL_FONTS")
			entry = LOCAL_FONTS[family]
			self.assertEqual(entry["weight"], expected["weight"], f"{family} weight mismatch")
			self.assertEqual(entry["italic"], expected["italic"], f"{family} italic mismatch")
			self.assertEqual(entry["stylesheet"], "local_fonts.bundle.css", f"{family} stylesheet mismatch")

	def test_is_local_font_true_for_every_bundled_family(self):
		for family in EXPECTED_LOCAL_FONTS:
			self.assertTrue(is_local_font(family), f"{family} should be recognised as local")
		self.assertFalse(is_local_font("Inter"))
		self.assertFalse(is_local_font("Some Unregistered Typed Font"))

	def test_filter_local_fonts_strips_every_bundled_family(self):
		"""None of the bundled local families may ever produce a Google Fonts
		CDN link - filter_local_fonts must remove all of them, leaving only
		genuine Google fonts behind."""
		fonts = {name: {"weight": [400], "italic": []} for name in EXPECTED_LOCAL_FONTS}
		fonts["Inter"] = {"weight": [400, 700], "italic": []}
		fonts["Lato"] = {"weight": [400], "italic": [400]}

		filtered = filter_local_fonts(fonts)

		for family in EXPECTED_LOCAL_FONTS:
			self.assertNotIn(family, filtered, f"{family} must not reach the Google Fonts link builder")
		self.assertIn("Inter", filtered)
		self.assertIn("Lato", filtered)

	def test_filter_local_fonts_removes_only_local_entries(self):
		fonts = {
			"Inter": {"weight": [400, 700], "italic": []},
			"Noto Sans Arabic": {"weight": [400, 700], "italic": []},
			"Lato": {"weight": [400], "italic": [400]},
		}
		filtered = filter_local_fonts(fonts)
		self.assertNotIn("Noto Sans Arabic", filtered)
		self.assertIn("Inter", filtered)
		self.assertIn("Lato", filtered)
		self.assertEqual(filtered["Inter"], fonts["Inter"])

	def test_filter_local_fonts_handles_empty_and_none(self):
		self.assertIsNone(filter_local_fonts(None))
		self.assertEqual(filter_local_fonts({}), {})

	def test_filter_local_fonts_all_local_returns_empty_dict(self):
		fonts = {"Noto Sans Arabic": {"weight": [400], "italic": []}}
		filtered = filter_local_fonts(fonts)
		self.assertEqual(filtered, {})
		# an empty dict must be falsy so the Jinja templates skip rendering
		# a Google Fonts <link> tag entirely when only local fonts were used.
		self.assertFalse(filtered)

	def test_filter_local_fonts_does_not_mutate_input(self):
		fonts = {
			"Inter": {"weight": [400], "italic": []},
			"Noto Sans Arabic": {"weight": [400], "italic": []},
		}
		original_keys = set(fonts.keys())
		filter_local_fonts(fonts)
		self.assertEqual(set(fonts.keys()), original_keys)


class TestBundledFontAssetsOnDisk(unittest.TestCase):
	"""Guards against a font/license file silently going missing - every
	family+weight registered above must have a real WOFF2 file (and every
	family must have its OFL/license file) on disk."""

	def test_every_registered_weight_has_a_font_file(self):
		for family, expected in EXPECTED_LOCAL_FONTS.items():
			font_dir = os.path.join(PUBLIC_ROOT, "fonts", expected["slug"])
			for weight, filename in expected["files"].items():
				path = os.path.join(font_dir, filename)
				self.assertTrue(
					os.path.isfile(path), f"{family} weight {weight}: missing font file {path}"
				)
				self.assertGreater(os.path.getsize(path), 0, f"{family} weight {weight}: empty font file {path}")

	def test_every_local_font_family_has_a_license_file(self):
		for family, expected in EXPECTED_LOCAL_FONTS.items():
			license_path = os.path.join(PUBLIC_ROOT, "fonts", expected["slug"], "OFL.txt")
			self.assertTrue(os.path.isfile(license_path), f"{family}: missing license file {license_path}")
			with open(license_path) as f:
				content = f.read()
			self.assertIn("Open Font License", content, f"{family}: license file doesn't look like OFL")

	def test_local_fonts_stylesheet_declares_every_family_and_weight(self):
		css_path = os.path.join(PUBLIC_ROOT, "css", "local_fonts.bundle.css")
		with open(css_path) as f:
			css = f.read()

		# no global body font-family should ever be set by this stylesheet
		self.assertNotRegex(css, r"\bbody\s*\{", "local_fonts.bundle.css must not set a global body rule")

		for family, expected in EXPECTED_LOCAL_FONTS.items():
			for weight in expected["weight"]:
				pattern = (
					r'@font-face\s*\{[^}]*font-family:\s*"%s"[^}]*font-weight:\s*%d'
					% (re.escape(family), weight)
				)
				self.assertRegex(
					css,
					re.compile(pattern, re.DOTALL),
					f"{family} weight {weight}: no matching @font-face rule in local_fonts.bundle.css",
				)


class TestLocalFontCssIsIncludedInPrintHtml(unittest.TestCase):
	"""Every template involved in rendering print/PDF/preview HTML must load
	local_fonts.bundle.css, so bundled local fonts (Arabic/Persian) always
	reach the generated output, not just the editor canvas."""

	def test_templates_include_local_fonts_stylesheet(self):
		for relative_path in TEMPLATES_REQUIRING_LOCAL_FONT_CSS:
			path = os.path.join(APP_ROOT, relative_path)
			self.assertTrue(os.path.isfile(path), f"template not found: {path}")
			with open(path) as f:
				content = f.read()
			self.assertIn(
				"include_style('local_fonts.bundle.css')",
				content,
				f"{relative_path} does not include local_fonts.bundle.css",
			)

	def test_editor_loads_local_fonts_stylesheet(self):
		path = os.path.join(APP_ROOT, "print_designer/page/print_designer/print_designer.js")
		with open(path) as f:
			content = f.read()
		self.assertIn(
			'frappe.require("local_fonts.bundle.css")',
			content,
			"Designer editor bootstrap does not load local_fonts.bundle.css",
		)


class TestJsRegistryStaysInSync(unittest.TestCase):
	"""defaultObjects.js:LocalFonts (what the font-family selector in the
	Designer actually reads from) and font_registry.py:LOCAL_FONTS are two
	hand-maintained mirrors of the same data - see README.md "How it works".
	This is a lightweight text-level guard against them drifting apart,
	since there's no shared build step or JS test runner in this app to
	catch that automatically.
	"""

	def _read_default_objects_js(self):
		path = os.path.join(
			PUBLIC_ROOT, "js", "print_designer", "defaultObjects.js"
		)
		with open(path) as f:
			return f.read()

	def test_every_local_font_family_present_in_js_registry(self):
		js_source = self._read_default_objects_js()
		local_fonts_block = js_source[js_source.index("export const LocalFonts") : js_source.index(
			"export const FontRegistry"
		)]
		for family in LOCAL_FONTS:
			self.assertIn(
				f'"{family}"' if " " in family else family,
				local_fonts_block,
				f"{family} present in font_registry.py but not in defaultObjects.js LocalFonts",
			)
			self.assertIn(
				'source: "local"',
				local_fonts_block,
				"LocalFonts entries must be marked source: \"local\"",
			)

	def test_no_extra_local_fonts_only_in_js_registry(self):
		"""Every family name quoted inside the LocalFonts block should also
		be a key in the Python LOCAL_FONTS dict, catching the reverse drift
		(added on the JS side, forgotten on the Python side)."""
		js_source = self._read_default_objects_js()
		start = js_source.index("export const LocalFonts")
		end = js_source.index("export const FontRegistry")
		local_fonts_block = js_source[start:end]

		# family names are the quoted or bare keys immediately followed by ": {"
		declared_families = re.findall(r'(?:"([^"]+)"|^\s*([A-Za-z]+)):\s*\{', local_fonts_block, re.MULTILINE)
		declared_families = {a or b for a, b in declared_families}

		missing_in_python = declared_families - set(LOCAL_FONTS)
		self.assertEqual(
			missing_in_python,
			set(),
			f"Families declared in defaultObjects.js LocalFonts but missing from font_registry.py LOCAL_FONTS: {missing_in_python}",
		)


if __name__ == "__main__":
	unittest.main()
