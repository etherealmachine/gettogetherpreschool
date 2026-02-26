# Get Together Preschool – Hugo static site

Static website for Get Together Preschool, built with [Hugo](https://gohugo.io/) and Tailwind CSS, deployed to GitHub Pages from the `docs/` folder.

## Structure

- **`content/`** – Markdown pages (one per page) with front matter and `layout` pointing to a custom template.
- **`layouts/`** – Hugo templates: base layout, nav/footer partials, `index.html` (home), and layouts for apply, contact, gallery, programs, spring_camp, thanks.
- **`static/`** – Static assets: `images/`, `css/site.css` (built by Tailwind), `javascript/`, `CNAME`, `.nojekyll`.
- **`src/input.css`** – Tailwind source and CSS variables.
- **`hugo.toml`** – Site config and params (contact info, form URLs, map embed, etc.).

## Prerequisites

- [Node.js](https://nodejs.org/) (for Tailwind CSS)
- [Hugo](https://gohugo.io/installation/) (e.g. `brew install hugo`)

## Build and deploy

1. Install dependencies and build the site into `docs/`:

   ```bash
   npm install
   npm run build:gh
   ```

2. Commit and push (GitHub Pages serves from `docs/`):

   ```bash
   git add .
   git commit -m "Update site"
   git push
   ```

See [DEPLOY.md](DEPLOY.md) for more detail, local development, and content/structure notes.

## Features

- **Hugo** – Single command builds the full site; content and layout are separate.
- **Tailwind CSS** – Utility CSS built from `src/input.css` into `static/css/site.css`.
- **Responsive** – Mobile menu, gallery grid, and forms work across screen sizes.
- **Bilingual** – CJK font toggle (Simplified / Traditional) via `cjk-font-toggle.js`.
- **Forms** – Contact and apply forms use FormSubmit.co with redirect to `/thanks/`.

## Custom domain

The site uses the custom domain `gettogetherpreschool.com` via `static/CNAME`. GitHub Pages is set to use the `docs/` folder on the main branch.
