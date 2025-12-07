#!/bin/bash
# CRITICAL SECURITY CLEANUP - Remove exposed API key from all files and Git history

set -e

EXPOSED_KEY="<GOOGLE_API_KEY_REDACTED>"
REPLACEMENT="<GOOGLE_API_KEY_REDACTED>"

echo "🚨 CRITICAL SECURITY CLEANUP"
echo "================================"
echo "Removing exposed API key from:"
echo "1. Working directory files"
echo "2. Git history"
echo ""

# Step 1: Remove from current files
echo "Step 1: Cleaning working directory..."
FILES_WITH_KEY=$(grep -rl "$EXPOSED_KEY" --include="*.py" --include="*.md" --include="*.txt" --include="*.sh" --include="*.json" --include="*.yaml" . 2>/dev/null || true)

if [ -n "$FILES_WITH_KEY" ]; then
    echo "Found API key in files:"
    echo "$FILES_WITH_KEY"
    echo ""

    # Replace API key in each file
    while IFS= read -r file; do
        if [ -f "$file" ]; then
            echo "  Cleaning: $file"
            # Use sed with backup
            sed -i.bak "s/$EXPOSED_KEY/$REPLACEMENT/g" "$file"
            rm "${file}.bak"
        fi
    done <<< "$FILES_WITH_KEY"

    echo "✅ Working directory cleaned"
else
    echo "✅ No files with API key found in working directory"
fi

echo ""
echo "Step 2: Cleaning Git history..."
echo "⚠️  This will rewrite Git history!"
echo ""

# Check if git-filter-repo is installed
if ! command -v git-filter-repo &> /dev/null; then
    echo "❌ git-filter-repo not found. Installing..."
    pip3 install git-filter-repo
fi

# Step 2: Remove from Git history using git-filter-repo
echo "Running git-filter-repo to remove API key from history..."
git filter-repo --force --invert-paths --path-match "$EXPOSED_KEY" --replace-text <(echo "$EXPOSED_KEY==>$REPLACEMENT")

echo ""
echo "✅ Git history cleaned"
echo ""
echo "Step 3: Verification..."

# Verify API key is gone
if grep -r "$EXPOSED_KEY" . 2>/dev/null; then
    echo "❌ API key still found!"
    exit 1
else
    echo "✅ API key removed from all files"
fi

if git log --all --source --full-history -S "$EXPOSED_KEY" | grep -q "$EXPOSED_KEY"; then
    echo "❌ API key still in Git history!"
    exit 1
else
    echo "✅ API key removed from Git history"
fi

echo ""
echo "================================"
echo "✅ CLEANUP COMPLETE"
echo ""
echo "Next steps:"
echo "1. ⚠️  REVOKE THE EXPOSED API KEY at Google Cloud Console NOW"
echo "2. Force push to GitHub: git push --force origin master"
echo "3. Generate new API key at Google Cloud Console"
echo "4. Add to .env file (NOT to Git)"
echo "5. Verify .gitignore includes .env"
echo ""
echo "🚨 CRITICAL: Revoke the exposed key BEFORE pushing!"
