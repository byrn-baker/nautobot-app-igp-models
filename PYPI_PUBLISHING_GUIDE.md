# PyPI Publishing Guide

This guide walks you through publishing the `nautobot-igp-models` package to PyPI (Python Package Index).

---

## Table of Contents

- [Pre-Publishing Checklist](#pre-publishing-checklist)
- [One-Time Setup](#one-time-setup)
- [Publishing Process](#publishing-process)
- [Testing on TestPyPI (Recommended)](#testing-on-testpypi-recommended)
- [Publishing to Production PyPI](#publishing-to-production-pypi)
- [Post-Publication](#post-publication)
- [Version Updates](#version-updates)
- [Troubleshooting](#troubleshooting)

---

## Pre-Publishing Checklist

Before publishing, ensure:

### ✅ Package Configuration

- [x] **Version number** is correct in [pyproject.toml](pyproject.toml) (currently: `0.1.0`)
- [x] **Package name** is unique: `nautobot-igp-models`
- [x] **License** is specified: `Apache-2.0`
- [x] **README.md** is complete and professional
- [x] **Authors** information is correct
- [x] **Repository URL** points to GitHub
- [x] **Python version** requirements are accurate: `>=3.10,<3.14`

### ✅ Code Quality

- [ ] All tests pass (run: `invoke unittest`)
- [ ] Linting passes (run: `invoke ruff`)
- [ ] Documentation is complete
- [ ] CHANGELOG or release notes are updated
- [ ] No security vulnerabilities (currently: 1 moderate)

### ✅ Git Repository

- [x] Latest changes are committed
- [x] Repository is pushed to GitHub
- [ ] Create a git tag for the version (recommended)

---

## One-Time Setup

### Step 1: Create PyPI Account

1. **Register on PyPI:**
   - Production: https://pypi.org/account/register/
   - Test (recommended first): https://test.pypi.org/account/register/

2. **Enable Two-Factor Authentication** (recommended for security)

3. **Create API Token:**
   - Go to Account Settings → API tokens
   - Click "Add API token"
   - Name: `nautobot-igp-models`
   - Scope: Choose "Entire account" for first upload, then you can create package-specific tokens later
   - **Save the token immediately** - you won't see it again!

### Step 2: Configure Poetry

Option A: Configure with token directly
```bash
poetry config pypi-token.pypi pypi-AgEIcH...yourtoken...
```

Option B: Store in environment variable (more secure)
```bash
# Add to your ~/.bashrc or ~/.zshrc
export POETRY_PYPI_TOKEN_PYPI=pypi-AgEIcH...yourtoken...
```

For TestPyPI:
```bash
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi pypi-AgEIcH...yourtoken...
```

---

## Publishing Process

### Standard Workflow

```bash
# 1. Ensure you're on develop branch with latest changes
git checkout develop
git pull origin develop

# 2. Update version number (if needed)
poetry version patch  # or minor, major, prepatch, preminor, premajor, prerelease

# 3. Build the package
poetry build

# 4. Publish to PyPI
poetry publish  # Production
# OR
poetry publish -r testpypi  # Test first (recommended)
```

---

## Testing on TestPyPI (Recommended)

**Always test on TestPyPI before publishing to production PyPI!**

### Step 1: Publish to TestPyPI

```bash
# Build the package
poetry build

# Publish to TestPyPI
poetry publish -r testpypi
```

### Step 2: Test Installation

Create a test environment and install from TestPyPI:

```bash
# Create test virtual environment
python -m venv test-env
source test-env/bin/activate  # On Windows: test-env\Scripts\activate

# Install from TestPyPI (with PyPI as fallback for dependencies)
pip install --index-url https://test.pypi.org/simple/ \
            --extra-index-url https://pypi.org/simple/ \
            nautobot-igp-models

# Test import
python -c "import nautobot_igp_models; print(nautobot_igp_models.__version__)"

# Verify package contents
pip show nautobot-igp-models
```

### Step 3: Verify on TestPyPI Website

Visit: https://test.pypi.org/project/nautobot-igp-models/

Check:
- ✅ README displays correctly
- ✅ Package metadata is accurate
- ✅ Installation instructions work
- ✅ Links (GitHub, docs) work correctly

---

## Publishing to Production PyPI

Once testing is successful:

### Step 1: Clean Previous Builds (if needed)

```bash
rm -rf dist/
poetry build
```

### Step 2: Publish to Production

```bash
poetry publish
```

You'll see output like:
```
Publishing nautobot-igp-models (0.1.0) to PyPI
 - Uploading nautobot_igp_models-0.1.0-py3-none-any.whl 100%
 - Uploading nautobot-igp-models-0.1.0.tar.gz 100%
```

### Step 3: Verify Publication

1. **Check PyPI page:**
   https://pypi.org/project/nautobot-igp-models/

2. **Test installation:**
   ```bash
   pip install nautobot-igp-models
   ```

3. **Verify in fresh environment:**
   ```bash
   python -m venv verify-env
   source verify-env/bin/activate
   pip install nautobot-igp-models
   python -c "import nautobot_igp_models"
   ```

---

## Post-Publication

### Create Git Tag

Tag the release in Git:

```bash
# Create annotated tag
git tag -a v0.1.0 -m "Release version 0.1.0"

# Push tag to GitHub
git push origin v0.1.0
```

### Create GitHub Release

1. Go to: https://github.com/byrn-baker/nautobot-app-igp-models/releases
2. Click "Draft a new release"
3. Choose tag: `v0.1.0`
4. Release title: `v0.1.0 - Initial Release`
5. Description: Copy from CHANGELOG or SESSION_SUMMARY.md
6. Attach build artifacts (optional): `dist/nautobot_igp_models-0.1.0.tar.gz`
7. Click "Publish release"

### Update Documentation

Add installation instructions to README.md:

```markdown
## Installation

Install from PyPI:

\`\`\`bash
pip install nautobot-igp-models
\`\`\`

For detailed installation and configuration instructions, see the [documentation](https://docs.nautobot.com/projects/nautobot-igp-models/).
```

### Announce Release (Optional)

- Post on Network to Code Slack
- Tweet/LinkedIn announcement
- Nautobot community channels
- Reddit r/nautobot

---

## Version Updates

### Semantic Versioning

Follow [Semantic Versioning](https://semver.org/):

- **Patch** (0.1.0 → 0.1.1): Bug fixes, no breaking changes
- **Minor** (0.1.0 → 0.2.0): New features, backward compatible
- **Major** (0.1.0 → 1.0.0): Breaking changes

### Updating Version

```bash
# Patch release (bug fixes)
poetry version patch  # 0.1.0 → 0.1.1

# Minor release (new features)
poetry version minor  # 0.1.0 → 0.2.0

# Major release (breaking changes)
poetry version major  # 0.1.0 → 1.0.0

# Pre-release versions
poetry version prepatch   # 0.1.0 → 0.1.1a0
poetry version preminor   # 0.1.0 → 0.2.0a0
poetry version premajor   # 0.1.0 → 1.0.0a0
poetry version prerelease # 0.1.1a0 → 0.1.1a1
```

### Release Workflow

```bash
# 1. Update version
poetry version patch

# 2. Commit version change
git add pyproject.toml
git commit -m "Bump version to $(poetry version -s)"

# 3. Create changelog entry
# Edit CHANGELOG.md or use towncrier

# 4. Build and publish
poetry build
poetry publish

# 5. Tag release
git tag -a "v$(poetry version -s)" -m "Release $(poetry version -s)"
git push origin "v$(poetry version -s)"

# 6. Create GitHub release
# Use GitHub web interface
```

---

## Troubleshooting

### Issue: "File already exists"

**Problem:** Trying to upload a version that already exists on PyPI.

**Solution:** You cannot overwrite a published version. Increment the version:
```bash
poetry version patch
poetry build
poetry publish
```

### Issue: "Invalid token"

**Problem:** Authentication failed.

**Solutions:**
1. Verify token is correct:
   ```bash
   poetry config --list | grep pypi-token
   ```

2. Regenerate token on PyPI and reconfigure:
   ```bash
   poetry config pypi-token.pypi pypi-AgEIcH...newtoken...
   ```

### Issue: "Package name already taken"

**Problem:** Package name `nautobot-igp-models` is already registered.

**Solution:** Choose a different name:
```toml
# In pyproject.toml
name = "nautobot-igp-models-yourname"
```

### Issue: Dependencies fail on TestPyPI

**Problem:** TestPyPI doesn't have all dependencies.

**Solution:** Use both indexes when testing:
```bash
pip install --index-url https://test.pypi.org/simple/ \
            --extra-index-url https://pypi.org/simple/ \
            nautobot-igp-models
```

### Issue: README not rendering correctly

**Problem:** Markdown rendering issues on PyPI.

**Solutions:**
1. Ensure README.md uses standard Markdown (not GitHub-specific)
2. Test locally:
   ```bash
   pip install readme-renderer
   python -m readme_renderer README.md -o /tmp/README.html
   open /tmp/README.html
   ```

3. Avoid:
   - Complex HTML
   - GitHub-specific syntax (alerts, task lists)
   - Relative links to other repo files

### Issue: Missing files in package

**Problem:** Some files not included in distribution.

**Solution:** Update `include` in pyproject.toml:
```toml
[tool.poetry]
include = [
    "nautobot_igp_models/static/**/*",
    "nautobot_igp_models/templates/**/*",
    "nautobot_igp_models/schemas/**/*",
]
```

Verify contents:
```bash
tar -tzf dist/nautobot-igp-models-0.1.0.tar.gz | less
```

---

## Quick Reference Commands

```bash
# Check current version
poetry version

# Build package
poetry build

# Publish to TestPyPI
poetry publish -r testpypi

# Publish to PyPI
poetry publish

# Create and push tag
git tag -a v$(poetry version -s) -m "Release $(poetry version -s)"
git push origin v$(poetry version -s)

# Check what will be included in package
poetry build -f sdist
tar -tzf dist/nautobot-igp-models-*.tar.gz
```

---

## Security Best Practices

1. ✅ **Use API tokens** instead of username/password
2. ✅ **Enable 2FA** on your PyPI account
3. ✅ **Use package-specific tokens** after first upload
4. ✅ **Store tokens securely** (use environment variables, not in code)
5. ✅ **Rotate tokens** periodically
6. ✅ **Review code** before publishing (ensure no secrets in code)
7. ✅ **Sign releases** with GPG (optional but recommended)

---

## Resources

- **PyPI:** https://pypi.org/
- **TestPyPI:** https://test.pypi.org/
- **Poetry Publishing Docs:** https://python-poetry.org/docs/libraries/#publishing-to-pypi
- **PyPI Help:** https://pypi.org/help/
- **Packaging Guide:** https://packaging.python.org/
- **Semantic Versioning:** https://semver.org/

---

## Your Package URLs

Once published:

- **PyPI Page:** https://pypi.org/project/nautobot-igp-models/
- **Test Page:** https://test.pypi.org/project/nautobot-igp-models/
- **Install Command:** `pip install nautobot-igp-models`
- **GitHub Releases:** https://github.com/byrn-baker/nautobot-app-igp-models/releases

---

*Last Updated: February 2026*
