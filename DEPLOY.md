# Testing Locally

Before deploying, you can test the site locally:

```bash
npm run build:css
cd docs
python3 -m http.server 8000
```

Then visit http://localhost:8000 in your browser.

# Updating the Site

To pull fresh content from the live site:

```bash
node download-assets.js
git add docs/
git commit -m "Update site content"
git push
```

GitHub Pages will automatically redeploy with the new content.
