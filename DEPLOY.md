# Building the Site

This site is built with [Hugo](https://gohugo.io/) and Tailwind CSS. The output is static HTML, CSS, and assets.

## Prerequisites

- [Node.js](https://nodejs.org/) (for Tailwind CSS)
- [Hugo](https://gohugo.io/installation/) (extended edition optional)

Install Hugo (macOS with Homebrew):

```bash
brew install hugo
```

## Build for GitHub Pages (output to `docs/`)

GitHub Pages is configured to serve from the `docs/` folder. Build the site into `docs/`:

```bash
npm install
npm run build:gh
```

This will:

1. Build Tailwind CSS into `static/css/site.css`
2. Run Hugo with `--destination docs`, generating the site into `docs/`

Then commit and push:

```bash
git add docs/
git add static/ content/ layouts/ hugo.toml src/ package.json tailwind.config.js
git commit -m "Update site"
git push
```

## Local development

Run the Hugo dev server (with live reload). Build CSS first, then in one terminal watch CSS and in another run Hugo:

```bash
npm run build:css
npm run watch:css
```

In a second terminal:

```bash
hugo server
```

Visit http://localhost:1313. To see the site as it will be when deployed (with `docs/` as root), you can also serve the built output:

```bash
npm run build:gh
cd docs && python3 -m http.server 8000
```

Then visit http://localhost:8000.

## Project structure

- `content/` – Markdown pages (one file per page with front matter and `layout`).
- `layouts/` – Hugo templates: `_default/baseof.html`, `index.html`, `_default/single.html`, and layout overrides (`apply`, `contact`, `gallery`, `programs`, `spring_camp`, `thanks`).
- `static/` – Static assets (images, CSS, JS). Hugo copies these into the output. Tailwind builds into `static/css/site.css`.
- `src/input.css` – Tailwind source and CSS variables.
- `hugo.toml` – Site config and params (contact info, form URLs, etc.).

## Adding or editing content

- **Copy and assets**: Add images to `static/images/`. The home carousel and gallery page list images from this folder automatically (excluding `logo.png`).
- **Text and structure**: Edit the relevant layout in `layouts/_default/` or the content file in `content/`. Page titles and meta descriptions are set in each content file’s front matter.
- **Site-wide settings**: Edit `hugo.toml` (e.g. phone, email, form redirect URL, map embed).

## Gallery script (optional)

The Python script `scripts/build_gallery.py` can still be used to convert HEIC images to JPEG and downsample images in `docs/images/`. After switching to Hugo, run it against `static/images/` if you keep source images there, or adapt the script to use `static/images/` and then run `npm run build:gh` to regenerate the site. The Hugo gallery and home carousel read from `static/images/` at build time.
