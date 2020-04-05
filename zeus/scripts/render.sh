#!/bin/bash

cd ${build_dir}/templates
for template in *.tex; do
    pdflatex -synctex=1 -interaction=nonstopmode -output-directory=../ ${template} > /dev/null 2>&1
    find .. -maxdepth 1 -type f -not -name '*.pdf' -delete
done