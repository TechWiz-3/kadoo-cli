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
        table_data = (table_info[0], table_info[1]["location"])
        tables.append(table_data)
    return tables


def get_def_table() -> list:
    """gets default table"""
    data = get_yaml_config()
    return data["default_table_path"]


def get_table_description(table_name) -> str:
    """gets table's description"""
    data = get_yaml_config()
    return data["tables"][table_name]["description"]


def create_new_table(name, location, description="no description"):
        config = get_yaml_config()
        config["tables"][name] = ({'location': location, 'description': description})
        with open("tables.yml", "w") as f:
            yaml.dump(config, f)
        print("New table log created")


def delete_table(name):
    config = get_yaml_config()
    try:
        config["tables"].pop(name)
    except KeyError:
        print(f"Table name not found for deletion '{name}'")
    else:
        with open("tables.yml", "w") as f:
            yaml.dump(config, f)
        print("Success")


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
    print("Data entered into table")


if __name__ == "__main__":
    pass
    #print(get_yaml_config())
    #print(get_tables_names())
   # print(get_def_table())
#    print(delete_table(name="ayo"))
