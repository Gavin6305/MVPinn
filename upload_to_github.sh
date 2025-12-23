#!/bin/bash
# Quick script to upload PINN4ME to GitHub

echo "=== PINN4ME GitHub Upload Script ==="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
else
    echo "Git repository already initialized."
fi

# Check current status
echo ""
echo "Current git status:"
git status --short

# Ask for confirmation
echo ""
read -p "Do you want to proceed with adding and committing all files? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

# Add all files
echo "Adding all files..."
git add .

# Commit
echo ""
read -p "Enter commit message (or press Enter for default): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Initial commit: PINN4ME - Physics-Informed Neural Network for Milne-Eddington Inversion"
fi

echo "Committing with message: $commit_msg"
git commit -m "$commit_msg"

# Check if remote exists
if git remote | grep -q "^origin$"; then
    echo ""
    echo "Remote 'origin' already exists."
    read -p "Do you want to update it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter GitHub repository URL: " repo_url
        git remote set-url origin "$repo_url"
    fi
else
    echo ""
    read -p "Enter GitHub repository URL (e.g., https://github.com/USERNAME/PINN4ME.git): " repo_url
    git remote add origin "$repo_url"
fi

# Set branch to main
git branch -M main

# Push
echo ""
echo "Pushing to GitHub..."
echo "You may be prompted for credentials."
git push -u origin main

echo ""
echo "Done! Check your GitHub repository to verify the upload."
