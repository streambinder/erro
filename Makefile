YEAR := $(shell find -maxdepth 1 -type d -printf '%f\n' | egrep -e '[0-9]{4}' | sort -ru | head -1)
LANGUAGES := $(shell jq -r 'first(.[] | keys | @csv)' < $(YEAR)/keys.json | sed 's/,/ /g' | xargs)

all:
	@ ( \
		mkdir -p bin; \
		cd $(YEAR); \
		for tex_variant in *.tex; do \
			tex_basename="$$(sed 's/.tex//g' <<< "$${tex_variant}")"; \
			for lang in $(LANGUAGES); do \
				echo "Building $$tex_variant in for $$lang language..."; \
				while read -r var; do \
					key="$$(awk -F'=' '{print $$1}' <<< "$${var}")"; \
					value="$$(cut -d"=" -f2- <<< "$${var}")"; \
					value_cmd="$$(awk '{print $$1}' <<< "$${value}")"; \
					if (which "$${value_cmd}" && eval "$${value}") > /dev/null 2>&1; then \
						export $$key="$$(eval $$value)"; \
					else \
						export $$key="$$value"; \
					fi; \
				done <<< "$$(jq -r --arg lang "$$lang" -r 'to_entries[] | "\(.key)=\(.value[$$lang])"' < keys.json)"; \
				tex_lang_variant="$${tex_basename}.$${lang}.tex"; \
				mush < "$${tex_variant}" > "$${tex_lang_variant}" && \
				pdflatex -synctex=1 -interaction=nonstopmode -output-directory=../bin "$${tex_lang_variant}" 2>&1 > /dev/null && \
				rm -f "$${tex_lang_variant}"; \
			done; \
		done; \
		cd ../bin && find -maxdepth 1 -type f ! -name \*.pdf -delete; \
	);

clean:
	@ ( \
		find -type f \( -name \*.aux -o -name \*.log -o -name \*.out -o -name \*.pdf -o -name \*.synctex.gz -o -name \*.toc \) -delete -print; \
		for lang in $(LANGUAGES); do \
			find -type f -name \*.$$lang.tex -delete -print; \
		done; \
		rm -rfv bin; \
	);
