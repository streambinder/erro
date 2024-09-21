#!/bin/bash

set -euo pipefail

cd "${BUILD_DIR}"

mv -f templates/*{html,txt} ./

for template_tex in templates/*.tex; do
	pdflatex -synctex=1 -interaction=nonstopmode "${template_tex}"
done

find . -maxdepth 1 -type f -not -name '*.pdf' -a -not -name '*.html' -a -not -name '*.txt' -delete
