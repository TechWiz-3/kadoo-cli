import toml


class Config:


    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        with open(config_file_path) as f:
            self.config = toml.load(f)


    def get_config(self):
        return self.config


    def get_completed_style(self):
    #        return self.config["completed_style"]
        style = self.config["completed_style"]
        open_s = f"[{style}]"
        close_s = f"[/{style}]"
        return [open_s, close_s]


    def get_default_style(self):
        return self.config["default_style"]


#config = Config("kadoo.toml")
