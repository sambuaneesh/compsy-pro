# Compile Checklist

The PDF currently present in this directory may be stale. Rebuild from source before submission.

Run from `reports/workshop_paper/`:

```bash
pdflatex -interaction=nonstopmode css_logisymb_2026_regular.tex
bibtex css_logisymb_2026_regular
pdflatex -interaction=nonstopmode css_logisymb_2026_regular.tex
pdflatex -interaction=nonstopmode css_logisymb_2026_regular.tex
```

Then check:

```bash
grep -E "Warning|Overfull|Underfull|undefined|Citation|Reference|LaTeX Error|Emergency" css_logisymb_2026_regular.log
pdffonts css_logisymb_2026_regular.pdf
```

Expected:
- no unresolved citations;
- no unresolved references;
- no severe overfull boxes;
- no Type 3 fonts in the final PDF.
