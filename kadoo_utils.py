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
    def get_all_quadrants(self, json):
        quadrants = []
        top_row = []
        bottom_row = []
        for i in range(1,5):
            if i == 1 or i == 2:
                top_row.append(json[str(i)])
            else:
                bottom_row.append(json[str(i)])
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
            if table[quadrant] == "":
                table[quadrant] += info
            else:
                table[quadrant] += f"\n{info}"
            file.seek(0)
            json.dump(table, file, indent=4)
        # write to quadrant
        return None


    @classmethod
    def remove_entry(self, quadrant, name):
        import re
        quadrant = str(quadrant)
        with open("table.json", "r+") as file:
            table = json.load(file)
            table[quadrant] = re.sub(rf"\n{name}", '', table[quadrant])
        with open("table.json", "w") as file:
            json.dump(table, file, indent=4)

