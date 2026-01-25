# Get Together Preschool - Static Website

This repository contains a clean, multi-page static HTML website for Get Together Preschool, deployed to GitHub Pages.

## Structure

```
docs/
├── css/
│   └── site.css        # Consolidated stylesheet
├── fonts/
│   └── *.woff2         # Web font files
├── images/             # All image assets (16 images)
├── index.html          # Home page
├── about.html          # Program philosophy
├── qualifications.html # Teacher credentials
├── gallery.html        # Photo gallery
├── programs.html       # Daily schedule & menu
├── contact.html        # Contact info & map
├── logo.png            # Site logo/favicon
├── .nojekyll          # Tells GitHub Pages not to use Jekyll
└── CNAME              # Custom domain configuration
```

## Features

- **6 clean HTML pages** with semantic markup
- **Zero JavaScript** - pure HTML & CSS (except Google Maps iframe)
- **Single CSS file** - consolidated and organized
- **Organized assets** - separate folders for CSS, fonts, and images
- **Fully responsive** - works on mobile, tablet, and desktop
- **Fast loading** - no JavaScript frameworks, just static content

## Deploying to GitHub Pages

### Method 1: Deploy from `docs` folder on main branch (Recommended)

1. Push this repository to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Static site for GitHub Pages"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

2. Go to your repository on GitHub
3. Click on **Settings** → **Pages**
4. Under **Source**, select:
   - Branch: `main`
   - Folder: `/docs`
5. Click **Save**
6. Your site will be published at `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/`

### Method 2: Deploy from `gh-pages` branch

1. Create a `gh-pages` branch with only the docs contents:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main

   # Create gh-pages branch
   git checkout --orphan gh-pages
   git rm -rf .
   cp -r docs/* .
   git add .
   git commit -m "Deploy to GitHub Pages"

   # Push both branches
   git push -u origin gh-pages
   git checkout main
   git push -u origin main
   ```

2. Go to **Settings** → **Pages** and select:
   - Branch: `gh-pages`
   - Folder: `/ (root)`

## Custom Domain

The site is configured to use the custom domain `gettogetherpreschool.com` via the `CNAME` file.

To use a different custom domain:

1. Update the `CNAME` file:
   ```bash
   echo "yourdomain.com" > docs/CNAME
   ```

2. Configure your DNS settings:
   - Add an A record pointing to GitHub Pages IPs:
     - 185.199.108.153
     - 185.199.109.153
     - 185.199.110.153
     - 185.199.111.153
   - Or add a CNAME record pointing to `YOUR_USERNAME.github.io`

3. In GitHub Settings → Pages, enter your custom domain and save

## Local Testing

To test the site locally, use any static file server:

```bash
# Using Python 3
cd docs
python3 -m http.server 8000

# Using Node.js (npx)
cd docs
npx serve

# Using PHP
cd docs
php -S localhost:8000
```

Then open http://localhost:8000 in your browser.

## Making Changes

### First Time Setup

Install dependencies:
```bash
npm install
```

### Editing Content

1. Open the HTML file you want to edit (e.g., `docs/about.html`)
2. Make your changes to the content
3. Save and commit:
   ```bash
   git add docs/
   git commit -m "Update content"
   git push
   ```

### Editing Styles

This site uses Tailwind CSS with a build process to keep the CSS file small.

1. Edit HTML classes directly in `docs/*.html` files
2. For custom CSS, edit `src/input.css`
3. Rebuild the CSS:
   ```bash
   npm run build:css
   ```
4. Commit and push the changes

To watch for changes and auto-rebuild:
```bash
npm run watch:css
```

### Adding Images

1. Add image files to `docs/images/`
2. Reference them in HTML with `./images/filename.jpg`
3. Commit and push

## Notes

- **Tailwind CSS** - optimized build process generates minimal CSS (~16KB)
- **No JavaScript dependencies** - fast, secure, and accessible
- **Self-contained** - all assets are in the `docs` folder
- **Easy to maintain** - clean, readable HTML with utility classes
- **SEO optimized** - each page has unique title and meta description
- **GitHub Pages ready** - `.nojekyll` prevents Jekyll processing

## Browser Support

The site uses modern CSS (Tailwind utility classes) and works in all modern browsers:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)
