const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const { URL } = require('url');

const baseUrl = 'https://gettogetherpreschool.com';
const outputDir = './docs';

// Create directory if it doesn't exist
function ensureDir(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

// Download a file
function downloadFile(url, outputPath) {
  return new Promise((resolve, reject) => {
    const fullUrl = url.startsWith('http') ? url : `${baseUrl}${url}`;
    const protocol = fullUrl.startsWith('https') ? https : http;

    ensureDir(path.dirname(outputPath));

    console.log(`Downloading: ${fullUrl} -> ${outputPath}`);

    const file = fs.createWriteStream(outputPath);
    protocol.get(fullUrl, (response) => {
      if (response.statusCode === 200) {
        response.pipe(file);
        file.on('finish', () => {
          file.close();
          console.log(`✓ Downloaded: ${outputPath}`);
          resolve();
        });
      } else {
        fs.unlink(outputPath, () => {});
        reject(new Error(`Failed to download ${fullUrl}: ${response.statusCode}`));
      }
    }).on('error', (err) => {
      fs.unlink(outputPath, () => {});
      reject(err);
    });
  });
}

// Parse HTML to find all assets
async function downloadAssets() {
  const html = fs.readFileSync(path.join(outputDir, 'index.html'), 'utf8');

  // Extract all asset URLs
  const assets = new Set();

  // Images
  const imgRegex = /(?:src|href)=["']([^"']+\.(?:png|jpg|jpeg|gif|svg|webp))["']/gi;
  let match;
  while ((match = imgRegex.exec(html)) !== null) {
    assets.add(match[1]);
  }

  // JS files
  const jsRegex = /(?:src)=["']([^"']+\.js)["']/gi;
  while ((match = jsRegex.exec(html)) !== null) {
    assets.add(match[1]);
  }

  // CSS files
  const cssRegex = /(?:href)=["']([^"']+\.css)["']/gi;
  while ((match = cssRegex.exec(html)) !== null) {
    assets.add(match[1]);
  }

  // Fonts
  const fontRegex = /(?:href)=["']([^"']+\.woff2?)["']/gi;
  while ((match = fontRegex.exec(html)) !== null) {
    assets.add(match[1]);
  }

  // Download all assets
  const downloads = [];
  for (const asset of assets) {
    if (asset.startsWith('http')) continue; // Skip external URLs

    const outputPath = path.join(outputDir, asset);
    downloads.push(downloadFile(asset, outputPath));
  }

  try {
    await Promise.all(downloads);
    console.log('\n✓ All assets downloaded successfully!');
  } catch (error) {
    console.error('Error downloading assets:', error);
  }
}

downloadAssets();
