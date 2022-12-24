import os
import yaml

class SetupUtils:

    home = os.path.expanduser("~")
    k_dir = os.path.expanduser("~/.kadoo")
    t_dir = os.path.expanduser("~/.kadoo/tables")  # table dir

    def __init__(self):
        pass


    def setup_kadoo(self):
        # create ~/.kadoo dir
        os.mkdir(f"{home}/.kadoo")

        # create tables.yml
        with open(f"{k_dir}/tables.yml", "w") as f:
            # populate tables.yml
            yaml_dict = {
                'default_table_name': 'Default',
                'default_table_path': f"{tables}/default.json",
                'tables':
                    {
                        'default': {'Location': f"{tables}/default.json"}
                    }
            }
            yaml.dump(yaml_dict, f)

        # create tables directory


        # create and populate default table
        # json file as in tables.yml

        # create kadoo.toml
        # populate kadoo.toml


    def create_new_table_file(self):
        pass
