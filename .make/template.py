#!/usr/bin/env python3

import glob
import os

import jinja2
import yaml

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

if os.path.isdir("src/assets"):
    os.system(f"cp -rf src/assets {os.environ['BUILD_DIR']}")

for config in glob.glob("src/langs/*.yml"):
    lang = config.split(os.path.sep)[-1].split(".yml")[0]
    CONFIG_LANG = None
    with open(config, "r", encoding="utf-8") as config_fd:
        try:
            CONFIG_LANG = yaml.safe_load(config_fd)
        except yaml.YAMLError as e:
            print(e)

    if CONFIG_LANG is None:
        print(f"unable to parse {config}")
        continue

    for template in glob.glob("src/templates/*.j2"):
        t_format = template.split(".")[-2]
        if t_format not in j_envs:
            print(f"template format {t_format} not supported")
            continue

        t_name = template.split(os.path.sep)[-1].split(f".{t_format}")[0]
        j_envs[t_format].get_template(template).stream(CONFIG_LANG).dump(
            f"{os.environ['BUILD_DIR']}/templates/{t_name}_{lang}.{t_format}"
        )
