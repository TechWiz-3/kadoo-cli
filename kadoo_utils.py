import json
import sys

if "--green" in sys.argv:
    style_1 = "[green1]"
    style_1_close = "[/green1]"
    #style_2 = "[bright_green]"
    #style_2_close = "[/bright_green]"
    style_2 = "[green3]"
    style_2_close = "[/green3]"
    style_3 = "[green4]"
    style_3_close = "[/green4]"
    style_4 = "[dark_green]"
    style_4_close = "[/dark_green]"
elif "--purple" in sys.argv:
#    style_1 = "[medium_violet_red]"
#    style_1_close = "[/medium_violet_red]"
#    style_2 = "[dark_violet]"
#    style_2_close = "[/dark_violet]"
#    style_3 = "[magenta1]"
#    style_3_close = "[/magenta1]"
##    style_3 = "[medium_orchid]"
##    style_3_close = "[/medium_orchid]"
#    style_4 = "[deep_pink1]"
#    style_4_close = "[/deep_pink1]"
    style_1 = "[#D67CF7]"
    style_1_close = "[/#D67CF7]"
    style_2 = "[#C86EEE]"
    style_2_close = "[/#C86EEE]"
    style_3 = "[#BA60E5]"
    style_3_close = "[/#BA60E5]"
    style_4 = "[#963CCF]"
    style_4_close = "[/#963CCF]"
elif "--cat" in sys.argv:
    if "frappe" not in sys.argv:
        style_1 = "[#ed8796]"
        style_1_close = "[/#ed8796]"
        style_2 = "[#f5a97f]"
        style_2_close = "[/#f5a97f]"
        style_3 = "[#c6a0f6]"
        style_3_close = "[/#c6a0f6]"
        style_4 = "[#8aadf4]"
        style_4_close = "[/#8aadf4]"
    else:
        style_1 = "[#d20f39]"
        style_1_close = "[/#d20f39]"
        style_2 = "[#fe640b]"
        style_2_close = "[/#fe640b]"
        style_3 = "[#04a5e5]"
        style_3_close = "[/#04a5e5]"
        style_4 = "[#8839ef]"
        style_4_close = "[/#8839ef]"
elif "--solarized" in sys.argv:
        style_1 = "[#dc322f]"
        style_1_close = "[/#dc322f]"
        style_2 = "[#d33682]"
        style_2_close = "[/#d33682]"
        style_3 = "[#268bd2]"
        style_3_close = "[/#268bd2]"
        style_4 = "[#859900]"
        style_4_close = "[/#859900]"
elif "--nord" in sys.argv:
    style_1 = "[#5e81ac]"
    style_1_close = "[/#5e81ac]"
    style_2 = "[#81a1c1]"
    style_2_close = "[/#81a1c1]"
    style_3 = "[#88c0d0]"
    style_3_close = "[/#88c0d0]"
    style_4 = "[#8fbcbb]"
    style_4_close = "[/#8fbcbb]"
elif "--nord-aurora" in sys.argv:
    style_1 = "[#bf616a]"
    style_1_close = "[/#bf616a]"
    style_2 = "[#d08770]"
    style_2_close = "[/#d08770]"
    style_3 = "[#ebcb8b]"
    style_3_close = "[/#ebcb8b]"
    style_4 = "[#a3be8c]"
    style_4_close = "[/#a3be8c]"
else:
    style_1 = "[blue]"
    style_1_close = "[/blue]"
    style_2 = "[magenta]"
    style_2_close = "[/magenta]"
    style_3 = "[blue]"
    style_3_close = "[/blue]"
    style_4 = "[magenta]"
    style_4_close = "[/magenta]"

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
            # no.1
            rest_of_row[0] = f"{style_1}{rest_of_row[0]}{style_1_close}"
            # no. 2
            rest_of_row[1] = f"{style_2}{rest_of_row[1]}{style_2_close}"
            return "[b][white]Important", *rest_of_row
        if r_num == 2:
            # no. 3
            rest_of_row[0] = f"{style_3}{rest_of_row[0]}{style_3_close}"
            # no. 4
            rest_of_row[1] = f"{style_4}{rest_of_row[1]}{style_4_close}"
            return "[b][white]Less Important", *rest_of_row


    @classmethod
    def add_json(self, quadrant, info):
        quadrant = str(quadrant)
        with open("table.json", "r+") as file:
            table = json.load(file)
            quadrant_content = list(table[quadrant].values())[0]
            if not len(quadrant_content): # 0
                quadrant_content.append(f"○ {info}")
            else:
                quadrant_content.append(f"\n○ {info}")
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
                if name == item or f"\n○ {name}" == item:
                    # change above to also include ○ tick/checkmark
                    if i == 0:
                        quadrant_content.remove(name)
                        # remove the newline on next entry
                        quadrant_content = Quadrant.update_newlines(quadrant_content)
                    else:
                        quadrant_content.remove(f"\n○ {name}")
                        # same here ^^^^
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
