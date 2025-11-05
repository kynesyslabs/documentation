# GitHub Action Workflow Templates

This directory contains workflow templates that need to be manually added to `.github/workflows/` directory.

## update-summary.yml.template

This workflow automatically updates `SUMMARY.md` when markdown files are pushed.

### Installation

1. Copy the template to the workflows directory:
   ```bash
   cp .github/workflow-templates/update-summary.yml.template .github/workflows/update-summary.yml
   ```

2. Commit and push:
   ```bash
   git add .github/workflows/update-summary.yml
   git commit -m "chore: enable SUMMARY.md auto-update workflow"
   git push
   ```

### How it works

- Triggers on push to main/master when any `.md` files change (except SUMMARY.md)
- Can also be triggered manually from GitHub Actions tab
- Runs the Python script to detect missing files
- Automatically commits and pushes updates to SUMMARY.md if needed
- Uses `[skip ci]` to prevent infinite loops

### Manual Testing

You can test the script locally anytime:
```bash
python3 .github/scripts/generate_summary.py
```
