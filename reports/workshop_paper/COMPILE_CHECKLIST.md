# Compile Checklist

Rebuild from source before submission. Generated PDF/log/aux files are intentionally not treated as source artifacts.

Run from `reports/workshop_paper/`:

```bash
rm -f css_logisymb_2026_regular.{aux,bbl,blg,log,out,pdf}
pdflatex -interaction=nonstopmode css_logisymb_2026_regular.tex
pdflatex -interaction=nonstopmode css_logisymb_2026_regular.tex
```

The bibliography is embedded directly in the TeX source, so BibTeX is not required for this draft. The second `pdflatex` pass resolves citations and cross-references.

The prose avoids `Figure~\ref{...}` and `Table~\ref{...}` references, so figure/table numbering should not show `??` even if a first pass is inspected. Citations still require the second pass, as usual in LaTeX.

If `latexmk` is available, this is also acceptable:

```bash
rm -f css_logisymb_2026_regular.{aux,bbl,blg,log,out,pdf}
latexmk -pdf -interaction=nonstopmode css_logisymb_2026_regular.tex
```

Then check:

```bash
grep -E "Warning|Overfull|Underfull|undefined|Citation|Reference|LaTeX Error|Emergency" css_logisymb_2026_regular.log
pdffonts css_logisymb_2026_regular.pdf
```

Expected:
- no unresolved citations;
- no unresolved references or citations;
- no severe overfull boxes;
- no Type 3 fonts in the final PDF.

If the submission system explicitly requires line numbers, uncomment `\linenumbers` near the top of the TeX file and re-check the rendered PDF. The clean draft keeps line numbers disabled because they overlapped with two-column text in the tested build.
