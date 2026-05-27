# Download

To download latest version, please, reach latest [GitHub repository](https://github.com/streambinder/erro) release.
Otherwise, if you want to grab it from the shell (or in any other way you prefer), you can use (or adapt) the following snippet:

```bash
lang="en"          # supported: en, it
variant="europass" # supported: europass, personal
release="https://github.com/streambinder/erro/releases/latest"
curl "${release}/download/${variant}_${lang}.pdf" -o resume.pdf
```

The same release also publishes non-PDF variants generated from the very same data source:

- `web_{en,it}.html` — single-page HTML rendition, designed to be iframed on a personal page.
- `plain_{en,it}.txt` — plain-text rendition, handy for diffing or piping into other tools.

New releases are tagged `YYYY-MM-DD` (UTC). A same-day re-push rolls the tag forward in place rather than minting a new one, so `latest` always points at the freshest build of the day.
