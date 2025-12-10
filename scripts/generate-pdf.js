#!/usr/bin/env node

// generate-pdf.js
// Script to generate PDF from built Docusaurus site using Puppeteer

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function generatePDF() {
  // Check if build directory exists
  const buildDir = path.join(__dirname, 'build');
  if (!fs.existsSync(buildDir)) {
    console.error('Build directory does not exist. Run "npm run build" first.');
    process.exit(1);
  }

  // Launch Puppeteer browser
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  try {
    // Set the path to the built site
    const sitePath = `file://${buildDir}/docs/1-robotics-module-one/index.html`;
    
    console.log('Generating PDF for Module 1...');
    
    await page.goto(sitePath, { waitUntil: 'networkidle2' });
    
    // Create output directory if it doesn't exist
    const outputDir = path.join(__dirname, 'output');
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir);
    }
    
    // Generate PDF
    await page.pdf({
      path: path.join(outputDir, 'robotics-module-1.pdf'),
      format: 'A4',
      printBackground: true,
      margin: {
        top: '20px',
        bottom: '40px',
        left: '20px',
        right: '20px'
      }
    });

    console.log('PDF generated successfully: output/robotics-module-1.pdf');
    
  } catch (error) {
    console.error('Error generating PDF:', error);
  } finally {
    await browser.close();
  }
}

// Install puppeteer if not already installed
const puppeteerPath = path.join(__dirname, 'node_modules', 'puppeteer');
if (!fs.existsSync(puppeteerPath)) {
  console.log('Installing Puppeteer...');
  const { execSync } = require('child_process');
  execSync('npm install puppeteer', { cwd: __dirname, stdio: 'inherit' });
}

generatePDF().catch(console.error);