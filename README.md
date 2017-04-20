# Curriculum Vitæ

Don't think this project really needs any kind of explaination.

Just to let you know: as I want to keep track even of my older _curricula_, project's root will separate any of them for year.

## Download latest version

In order to easily get latest version, you can batch download it this way:

```bash
# IT version
wget $(curl -I https://github.com/streambinder/curriculum-vitae/releases/latest | \
    grep ^Location\: | cut -d' ' -f2 | tr -cd "[:print:]" | \
    sed 's/\/tag\//\/download\//g')/it.pdf

# EN version
wget $(curl -I https://github.com/streambinder/curriculum-vitae/releases/latest | \
    grep ^Location\: | cut -d' ' -f2 | tr -cd "[:print:]" | \
    sed 's/\/tag\//\/download\//g')/en.pdf
```
