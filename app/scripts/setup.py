import yaml
from sys import platform
import os
from pathlib import Path
from typing import Dict, List

PARENT_DIR = Path('.')

### App Info ###
def load_description()-> str:
    with open(PARENT_DIR / 'description.md', 'r') as desc:
        return desc.read()

app_desc = load_description()

def load_meta_tags()-> List:
    with open(PARENT_DIR / 'conf' / 'meta_tags.yaml', 'r') as mt:
        return yaml.safe_load(mt)
        
meta_tags = load_meta_tags()
### --- --- ###

### Logs ###
def log_runtime()-> None:
    with open(PARENT_DIR / 'conf' / 'runtime.yaml', 'w') as p_log:
        p_log.write('ppid: %s\npid: %s' % (os.getppid(), os.getpid()))
### --- --- ###


### Configurations ###
def parse_configs()-> Dict: # Load into main file
    with open(PARENT_DIR / 'conf' / 'config.yaml', 'r') as conf:
        return yaml.safe_load(conf)

configs = parse_configs()

def parse_secrets()-> Dict: # Load secrets
    with open(PARENT_DIR / 'conf' / '.secrets', 'r') as conf:
        return yaml.safe_load(conf)

def parse_text_templates()-> Dict: # Load text templates
    with open(PARENT_DIR / 'templates' / 'text_templates.yaml', 'r') as tt:
        return yaml.safe_load(tt)


secrets = parse_secrets()
text_temp = parse_text_templates()
### --- --- ###

