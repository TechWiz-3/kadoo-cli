import json

class Quadrant:

    def __init__(self, table):
        self.table = table

    @classmethod
    def get_quadrant(self, q_num, txt):
        if q_num == 1:
            return "[b][white]Important", txt, ""
        if q_num == 2:
            return "[b][white]Important", "", txt
        if q_num == 3:
            return "[b][white]Less Important", txt, ""
        if q_num == 4:
            return "[b][white]Less Important", "", txt

    @classmethod
    def get_all_quadrants(self, j_data):
        quadrants = []
        top_row = []
        bottom_row = []
        for i in range(1, 5):
            contents_str = ""
            if i == 1 or i == 2:
                for item in list(j_data[str(i)].values())[0]:
                    contents_str += item
                top_row.append(contents_str)
            else:
                for item in list(j_data[str(i)].values())[0]:
                    contents_str += item
                bottom_row.append(contents_str)
        quadrants.append(top_row)
        quadrants.append(bottom_row)
        return quadrants


    @classmethod
    def get_row(self, r_num, rest_of_row):
        if r_num == 1:
            return "[b][white]Important", *rest_of_row
        if r_num == 2:
            return "[b][white]Less Important", *rest_of_row


    @classmethod
    def add_json(self, quadrant, info):
        quadrant = str(quadrant)
        with open("table.json", "r+") as file:
            table = json.load(file)
            quadrant_content = list(table[quadrant].values())[0]
            if not len(quadrant_content):
                quadrant_content.append(f"\n{info}")
            else:
                quadrant_content.append(info)
            table[quadrant] = {"content": quadrant_content}
            file.seek(0)
            json.dump(table, file, indent=4)


    @classmethod
    def remove_entry(self, quadrant, name):
        quadrant = str(quadrant)
        with open("table.json", "r+") as file:
            table = json.load(file)
            quadrant_content = list(table[quadrant].values())[0]
            for i, item in enumerate(quadrant_content):
                if name == item or f"\n{name}" == item:
                    if i == 0:
                        quadrant_content.remove(name)
                        # remove the newline on next entry
                        quadrant_content = Quadrant.update_newlines(quadrant_content)
                    else:
                        quadrant_content.remove(f"\n{name}")
            table[quadrant] = {"content": quadrant_content}
        with open("table.json", "w") as file:
            json.dump(table, file, indent=4)


    @classmethod
    def update_newlines(self, content) -> str:
        """remove the newline char on the next line after deleting the first
        entry"""
        import re
        content[0] = re.sub("\n", "",  content[0])
        return content
