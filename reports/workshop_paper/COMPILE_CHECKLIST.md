# Compile Checklist

The PDF currently present in this directory may be stale. Rebuild from source before submission.

Run from `reports/workshop_paper/`:

```bash
rm -f css_logisymb_2026_regular.{aux,bbl,blg,log,out,pdf}
pdflatex -interaction=nonstopmode css_logisymb_2026_regular.tex
bibtex css_logisymb_2026_regular
pdflatex -interaction=nonstopmode css_logisymb_2026_regular.tex
pdflatex -interaction=nonstopmode css_logisymb_2026_regular.tex
```

If `latexmk` is available, this is also acceptable:

```bash
rm -f css_logisymb_2026_regular.{aux,bbl,blg,log,out,pdf}
latexmk -pdf -interaction=nonstopmode css_logisymb_2026_regular.tex
```

Then check:

```bash
grep -E "Warning|Overfull|Underfull|undefined|Citation|Reference|LaTeX Error|Emergency" css_logisymb_2026_regular.log
test -s css_logisymb_2026_regular.bbl
test -s css_logisymb_2026_regular.blg
pdffonts css_logisymb_2026_regular.pdf
```

Expected:
- no unresolved citations;
- no unresolved references;
- no severe overfull boxes;
- no Type 3 fonts in the final PDF.
