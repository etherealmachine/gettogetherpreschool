# Get Together Preschool - Static Website

This repository contains a static copy of the Get Together Preschool website (https://gettogetherpreschool.com/) for deployment to GitHub Pages.

## Structure

```
docs/
├── index.html          # Main HTML file
├── images/             # All image assets
├── _next/              # Next.js static assets (CSS, JS, fonts)
└── .nojekyll          # Tells GitHub Pages not to use Jekyll
```

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

## Custom Domain (Optional)

If you want to use a custom domain (e.g., gettogetherpreschool.com):

1. Add a `CNAME` file to the `docs` directory:
   ```bash
   echo "gettogetherpreschool.com" > docs/CNAME
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

To test the site locally, you can use any static file server:

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

## Updating the Site

To re-crawl and update the site from the live version:

```bash
node download-assets.js
```

This will download the latest version of all assets from https://gettogetherpreschool.com/

## Notes

- The site is a static snapshot and won't receive automatic updates from the original site
- All assets are self-contained in the `docs` folder
- The `.nojekyll` file prevents GitHub Pages from processing the site with Jekyll
- The original site is a Next.js application, but this version is purely static HTML/CSS/JS
