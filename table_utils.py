import yaml


def get_yaml_config(yaml_path="tables.yml"):
    with open(yaml_path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return data

def get_tables_names() -> list:
    """[(table_name, table_path)]"""
    tables = []
    data = get_yaml_config()
    for table_info in data["tables"].items():
        table_data = (table_info[0], table_info[1]["Location"])
        tables.append(table_data)
    return tables


def get_def_table() -> list:
    """gets default table"""
    data = get_yaml_config()
    return data["default_table_path"]


def create_new_table(name, location):
        config = get_yaml_config()
        config["tables"][name] = ({'Location': location})
        with open("tables.yml", "w") as f:
            yaml.dump(config, f)


def delete_table(name):
    config = get_yaml_config()
    try:
        config["tables"].pop(name)
    except KeyError:
        print(f"Table name not found for deletion '{name}'")


def initialise_table(name):
    with open(f"{name}.json", "w") as f:
        init_dict = {
        "1": {
            "content": []
        },
        "2": {
            "content": []
        },
        "3": {
            "content": []
        },
        "4": {
            "content": []
        }
    }
        import json
        json.dump(init_dict, f, indent=4)


if __name__ == "__main__":
    #print(get_yaml_config())
    #print(get_tables_names())
   # print(get_def_table())
    print(delete_table(name="ayo"))
