import json
import re
import sys

from kadoo.config_utils import Config
from kadoo.start_utils import KADOO

args = sys.argv


def get_style_tags():
    c = Config(f"{KADOO}/kadoo.toml")
    configured_style = c.get_default_style()

    if not configured_style:
        pass
    elif args not in ("green", "purple", "cap", "cap-frappe", "nord", "nord-aurora"):
        args.append(configured_style)

    if "green" in args:
        style_1 = "[green1]"
        style_1_close = "[/green1]"
        style_2 = "[green3]"
        style_2_close = "[/green3]"
        style_3 = "[green4]"
        style_3_close = "[/green4]"
        style_4 = "[dark_green]"
        style_4_close = "[/dark_green]"
    elif "purple" in args:
        style_1 = "[#D67CF7]"
        style_1_close = "[/#D67CF7]"
        style_2 = "[#C86EEE]"
        style_2_close = "[/#C86EEE]"
        style_3 = "[#BA60E5]"
        style_3_close = "[/#BA60E5]"
        style_4 = "[#963CCF]"
        style_4_close = "[/#963CCF]"
    elif "cap-frappe" in args:
        style_1 = "[#d20f39]"
        style_1_close = "[/#d20f39]"
        style_2 = "[#fe640b]"
        style_2_close = "[/#fe640b]"
        style_3 = "[#04a5e5]"
        style_3_close = "[/#04a5e5]"
        style_4 = "[#8839ef]"
        style_4_close = "[/#8839ef]"
    elif "cap":
        style_1 = "[#ed8796]"
        style_1_close = "[/#ed8796]"
        style_2 = "[#f5a97f]"
        style_2_close = "[/#f5a97f]"
        style_3 = "[#c6a0f6]"
        style_3_close = "[/#c6a0f6]"
        style_4 = "[#8aadf4]"
        style_4_close = "[/#8aadf4]"
    elif "solarized" in args:
            style_1 = "[#dc322f]"
            style_1_close = "[/#dc322f]"
            style_2 = "[#d33682]"
            style_2_close = "[/#d33682]"
            style_3 = "[#268bd2]"
            style_3_close = "[/#268bd2]"
            style_4 = "[#859900]"
            style_4_close = "[/#859900]"
    elif "nord" in args:
        style_1 = "[#5e81ac]"
        style_1_close = "[/#5e81ac]"
        style_2 = "[#81a1c1]"
        style_2_close = "[/#81a1c1]"
        style_3 = "[#88c0d0]"
        style_3_close = "[/#88c0d0]"
        style_4 = "[#8fbcbb]"
        style_4_close = "[/#8fbcbb]"
    elif "nord-aurora" in args:
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
    return [(style_1, style_1_close, style_2, style_2_close), (style_3, style_3_close, style_4, style_4_close)]

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
    def get_row(self, r_num, rest_of_row, style):
        style_tag_data = get_style_tags()

        for i, style_tags in enumerate(style_tag_data):
            if r_num == 1 and i == 0:
                a_open, a_close, b_open, b_close = style_tags
                # no.1
                rest_of_row[0] = f"{a_open}{rest_of_row[0]}{a_close}"
                # no. 2
                rest_of_row[1] = f"{b_open}{rest_of_row[1]}{b_close}"
                return "[b][white]Important", *rest_of_row
            if r_num == 2 and i == 1:
                a_open, a_close, b_open, b_close = style_tags
                # no. 3
                rest_of_row[0] = f"{a_open}{rest_of_row[0]}{a_close}"
                # no. 4
                rest_of_row[1] = f"{b_open}{rest_of_row[1]}{b_close}"
                return "[b][white]Less Important", *rest_of_row


    @classmethod
    def add_json(self, quadrant, info, path):
        quadrant = str(quadrant)
        with open(path, "r+") as file:
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
    def remove_entry(self, quadrant, name, path):
        quadrant = str(quadrant)
        with open(path, "r+") as file:
            change = False
            table = json.load(file)
            quadrant_content = list(table[quadrant].values())[0]
            for i, item in enumerate(quadrant_content):
                if f"○ {name}" == item or f"\n○ {name}" == item:
                    # change above to also include ○ tick/checkmark
                    ## ^^                                ^^^^^^^
                    if i == 0:
                        quadrant_content.remove(name)
                        # remove the newline on next entry
                        quadrant_content = Quadrant.update_newlines(quadrant_content)
                    else:
                        quadrant_content.remove(f"\n○ {name}")
                        # same here ^^^^
                    change = True
                    break
                    table[quadrant] = {"content": quadrant_content}
        if change:
            with open(path, "w") as file:
                json.dump(table, file, indent=4)
        else:
            print("Not found, no changes made")


    @classmethod
    def mark_complete(self, quadrant, name, path):
        from kadoo.config_utils import Config
        c = Config("kadoo.toml")
        s = c.get_completed_style()
        # if no config style
        if s[0] == "[]":
            s[0] = ""
            s[1] = ""
        quadrant = str(quadrant)
        changes = False
        with open(path, "r+") as file:
            table = json.load(file)
            quadrant_content = list(table[quadrant].values())[0]
            for todo_item in quadrant_content:
                if todo_item == f"○ {name}" or todo_item == f"\n○ {name}":
                    index = quadrant_content.index(todo_item)
#                    marked = re.sub("○", "[green]✔[/green]", todo_item)
                    if index > 0:  # use newlines
                        # remove the newline and empty circle
                        marked = re.sub("\n○ ", "", todo_item)
                        # apply user configured style with new checkmark and
                        # newline
                        marked = f"\n[green]✔[/green] {s[0]}{marked}{s[1]}"
                    elif index == 0:
                        # no newline
                        # remove the empty circle
                        marked = re.sub("○ ", "", todo_item)
                        # apply user configured style with new checkmark and
                        # newline
                        marked = f"[green]✔[/green] {s[0]}{marked}{s[1]}"

                    # assign changes
                    quadrant_content[index] = marked
                    table[quadrant] = {"content": quadrant_content}
                    changes = True
                    break
        if changes:  # if todo found and changed
            # rewrite table file
            with open(path, "w") as file:
                json.dump(table, file, indent=4)
        else:
            print("Not found, no changes made")


    @classmethod
    def mark_undone(self, quadrant, name, path):
        quadrant = str(quadrant)
        changes = False
        with open(path, "r+") as file:
            table = json.load(file)
            quadrant_content = list(table[quadrant].values())[0]
            pattern = re.compile(f"(\n)?\[green]✔\[/green] \[[a-z ]*\]{name}\[/[a-z ]*\]")
            pattern2 = re.compile(f"(\n)?\[green]✔\[/green] {name}")
            for todo_item in quadrant_content:
                result = re.match(pattern, todo_item)
                result2 = re.match(pattern2, todo_item)
                if result is not None:
                    index = quadrant_content.index(result.group())
                    # replace the green tick with empty circle
                    marked = re.sub("\[green]✔\[/green]", "\u25cb", result.group())
                    marked = re.sub(r"\[/[a-z ]*\]", "", marked)
                    marked = re.sub(r"\[[a-z ]*\]", "", marked)
                    quadrant_content[index] = marked
                    table[quadrant] = {"content": quadrant_content}
                    changes = True
                    break
                elif result2 is not None:
                    index = quadrant_content.index(result2.group())
                    # replace the green tick with empty circle
                    marked = re.sub("\[green]✔\[/green]", "\u25cb", result2.group())
                    marked = re.sub(r"\[/[a-z ]*\]", "", marked)
                    marked = re.sub(r"\[[a-z ]*\]", "", marked)
                    quadrant_content[index] = marked
                    table[quadrant] = {"content": quadrant_content}
                    changes = True
                    break
        if changes:  # if todo found and changed
            # rewrite table file
            with open(path, "w") as file:
                json.dump(table, file, indent=4)
        else:
            print("Not found, no changes made")


    @classmethod
    def update_newlines(self, content) -> str:
        """remove the newline char on the next line after deleting the first
        entry"""
        content[0] = re.sub("\n", "",  content[0])
        return content
