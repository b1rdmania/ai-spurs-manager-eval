# Regenerating PDF Reports

To convert markdown reports to PDF using Pandoc:

```bash
# Single report
pandoc frank.md -o frank.pdf --pdf-engine=wkhtmltopdf

# All reports
for file in *.md; do
    pandoc "$file" -o "${file%.md}.pdf" --pdf-engine=wkhtmltopdf
done
```

## Requirements
- pandoc
- wkhtmltopdf

## Install on macOS
```bash
brew install pandoc wkhtmltopdf
```

## Install on Ubuntu
```bash
sudo apt-get install pandoc wkhtmltopdf
```
