# Guide: Uploading PINN4ME to GitHub

This guide will walk you through uploading your repository to GitHub.

## Step 1: Initialize Git Repository

Open a terminal and navigate to the repository:

```bash
cd /project/bs644/ql47/ME/PINN4ME/scr/github_repository
```

Initialize git (if not already done):

```bash
git init
```

## Step 2: Add All Files

Add all files to git:

```bash
git add .
```

Check what will be committed:

```bash
git status
```

## Step 3: Make Initial Commit

Create your first commit:

```bash
git commit -m "Initial commit: PINN4ME - Physics-Informed Neural Network for Milne-Eddington Inversion"
```

## Step 4: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the **"+"** icon in the top right corner
3. Select **"New repository"**
4. Fill in the details:
   - **Repository name**: `PINN4ME` (or your preferred name)
   - **Description**: "Physics-Informed Neural Network for Milne-Eddington Inversion of Solar Stokes Profiles"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click **"Create repository"**

## Step 5: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/PINN4ME.git

# Rename default branch to main (if needed)
git branch -M main

# Push your code to GitHub
git push -u origin main
```

If you're using SSH instead of HTTPS:

```bash
git remote add origin git@github.com:YOUR_USERNAME/PINN4ME.git
git branch -M main
git push -u origin main
```

## Step 6: Authentication

If prompted for credentials:
- **HTTPS**: Use a Personal Access Token (not your password)
  - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
  - Generate a new token with `repo` permissions
  - Use this token as your password
- **SSH**: Make sure your SSH key is added to GitHub

## Step 7: Verify Upload

1. Go to your GitHub repository page
2. You should see all your files
3. Check that README.md displays correctly

## Optional: Update Repository Information

Before pushing, you may want to update:

1. **README.md**: Replace placeholders:
   - `[Your Name]` → Your actual name
   - `your.email@example.com` → Your email
   - `https://github.com/yourusername/PINN4ME` → Your actual repository URL

2. **setup.py**: Update author information

3. **LICENSE**: Update copyright year and name (if needed)

## Troubleshooting

### If you get "remote origin already exists":
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/PINN4ME.git
```

### If you need to update files after initial push:
```bash
git add .
git commit -m "Update: description of changes"
git push
```

### If you want to exclude certain files:
Check `.gitignore` - it should already exclude:
- Model files (`.pt`, `.pth`)
- Data files (`.fts`, `.fits`, `.npz`)
- Output images (`.png`, `.jpg`)
- Python cache (`__pycache__/`)

## Next Steps After Upload

1. Add a repository description on GitHub
2. Add topics/tags (e.g., `machine-learning`, `solar-physics`, `pytorch`, `pinn`)
3. Consider adding:
   - GitHub Actions badges to README
   - Citation information
   - Additional documentation
4. Create releases for version tags

## Quick Reference Commands

```bash
# Navigate to repository
cd /project/bs644/ql47/ME/PINN4ME/scr/github_repository

# Initialize (first time only)
git init
git add .
git commit -m "Initial commit"

# Connect to GitHub (first time only)
git remote add origin https://github.com/YOUR_USERNAME/PINN4ME.git
git branch -M main
git push -u origin main

# Future updates
git add .
git commit -m "Description of changes"
git push
```

