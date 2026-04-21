# How to Upload Files to GitHub (Step-by-Step)

## Method 1: Upload from Terminal (Recommended)

### 1) Open terminal in your project folder
```bash
cd /path/to/JP-Enterprises-Saharsa
```

### 2) Initialize Git (only if not initialized)
```bash
git init
```

### 3) Add all files and commit
```bash
git add .
git commit -m "Initial project upload"
```

### 4) Connect your GitHub repository
Create an empty repo on GitHub first, then run:
```bash
git remote add origin https://github.com/<your-username>/<your-repo>.git
```

If `origin` already exists:
```bash
git remote set-url origin https://github.com/<your-username>/<your-repo>.git
```

### 5) Push code to GitHub
```bash
git branch -M main
git push -u origin main
```

---

## Method 2: Upload directly on GitHub website (No terminal)
1. Open your repository on GitHub.
2. Click **Add file** → **Upload files**.
3. Drag/drop your files.
4. Add a commit message.
5. Click **Commit changes**.

---

## Add new files later (after first upload)
```bash
git add <file-name>
git commit -m "Add <file-name>"
git push
```

## Update all changed files at once
```bash
git add .
git commit -m "Update website and inventory"
git push
```

## Common errors
- **Authentication failed**: Use GitHub Personal Access Token instead of password.
- **remote origin already exists**: Use `git remote set-url origin <repo-url>`.
- **rejected/non-fast-forward**: Run `git pull --rebase origin main` then `git push`.
