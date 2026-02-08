# Documentation Hosting Guide

This guide covers three options for hosting your Nautobot IGP Models documentation. All options are **completely free**.

---

## ⭐ Option 1: ReadTheDocs (RECOMMENDED)

**Best for**: Professional Python packages, automatic builds, search functionality, multiple versions

**Your docs URL will be**: `https://nautobot-igp-models.readthedocs.io/`

### Why ReadTheDocs?
- ✅ Free forever for open-source projects
- ✅ Automatic builds on every push to GitHub
- ✅ Professional appearance
- ✅ Built-in search functionality
- ✅ Version support (docs for v0.1.0, v0.2.0, etc.)
- ✅ SSL/HTTPS included
- ✅ No need to be an "official" Nautobot app

### Setup Steps (5 minutes)

1. **Sign up for ReadTheDocs**
   - Go to https://readthedocs.org/
   - Click "Sign Up" → "Sign in with GitHub"
   - Authorize ReadTheDocs to access your public repositories

2. **Import Your Project**
   - Click "Import a Project" button
   - Click "Import Manually"
   - Fill in the form:
     ```
     Name: nautobot-igp-models
     Repository URL: https://github.com/byrn-baker/nautobot-app-igp-models
     Repository type: Git
     Default branch: main
     ```
   - Click "Next"

3. **Verify Build Settings** (should auto-detect)
   - ReadTheDocs will find your `.readthedocs.yaml` file
   - It will use MkDocs as the documentation builder
   - Click "Build version" to trigger first build

4. **Wait for Build** (2-5 minutes)
   - Go to "Builds" tab to watch progress
   - First build takes a bit longer

5. **Update pyproject.toml**
   Change line 10 from:
   ```toml
   documentation = "https://docs.nautobot.com/projects/nautobot-igp-models/en/latest/"
   ```

   To:
   ```toml
   documentation = "https://nautobot-igp-models.readthedocs.io/en/latest/"
   ```

6. **Update README.md badges**
   Change line 7 from:
   ```markdown
   <a href="https://docs.nautobot.com/projects/nautobot-igp-models/en/latest/"><img src="https://readthedocs.org/projects/nautobot-app-nautobot-igp-models/badge/"></a>
   ```

   To:
   ```markdown
   <a href="https://nautobot-igp-models.readthedocs.io/"><img src="https://readthedocs.org/projects/nautobot-igp-models/badge/"></a>
   ```

### Managing Versions

Once you tag releases (v0.1.0, v0.2.0, etc.), ReadTheDocs will automatically build docs for each version:
- `https://nautobot-igp-models.readthedocs.io/en/latest/` - Latest development
- `https://nautobot-igp-models.readthedocs.io/en/stable/` - Latest release
- `https://nautobot-igp-models.readthedocs.io/en/v0.1.0/` - Specific version

---

## 🎯 Option 2: GitHub Pages

**Best for**: Simple setup, docs hosted directly on GitHub

**Your docs URL will be**: `https://byrn-baker.github.io/nautobot-app-igp-models/`

### Setup Steps

1. **Enable GitHub Pages**
   - Go to https://github.com/byrn-baker/nautobot-app-igp-models/settings/pages
   - Under "Source", select "Deploy from a branch"
   - Select branch: `gh-pages`
   - Select folder: `/ (root)`
   - Click "Save"

2. **Build and Deploy Docs**
   ```bash
   # Install mkdocs if not already installed
   poetry install --with dev

   # Build and deploy to gh-pages branch
   poetry run mkdocs gh-deploy --force
   ```

3. **Wait 2-3 minutes** for GitHub to deploy

4. **Update pyproject.toml** (line 10):
   ```toml
   documentation = "https://byrn-baker.github.io/nautobot-app-igp-models/"
   ```

5. **Update README.md**
   - Remove the ReadTheDocs badge (line 7)
   - Or replace with a GitHub Pages badge:
     ```markdown
     <a href="https://byrn-baker.github.io/nautobot-app-igp-models/"><img src="https://img.shields.io/badge/docs-GitHub%20Pages-blue"></a>
     ```

### Updating Docs

Every time you update documentation, run:
```bash
poetry run mkdocs gh-deploy --force
```

**Note**: This is manual - not automatic like ReadTheDocs.

---

## 🎯 Option 3: Link to GitHub Repo

**Best for**: Quick start, minimal setup, users comfortable with GitHub

**Your docs URL will be**: `https://github.com/byrn-baker/nautobot-app-igp-models`

### Setup Steps

1. **Update pyproject.toml** (line 10):
   ```toml
   documentation = "https://github.com/byrn-baker/nautobot-app-igp-models#readme"
   ```

   Or link directly to the docs folder:
   ```toml
   documentation = "https://github.com/byrn-baker/nautobot-app-igp-models/tree/main/docs"
   ```

2. **Update README.md badges**
   Remove the docs badge entirely, or replace with:
   ```markdown
   <a href="https://github.com/byrn-baker/nautobot-app-igp-models/tree/main/docs"><img src="https://img.shields.io/badge/docs-GitHub-blue"></a>
   ```

**Pros**:
- ✅ Zero setup required
- ✅ Always up-to-date with your repo

**Cons**:
- ❌ Less professional appearance
- ❌ No search functionality
- ❌ No built-in versioning
- ❌ Markdown files shown raw (not rendered HTML)

---

## 📊 Comparison

| Feature | ReadTheDocs | GitHub Pages | GitHub Repo |
|---------|-------------|--------------|-------------|
| Cost | Free | Free | Free |
| Auto-builds | ✅ Yes | ❌ Manual | ✅ Yes |
| Professional | ✅ Yes | ✅ Yes | ⚠️  Basic |
| Search | ✅ Yes | ❌ No | ⚠️  GitHub search |
| Versions | ✅ Yes | ❌ No | ⚠️  Via branches |
| Setup time | 5 min | 10 min | 1 min |
| SSL/HTTPS | ✅ Yes | ✅ Yes | ✅ Yes |

---

## 🎯 Recommendation

**For a professional Python package going to PyPI**: Use **ReadTheDocs (Option 1)**

It's the industry standard for Python packages and provides:
- Professional appearance
- Automatic builds
- Version support
- Search functionality
- Zero maintenance

Most PyPI packages (including all official Nautobot apps) use ReadTheDocs because it's the best option.

---

## 🔧 Quick Start Commands

### After choosing ReadTheDocs:
```bash
# 1. Update pyproject.toml
sed -i 's|https://docs.nautobot.com/projects/nautobot-igp-models/en/latest/|https://nautobot-igp-models.readthedocs.io/en/latest/|' pyproject.toml

# 2. Commit and push
git add pyproject.toml README.md
git commit -m "Update documentation URLs for ReadTheDocs"
git push origin main
```

### After choosing GitHub Pages:
```bash
# 1. Deploy docs
poetry run mkdocs gh-deploy --force

# 2. Update pyproject.toml
sed -i 's|https://docs.nautobot.com/projects/nautobot-igp-models/en/latest/|https://byrn-baker.github.io/nautobot-app-igp-models/|' pyproject.toml

# 3. Commit and push
git add pyproject.toml README.md
git commit -m "Update documentation URLs for GitHub Pages"
git push origin main
```

---

## ❓ FAQs

**Q: Do I need to be an official Nautobot app to use ReadTheDocs?**
A: No! ReadTheDocs is free for any open-source project. You just need a public GitHub repo.

**Q: Will PyPI link to my docs automatically?**
A: Yes! PyPI reads the `documentation` field in pyproject.toml and creates a "Documentation" link on your package page.

**Q: Can I change hosting providers later?**
A: Yes, easily! Just update the URL in pyproject.toml and republish to PyPI.

**Q: What if I don't have docs yet?**
A: You already have excellent docs in the `docs/` folder! MkDocs will build them into a beautiful website.
