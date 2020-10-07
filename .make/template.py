#!/usr/bin/env python3

import glob
import jinja2
import os
import yaml

from jinja2 import Template
from distutils.dir_util import copy_tree

j_envs = {
    'tex': jinja2.Environment(
        block_start_string='\\jblock{',
        block_end_string='}',
        variable_start_string='\\jvar{',
        variable_end_string='}',
        comment_start_string='\\#{',
        comment_end_string='}',
        line_statement_prefix='%%',
        line_comment_prefix='%#',
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(os.path.abspath('.'))
    ),
    'html': jinja2.Environment(
        block_start_string='<jblock',
        block_end_string='/>',
        variable_start_string='<jvar',
        variable_end_string='/>',
        comment_start_string='<!--',
        comment_end_string='-->',
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(os.path.abspath('.'))
    )
}


for config in glob.glob('src/config_*.yaml'):
    lang = config.split('_')[1].split('.yaml')[0]
    config_lang = None
    with open(config, 'r') as config_fd:
        try:
            config_lang = yaml.safe_load(config_fd)
        except yaml.YAMLError as e:
            print(e)

    if config_lang is None:
        print('unable to parse {}'.format(config))
        continue

    for template in glob.glob('src/template_*'):
        t_format = template.split('.')[-1]
        if t_format not in j_envs:
            print('template format {} not supported'.format(t_format))
            continue

        t_name = template.split('_')[1].split('.{}'.format(t_format))[0]
        j_envs[t_format].get_template(template).stream(config_lang).dump(
            '{}/templates/{}_{}.{}'.format(os.environ['BUILD_DIR'],  t_name, lang, t_format))

    if os.path.isdir('src/assets'):
        copy_tree('src/assets', '{}'.format(os.environ['BUILD_DIR']))
