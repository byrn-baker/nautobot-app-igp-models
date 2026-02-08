# Release Checklist

Quick checklist for releasing a new version of `nautobot-igp-models` to PyPI.

---

## Pre-Release Checklist

### Code Quality
- [ ] All tests pass: `invoke unittest`
- [ ] Linting passes: `invoke ruff`
- [ ] No critical security vulnerabilities
- [ ] Documentation is up to date
- [ ] CHANGELOG/release notes updated

### Version Management
- [ ] Decide version bump (patch/minor/major)
- [ ] Update version: `poetry version [patch|minor|major]`
- [ ] Review version in `pyproject.toml`

### Repository
- [ ] All changes committed
- [ ] Push to GitHub: `git push origin develop`
- [ ] Pull request merged (if using PR workflow)

---

## Testing Release (Recommended First Time)

### Test on TestPyPI

```bash
# 1. Build
poetry build

# 2. Publish to TestPyPI
poetry publish -r testpypi

# 3. Test installation
python -m venv test-env
source test-env/bin/activate
pip install --index-url https://test.pypi.org/simple/ \
            --extra-index-url https://pypi.org/simple/ \
            nautobot-igp-models

# 4. Verify
python -c "import nautobot_igp_models; print(nautobot_igp_models.__version__)"
```

- [ ] Package installs successfully
- [ ] Import works
- [ ] TestPyPI page looks correct: https://test.pypi.org/project/nautobot-igp-models/

---

## Production Release

### Build and Publish

```bash
# Clean previous builds
rm -rf dist/

# Build fresh
poetry build

# Publish to PyPI
poetry publish
```

- [ ] Build successful
- [ ] Publish successful
- [ ] PyPI page updated: https://pypi.org/project/nautobot-igp-models/

### Verify Installation

```bash
python -m venv verify-env
source verify-env/bin/activate
pip install nautobot-igp-models
python -c "import nautobot_igp_models"
```

- [ ] Installs successfully from PyPI
- [ ] Import works
- [ ] Version correct

---

## Post-Release

### Git Tagging

```bash
# Create tag
git tag -a v$(poetry version -s) -m "Release version $(poetry version -s)"

# Push tag
git push origin v$(poetry version -s)
```

- [ ] Tag created
- [ ] Tag pushed to GitHub

### GitHub Release

1. Go to https://github.com/byrn-baker/nautobot-app-igp-models/releases
2. Click "Draft a new release"
3. Select tag `v0.1.0` (or your version)
4. Title: `v0.1.0 - [Brief Description]`
5. Description: Copy from CHANGELOG
6. Publish release

- [ ] GitHub release created
- [ ] Release notes complete

### Documentation Updates

- [ ] README.md includes PyPI installation instructions
- [ ] Documentation site updated (if applicable)
- [ ] CHANGELOG.md updated for next version

---

## Announcement (Optional)

- [ ] Post to Network to Code Slack
- [ ] Social media announcement
- [ ] Nautobot community channels
- [ ] Project mailing list/Discord

---

## Next Development Cycle

```bash
# Optionally bump to next dev version
poetry version prepatch  # e.g., 0.1.0 → 0.1.1a0

# Start new CHANGELOG section
# Edit CHANGELOG.md to add:
# ## [Unreleased]
# ### Added
# ### Changed
# ### Fixed
```

- [ ] Version bumped to dev version (optional)
- [ ] CHANGELOG ready for next release notes

---

## Quick Commands Reference

```bash
# Check version
poetry version

# Bump version
poetry version [patch|minor|major|prepatch|preminor|premajor]

# Build
poetry build

# Publish to TestPyPI
poetry publish -r testpypi

# Publish to PyPI
poetry publish

# Create tag
git tag -a v$(poetry version -s) -m "Release $(poetry version -s)"

# Push tag
git push origin v$(poetry version -s)

# View package contents
tar -tzf dist/nautobot-igp-models-*.tar.gz | less
```

---

## First Time Setup (One-Time)

Only needed once per machine:

```bash
# Set PyPI token
poetry config pypi-token.pypi pypi-AgEIcH...yourtoken...

# Set TestPyPI (optional)
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi pypi-AgEIcH...yourtoken...
```

---

## Troubleshooting

**Build fails:**
- Check `pyproject.toml` syntax
- Ensure all required files exist
- Review `poetry check` output

**Publish fails (already exists):**
- Cannot overwrite existing version
- Increment version and republish

**Import fails after install:**
- Check package name vs import name
- Verify dependencies installed
- Check Python version compatibility

**TestPyPI installation fails:**
- Use both indexes (TestPyPI + PyPI)
- Some dependencies may not exist on TestPyPI

---

*See [PYPI_PUBLISHING_GUIDE.md](PYPI_PUBLISHING_GUIDE.md) for detailed instructions*
