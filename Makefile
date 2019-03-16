YEAR := $(shell find -maxdepth 1 -type d -printf '%f\n' | egrep -e '[0-9]{4}' | sort -ru | head -1)


all:
	@ ( \
		mkdir -p bin; \
		cd bin; \
		for texfile in ../$(YEAR)/*.tex; do \
			pdflatex -synctex=1 -interaction=nonstopmode "$$texfile"; \
		done; \
	);

clean:
	@rm -rf bin
