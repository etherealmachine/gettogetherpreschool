# Quick Deploy Guide to GitHub Pages

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (e.g., `gettogetherpreschool`)
3. Do NOT initialize with README, .gitignore, or license (we already have these)
4. Click "Create repository"

## Step 2: Push Code to GitHub

Copy the commands shown on GitHub after creating the repo, or use these:

```bash
# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

## Step 3: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** (top menu)
3. Click **Pages** (left sidebar)
4. Under **Build and deployment**:
   - **Source**: Deploy from a branch
   - **Branch**: main
   - **Folder**: /docs
5. Click **Save**

## Step 4: Wait for Deployment

- GitHub will build and deploy your site (takes 1-2 minutes)
- Once done, you'll see a green checkmark and URL at the top
- Your site will be live at: `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/`

## Optional: Custom Domain

If you own `gettogetherpreschool.com` and want to use it:

1. Add CNAME file:
   ```bash
   echo "gettogetherpreschool.com" > docs/CNAME
   git add docs/CNAME
   git commit -m "Add custom domain"
   git push
   ```

2. Update DNS settings at your domain registrar:
   - Add A records pointing to:
     - `185.199.108.153`
     - `185.199.109.153`
     - `185.199.110.153`
     - `185.199.111.153`

3. In GitHub Settings → Pages:
   - Enter your custom domain: `gettogetherpreschool.com`
   - Check "Enforce HTTPS"
   - Click Save

4. Wait for DNS propagation (can take up to 24-48 hours)

## Testing Locally

Before deploying, you can test the site locally:

```bash
cd docs
python3 -m http.server 8000
```

Then visit http://localhost:8000 in your browser.

## Updating the Site

To pull fresh content from the live site:

```bash
node download-assets.js
git add docs/
git commit -m "Update site content"
git push
```

GitHub Pages will automatically redeploy with the new content.
