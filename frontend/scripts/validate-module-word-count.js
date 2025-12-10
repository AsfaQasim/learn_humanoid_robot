#!/usr/bin/env node

// validate-module-word-count.js
// Validates that the Module 1 content meets the required word count (6,000-7,500 words)

const fs = require('fs');
const path = require('path');

// Function to count words in a string
function countWords(text) {
  // Remove markdown formatting and count words
  const cleanText = text
    .replace(/[#*`_\[\]]/g, '') // Remove common markdown formatting
    .replace(/\[.*?\]\(.*?\)/g, '') // Remove links [text](url)
    .replace(/!\[.*?\]\(.*?\)/g, '') // Remove image tags
    .replace(/\n\s*\n/g, ' ') // Replace multiple newlines with space
    .replace(/\s+/g, ' ') // Replace multiple spaces with single space
    .trim();

  return cleanText.split(/\s+/).filter(word => word.length > 0).length;
}

// Function to read all markdown files in a directory recursively
function readMarkdownFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir);

  for (const file of files) {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);

    if (stat.isDirectory()) {
      readMarkdownFiles(filePath, fileList);
    } else if (path.extname(file) === '.md' || path.extname(file) === '.mdx') {
      fileList.push(filePath);
    }
  }

  return fileList;
}

// Get all markdown files in the Module 1 directory
const moduleDirPath = path.join(__dirname, '../docs/1-robotics-module-one');
const markdownFiles = readMarkdownFiles(moduleDirPath);

let totalWordCount = 0;
const fileWordCounts = [];

console.log('Module 1 Word Count Validation\n');
console.log('File-by-file breakdown:\n');

for (const file of markdownFiles) {
  const content = fs.readFileSync(file, 'utf8');
  const wordCount = countWords(content);
  totalWordCount += wordCount;
  
  // Get relative path for cleaner output
  const relativePath = path.relative(path.join(__dirname, '../docs'), file);
  fileWordCounts.push({ file: relativePath, count: wordCount });
  
  console.log(`${relativePath}: ${wordCount} words`);
}

console.log(`\nTotal Module 1 word count: ${totalWordCount}`);
console.log('Required word count: 6,000-7,500 words');

// Define the required word count range
const MIN_WORDS = 6000;
const MAX_WORDS = 7500;

if (totalWordCount >= MIN_WORDS && totalWordCount <= MAX_WORDS) {
  console.log(`✅ SUCCESS: Word count is within the required range (${MIN_WORDS}-${MAX_WORDS})`);
  process.exit(0);
} else {
  console.log(`❌ FAILURE: Word count is OUTSIDE the required range (${MIN_WORDS}-${MAX_WORDS})`);
  
  if (totalWordCount < MIN_WORDS) {
    console.log(`⚠️  Module is ${MIN_WORDS - totalWordCount} words SHORT of minimum requirement`);
  } else {
    console.log(`⚠️  Module is ${totalWordCount - MAX_WORDS} words OVER the maximum requirement`);
  }
  
  // Exit with error code
  process.exit(1);
}