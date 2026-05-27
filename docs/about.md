# About

Yup. I host my LaTeX CV on a dedicated repository on GitHub and release every version of it using dedicated _Releases_.
I really enjoyed the idea to review it as a coding project, making it buildable as a common project using build automation tools and release its binary (PDF) version.

## Build it yourself

If you want to fork the project and produce your own resume, the local toolchain is:

- Python `>=3.13` and [`uv`](https://docs.astral.sh/uv/) for the templating script (`uv sync` pulls Jinja2 and PyYAML).
- `make` to drive the build (`make`, then artifacts land under `build/`).
- `pdflatex` to compile the LaTeX targets — on Debian/Ubuntu install `texlive-latex-recommended` and `texlive-fonts-extra`; HTML and plain-text targets need no LaTeX.

Source data lives under `src/langs/*.yml` and templates under `src/templates/*.{tex,html,txt}.j2`.
