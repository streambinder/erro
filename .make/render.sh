#!/bin/bash

cd ${BUILD_DIR}

mv -f templates/*html ./

for template_tex in templates/*.tex; do
    pdflatex -synctex=1 -interaction=nonstopmode \
        ${template_tex} > /dev/null 2>&1
done

find . -maxdepth 1 -type f -not -name '*.pdf' -a -not -name '*.html' -delete
