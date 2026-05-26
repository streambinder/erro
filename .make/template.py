#!/usr/bin/env python3

from __future__ import annotations

import glob
import os
import re
from typing import Any

import jinja2
import yaml

# matches *word* — used in YAML to mark emphasis without committing to a target syntax
EMPH_PATTERN = re.compile(r"\*([^*\s][^*]*[^*\s]|[^*\s])\*")
# matches [text](url) — markdown-style links; text may itself contain *emph*
LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


def latex_escape(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    # markdown markers must be extracted before escape; the generated \emph{}/\href{}{}
    # would otherwise have their braces/backslash escaped into literals
    link_placeholder = "\x00LINK\x00"
    emph_placeholder = "\x00EMPH\x00"
    links: list[tuple[str, str]] = []
    emphs: list[str] = []

    def stash_link(match: re.Match[str]) -> str:
        links.append((match.group(1), match.group(2)))
        return link_placeholder

    def stash_emph(match: re.Match[str]) -> str:
        emphs.append(match.group(1))
        return emph_placeholder

    value = LINK_PATTERN.sub(stash_link, value)
    value = EMPH_PATTERN.sub(stash_emph, value)

    # order matters: backslash first, then chars that map to commands
    replacements = [
        ("\\", r"\textbackslash{}"),
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("~", r"\textasciitilde{}"),
        ("^", r"\textasciicircum{}"),
    ]
    for src, dst in replacements:
        value = value.replace(src, dst)

    for content in emphs:
        # emph content was already escaped via the placeholder roundtrip — recover the original
        # then re-escape so nested markdown is preserved literally. simpler: re-run the same
        # pipeline recursively on the captured text (no link/emph inside emph supported here)
        value = value.replace(emph_placeholder, rf"\emph{{{_latex_escape_plain(content)}}}", 1)
    for text, url in links:
        # url goes raw inside \href (hyperref handles its own escaping for URLs);
        # text is escaped, with nested *emph* recursively resolved
        value = value.replace(link_placeholder, rf"\href{{{url}}}{{{latex_escape(text)}}}", 1)
    return value


def _latex_escape_plain(value: str) -> str:
    # escape pass without markdown handling; used inside already-stashed contexts
    replacements = [
        ("\\", r"\textbackslash{}"),
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("~", r"\textasciitilde{}"),
        ("^", r"\textasciicircum{}"),
    ]
    for src, dst in replacements:
        value = value.replace(src, dst)
    return value


def html_emph(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    # links first so nested *emph* inside link text gets handled by the emph pass after
    value = LINK_PATTERN.sub(r'<a href="\2">\1</a>', value)
    return EMPH_PATTERN.sub(r"<em>\1</em>", value)


def txt_emph(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    value = LINK_PATTERN.sub(r"\1 (\2)", value)
    return EMPH_PATTERN.sub(r"\1", value)


j_envs = {
    "html": jinja2.Environment(
        block_start_string="<jblock",
        block_end_string="/>",
        variable_start_string="<jvar",
        variable_end_string="/>",
        comment_start_string="<!--",
        comment_end_string="-->",
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(os.path.abspath(".")),
    ),
    "tex": jinja2.Environment(
        block_start_string="\\jblock{",
        block_end_string="}",
        variable_start_string="\\jvar{",
        variable_end_string="}",
        comment_start_string="\\#{",
        comment_end_string="}",
        line_statement_prefix="%%",
        line_comment_prefix="%#",
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(os.path.abspath(".")),
    ),
    "txt": jinja2.Environment(
        block_start_string="{%",
        block_end_string="%}",
        variable_start_string="{{",
        variable_end_string="}}",
        comment_start_string="{#",
        comment_end_string="#}",
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(os.path.abspath(".")),
    ),
}

j_envs["tex"].filters["latex_escape"] = latex_escape
j_envs["html"].filters["html_emph"] = html_emph
j_envs["txt"].filters["txt_emph"] = txt_emph


def main() -> None:
    if os.path.isdir("src/assets"):
        os.system(f"cp -rf src/assets {os.environ['BUILD_DIR']}")

    for config in glob.glob("src/langs/*.yml"):
        lang = config.split(os.path.sep)[-1].split(".yml")[0]
        config_lang: Any = None
        with open(config, "r", encoding="utf-8") as config_fd:
            try:
                config_lang = yaml.safe_load(config_fd)
            except yaml.YAMLError as e:
                print(e)

        if config_lang is None:
            print(f"unable to parse {config}")
            continue

        for template in glob.glob("src/templates/*.j2"):
            t_format = template.split(".")[-2]
            if t_format not in j_envs:
                print(f"template format {t_format} not supported")
                continue

            t_name = template.split(os.path.sep)[-1].split(f".{t_format}")[0]
            j_envs[t_format].get_template(template).stream(config_lang).dump(
                f"{os.environ['BUILD_DIR']}/templates/{t_name}_{lang}.{t_format}"
            )


if __name__ == "__main__":
    main()
