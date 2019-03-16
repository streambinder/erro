YEAR := $(shell find -maxdepth 1 -type d -printf '%f\n' | egrep -e '[0-9]{4}' | sort -ru | head -1)


all:
	@ ( \
		mkdir -p bin; \
		cd $(YEAR); \
		for texfile in *.tex; do \
			pdflatex -synctex=1 -interaction=nonstopmode -output-directory=../bin "$$texfile"; \
		done; \
	);

clean:
	@ ( \
		find -type f \( -name \*.aux -o -name \*.log -o -name \*.out -o -name \*.pdf -o -name \*.synctex.gz -o -name \*.toc \) -delete -print; \
		rm -rfv bin; \
	);
