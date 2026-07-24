<div align="center">

<a href="https://frappe.io/print-designer">
    <img src="https://github.com/frappe/print_designer/blob/develop/print_designer/public/images/print-designer-logo.svg" height="80" alt="Print Designer Logo">
</a>


<h1>Print Designer</h1>

**Frappe app to design print formats using interactive UI.**


![GitHub release (latest by date)](https://img.shields.io/github/v/release/frappe/print_designer)

<div>
    <picture>
        <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/b008b238-bd07-497b-ae1f-83d58600e0ca">
        <img width="1402" alt="Print Designer Screenshot" src="https://github.com/user-attachments/assets/b008b238-bd07-497b-ae1f-83d58600e0ca">
    </picture>
</div>

[Website](https://frappe.io/print-designer) - [Documentation](https://docs.frappe.io/print-designer)
</div>

## Print Designer

Print Designer is an open-source designing tool that allows businesses to create dynamic and professional-looking print formats. If you are looking to design print formats that enhance your brand image and streamline operational efficiency, then give it a try.


### Motivation

Frappe Framework and ERPNext have everything included, meaning you have all you need, including print format builder. This is easy to use, and you can easily create basic formats. If you need more customisable formats with complex layouts and alignment, you must create a custom format with code, which can take days or weeks.

As everything at Frappe follows a UI-first approach, why not have a way to design complex formats from the UI without any coding? Having used Adobe Illustrator, Photoshop, XD, and Figma in the past, I wanted to create a tool that would allow users to have a very high level of freedom to customize it just the way they like it. It initially started as a side project. After gaining some initial traction, I started working on it full-time. Our vision is to enable users to create all kinds of complex print formats from invoices to product brochures If you are looking for a one-stop solution for this, we welcome you to try the Print Designer.

### Key Features

- ✨ **Intuitive Visual Designer:** Make formats with intuitive visual interface and get realtime feedback.
- 📱 **Dynamic Data Integration:** Add and automatically populate data to your print format from selected document and all of its linked documents.
- 🛠️ **Table Editor:** Easily create and modify your table designs with visual feedback.
- 🧑‍💻 **Scripting Capabilities:** Power users can add custom data or custom html elements.
- 📄 **Multi Page:** Design multiple pages and create even more complex designs.

### Under the Hood

- [Frappe Framework](https://github.com/frappe/frappe): A full-stack web application framework.


## Getting Started (Production)

> **Warning**
>
> Please note that print designer is only compatible with develop and V15 version of frappe framework.

### Managed Hosting

Get started with your personal or business site with a few clicks on Frappe Cloud - our official hosting service.
<div>
	<a href="https://frappecloud.com/marketplace/apps/print_designer" target="_blank">
		<picture>
			<source media="(prefers-color-scheme: dark)" srcset="https://frappe.io/files/try-on-fc-white.png">
			<img src="https://frappe.io/files/try-on-fc-black.png" alt="Try on Frappe Cloud" height="28" />
		</picture>
	</a>
</div>


### Self Hosting

Follow these steps to set up Print Designer in production:

**Step 1**: Download the easy install script

```bash
wget https://frappe.io/easy-install.py
```

**Step 2**: Run the deployment command

```bash
python3 ./easy-install.py deploy \
    --project=pd_prod_setup \
    --email=email@example.com \
    --image=ghcr.io/frappe/print_designer \
    --version=stable \
    --app=print_designer \
    --sitename subdomain.domain.tld
```

Replace the following parameters with your values:
- `email@example.com`: Your email address
- `subdomain.domain.tld`: Your domain name where print designer will be hosted

The script will set up a production-ready instance of Print Designer with all the necessary configurations in about 5 minutes.

## Getting Started (Development)

### Docker

You need Docker, docker-compose and git setup on your machine. Refer [Docker documentation](https://docs.docker.com/). After that, run following command:

**Step 1**: Setup folder and download the required files

```bash
mkdir frappe-pd && cd frappe-pd
wget -O docker-compose.yml https://raw.githubusercontent.com/frappe/print_designer/develop/docker/docker-compose.yml
wget -O init.sh https://raw.githubusercontent.com/frappe/print_designer/develop/docker/init.sh
```

**Step 2**: Run the container

```bash
docker compose up
```

Wait until the setup script creates a site and you see `Current Site set to print-designer.localhost` in the terminal. Once done, the site [http://print-designer.localhost:8000](http://print-designer.localhost:8000) should now be available.

**Credentials:**
Username: `Administrator`
Password: `admin`

## Getting Started (Development)

### Local Setup

1. [Setup Bench](https://docs.frappe.io/framework/user/en/installation).
1. In the frappe-bench directory, run `bench start` and keep it running.
1. Open a new terminal session and cd into `frappe-bench` directory and run following commands:
```bash
bench get-app print_designer
bench new-site print-designer.localhost --install-app print_designer
bench browse print-designer.localhost --user Administrator
```
1. Access the print designer page at `print-designer.localhost:8000/app/print-designer` in your web browser.


## Fonts

Print Designer's font-family picker draws from a generic **font registry**
that supports two font sources:

- `google` - fetched at render time from `fonts.googleapis.com`/`fonts.gstatic.com`.
  This is the original behaviour and covers every font that shipped before
  self-hosted font support was added (Inter, Lato, Montserrat, etc.) -
  unchanged, still requires outbound internet access from wherever the
  editor/PDF renderer runs.
- `local` - bundled inside this app under `public/fonts/`, loaded via a
  self-hosted `@font-face` stylesheet. No CDN request is made, so these
  fonts work fully offline and render identically whether or not the server
  has internet access.

### Bundled local fonts

All entries below are `source: "local"` in the registry, are licensed under
the SIL Open Font License 1.1 (license text preserved alongside each font's
files in `public/fonts/<slug>/OFL.txt`), and never generate a Google Fonts
CDN request.

| Family | Weights | Slug | Source | Intended use |
|---|---|---|---|---|
| Noto Sans Arabic | 400, 500, 600, 700 | `noto-sans-arabic` | [Noto Project](https://github.com/notofonts/arabic) | Neutral UI/body text, general-purpose Arabic invoices |
| Noto Kufi Arabic | 400, 500, 600, 700 | `noto-kufi-arabic` | [Noto Project](https://github.com/notofonts/kufi-arabic) | Geometric/modern headings, letterheads, company names |
| Noto Naskh Arabic | 400, 500, 600, 700 | `noto-naskh-arabic` | [Noto Project](https://github.com/notofonts/naskh-arabic) | Formal/traditional Arabic body text, contracts, legal documents |
| Cairo | 400, 500, 600, 700 | `cairo` | [Cairo Project](https://github.com/Gue3bara/Cairo) | Modern bilingual (Arabic + Latin) UI and invoice text |
| Amiri | 400, 700 | `amiri` | [The Amiri Project](https://github.com/aliftype/amiri) | Classical Naskh calligraphic style - formal Arabic documents, headings; not intended for dense small-print tables (upstream only publishes Regular/Bold, no Medium/SemiBold) |
| Vazirmatn | 400, 500, 600, 700 | `vazirmatn` | [Vazirmatn Project](https://github.com/rastikerdar/vazirmatn) | Persian (Farsi) invoices and UI text; also covers Arabic |
| Tajawal | 400, 500, 700 | `tajawal` | Boutros International, via Google Fonts | Rounded modern Arabic headings and UI text (upstream has no 600 weight) |

**Bilingual Arabic/Latin note:** all of the families above are self-hosted
using only their Arabic-script glyph subset (matching how Google's own
Noto Sans Arabic CDN stylesheet is subsetted), so Latin text sharing a text
element with one of these fonts falls back to the renderer's default Latin
font rather than a matched companion typeface - see "Known limitation"
below. If your invoices need first-class matched Arabic+Latin pairing in a
single typeface, **Dubai** (Government of Dubai's bilingual font) is the
better fit once we're supplied a properly licensed package we're authorized
to bundle - it is not open-source/OFL like the fonts above, so it has not
been added here. Do not add a "Dubai" or "Noor" entry to either registry
without first confirming licensing terms with whoever supplies those files.

### How it works

The registry lives in two mirrored places, kept in sync manually:

- `public/js/print_designer/defaultObjects.js` - `LocalFonts` (metadata for
  bundled fonts) and `FontRegistry` (the merged `google` + `local` registry
  the Designer UI actually reads from: font-family autocomplete, weight
  picker, italic-availability check).
- `print_designer/font_registry.py` - `LOCAL_FONTS`, used server-side by the
  print/PDF-rendering Jinja templates to keep local fonts out of the
  Google Fonts CDN `<link>` tags (`filter_local_fonts`, registered as a
  Jinja method).

Every registry entry (Google or local) is normalized to:

```js
{ weight: number[], italic: number[], source: "google" | "local" }
```

An unregistered/manually-typed font family (no matching entry) is handled
safely everywhere it's read: the weight picker falls back to the full
100-900 weight list instead of throwing, and the italic toggle is simply
treated as unavailable. Existing saved Print Formats that reference a
Google font, or even an unrecognised font name, keep rendering exactly as
before.

### Where the font CSS is loaded

Local fonts' `@font-face` rules live in `public/css/local_fonts.bundle.css`
(declarations only - it never sets a global `body { font-family }`, so it
has no effect on elements that don't explicitly select a local font). It is
loaded in every surface that renders print content:

| Surface | Where it's loaded |
|---|---|
| Designer editor & preview canvas | `frappe.require("local_fonts.bundle.css")` in `print_designer/page/print_designer/print_designer.js` |
| Print/PDF body (schema ≥ 1.1.0) | `render_google_fonts.html` macro, via `include_style('local_fonts.bundle.css')` |
| Print/PDF body (legacy schema) | `old_print_format.html`, same `include_style()` call |
| PDF header/footer (chrome generator) | `header_footer.html` |
| PDF header/footer (wkhtmltopdf generator) | `header_footer_old.html` |

`include_style()` (a standard Frappe Jinja global) resolves the `*.bundle.css`
logical name through the site's asset manifest and returns an absolute
`<link>` tag - the same mechanism Frappe itself uses for `print.bundle.css`.
Since Print Designer's Chrome PDF renderer navigates to the site's own
origin before content is injected, this asset resolves as a normal
same-origin request - no external network access required.

### Adding another self-hosted font

1. Obtain real, licensed-for-embedding font files (WOFF2 preferred for both
   the editor and the Chrome/CDP PDF renderer - no TTF/OTF conversion is
   needed since the renderer is a full browser engine). Keep the license
   file (e.g. `OFL.txt`) alongside the font files - do not bundle a font
   without one.
2. Add the files under `public/fonts/<family-slug>/`, following the
   `noto-sans-arabic/` example.
3. Add `@font-face` rules to `public/css/local_fonts.bundle.css` (or a new
   `*.bundle.css` file if you'd rather not grow this one - remember to
   `include_style()`/`frappe.require()` it in the same 5 places listed
   above). Use absolute `/assets/print_designer/fonts/...` URLs so the
   reference survives bundling regardless of where the compiled CSS ends up.
   Do not add a global `font-family` rule.
4. Register the family in **both**:
   - `LocalFonts` in `public/js/print_designer/defaultObjects.js`
     (`weight`, `italic`, `source: "local"`, `stylesheet`).
   - `LOCAL_FONTS` in `print_designer/font_registry.py`
     (`weight`, `italic`, `stylesheet`).
5. Rebuild and clear cache:
   ```bash
   bench build --app print_designer
   bench clear-cache
   ```
6. **Test PDF output specifically**, not just the editor canvas - the
   Designer canvas is a live browser context and will render a working
   `@font-face` correctly, but that doesn't guarantee the same font renders
   (or shapes complex scripts) correctly through the PDF generation path.
   Generate a PDF via both the `chrome` and `wkhtmltopdf` generators if your
   deployment supports both, with external network access blocked, and
   inspect the actual output - missing glyphs or fallback-font substitution
   in the PDF only shows up here, not in the editor.

### Known limitation

All of the locally bundled fonts above are self-hosted using only their
Arabic/Persian glyph subset, not Latin. Mixed-script text inside a
*single* text element will render the Latin portion in the renderer's
default fallback font, not your Latin font of choice. For Arabic/Persian +
Latin content in the same print format (e.g. an invoice with Arabic labels
and Latin invoice numbers), use separate text elements per script and set
each element's font family independently - Print Designer already supports
per-element font selection. See the bilingual note above for what to use if
you need a single matched typeface across both scripts.

## FAQ
1. Incorrect PDF Page Size

    - Frappe / Print Designer requires at least  [version 0.12.5 with patched qt](https://frappeframework.com/docs/v14/user/en/installation#pre-requisites)

    - Install correct version by following [installation guide](https://frappeframework.com/docs/v14/user/en/installation) and confirm : 

    ```
    wkhtmltopdf --version
    ```
    - output should be similar to `wkhtmltopdf 0.12.6 (with patched qt)`


2. Mac Installation Error
    - If error has `npm ERR! node-pre-gyp WARN Pre-built binaries not found for canvas@x.x.x` it means that there aren't any pre-built binaries for your system so it will try to compile them and in order to do that you need 
    - Xcode Command Line Tools `xcode-select --install`
    - [HomeBrew](https://brew.sh/) and `brew install pkg-config cairo pango libpng jpeg giflib librsvg pixman`
    - If you have **xcode 10.0 or higher** installed, in order to build from source you need **NPM 6.4.1 or higher** `npm install -g npm@latest`.

3. Linux ARM CPU Installation Error
    - If error has `node-pre-gyp WARN Pre-built binaries not installable for canvas@x.x.x and node@x.x.x` it means that there aren't any pre-built binaries for your system so it will try to compile them
    - In order to do that you need `sudo apt-get update && sudo apt-get install build-essential libcairo2-dev libpango1.0-dev libjpeg-dev libgif-dev librsvg2-dev`

<br>

## Links

- [Telegram Public Group](https://t.me/+beFRbDSDEgtjYmY9)
- [Discuss Forum](https://discuss.frappe.io/c/print-designer/84)
- [Documentation](https://docs.frappe.io/print_designer)


<br>
<div align="center">
	<a href="https://frappe.io" target="_blank">
		<picture>
			<source media="(prefers-color-scheme: dark)" srcset="https://frappe.io/files/Frappe-white.png">
			<img src="https://frappe.io/files/Frappe-black.png" alt="Frappe Technologies" height="28"/>
		</picture>
	</a>
</div>
