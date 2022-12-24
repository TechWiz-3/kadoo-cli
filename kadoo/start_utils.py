"""For configuring the .kadoo directory"""

import os
import yaml
import toml

KADOO = os.path.expanduser("~/.kadoo")
# KADOO = "./testing"

# create .kadoo dir
# create tables.yml
# create kadoo.toml


def is_kadoo_setup():
    return os.path.exists(KADOO)


def create_tables_yml():
    with open(f"{KADOO}/tables.yml", "w") as f:
        tables = {
              "default_table_name": None,
              "default_table_path": None,
              "tables": {}
            }
        yaml.dump(tables, f, indent=4)


def create_kadoo_toml():
    with open(f"{KADOO}/kadoo.toml", "w"):
        config = {
            'default_style': 'cap',
            'default_completed_emoji': '[green]✔[/green]',
            'completed_style': '',
            'default_incompleted_emoji': '',
        }
        with open(f"{KADOO}/kadoo.toml", "w") as f:
            toml.dump(config, f)


def setup_kadoo():
    if not is_kadoo_setup():
        os.mkdir(KADOO)  # create .kadoo dir
        create_tables_yml()
        create_kadoo_toml()
