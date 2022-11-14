from rich.console import Console
from rich.table import Table
from rich import box
import argparse
from sys import argv
import sys

from kadoo_utils import Quadrant
from multiple_table_management_utils import get_yaml_config
from multiple_table_management_utils import get_tables_names

def base_table(new=None,info=None, quadrant=0):
    table = Table(box=box.MINIMAL)

    table.add_column("", justify="right", style="cyan", no_wrap=True)
    table.add_column("More Urgent", justify="left", style="cyan", no_wrap=True)
    table.add_column("Not Urgent", style="magenta")

    if info and quadrant:
        if quadrant in (1,2):
            row = Quadrant.get_quadrant(quadrant, info)
            table.add_row(*row)
            table.add_row("[b][white]Less Important", "", "")
        elif quadrant in (3,4):
            table.add_row("[b][white]Important", "", "")
            row = Quadrant.get_quadrant(quadrant, info)
            table.add_row(*row)
    else:
        table.add_row("[b][white]Important", "", "")
        table.add_row("[b][white]Less Important", "", "")

    console = Console()
    console.print(table)



def crazy_table(rows, default=True):
    if default:
        table_style = ["cyan", "cyan", "magenta"]
    else:
        table_style = ["", "", ""]

    table = Table(box=box.MINIMAL)

    table.add_column("", justify="right", style=table_style[0], no_wrap=True)
    table.add_column("More Urgent", justify="left", style=table_style[1], no_wrap=True)
    table.add_column("Not Urgent", style=table_style[2])

    for i, row in enumerate(rows):
        row = Quadrant.get_row(i+1, row)
        table.add_row(*row)

    return table


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command")
    tables_used = get_tables_names()
    subparsers_loaded = []
    for table in tables_used:
        print(table)
        subparsers.add_parser(name=table[0], help="ayoo")
        subparsers_loaded.append((table[0], table[1]))

    parser.add_argument("-a", "--add", type=str, required=argv in ("-a", "--add", "-r", "--remove"))
    parser.add_argument("-q", "--quadrant", type=int, choices={1, 2, 3, 4}, required="-a" in argv or "--add" in argv)
    parser.add_argument("-b", "--base", action="store_true", required=False)
    parser.add_argument("-r", "--remove", type=str, required=False)
    parser.add_argument("-ct", "--create-table", action="store_true", required=argv in ("-n", "--name"))
    parser.add_argument("-n", "--name", type=str, required=False)
    parser.add_argument("--green", action="store_true", required=False)
    parser.add_argument("--purple", action="store_true", required=False)
    parser.add_argument("--cap", action="store_true", required=False)
    parser.add_argument("--solarized", action="store_true", required=False)
    parser.add_argument("--nord", action="store_true", required=False)
    parser.add_argument("--nord-aurora", action="store_true", required=False)
    args = parser.parse_args()

    if args.create_table:
        name = args.name
        # change this to absolute path later
        location = f"./{args.name.lower()}"
        from multiple_table_management_utils import create_new_table
        create_new_table(name, location)
    else:  # load subparsers used, if any
        for table_subparser in subparsers_loaded:
            if args.command == table_subparser[0]:
                selected_table_path = table_subparser[1]
                # don't want to be working with
                # multiple tables at the same time
                break
        else:
            from multiple_table_management_utils import get_def_table
            # use default
            selected_table_path = get_def_table()


    if args.base:
        base_table()
        sys.exit(0)


    if args.quadrant and not args.add and not args.quadrant:
        print("bruh")
        sys.exit(0)


    if args.remove:
        Quadrant.remove_entry(args.quadrant, args.remove)

    if args.add:
        Quadrant.add_json(args.quadrant, args.add)


    import json
    with open(selected_table_path) as j_file:
        j = json.load(j_file)
    rows = Quadrant.get_all_quadrants(j)
    if args.green:
        t = crazy_table(rows, default=False)
    else:
        t = crazy_table(rows)
    console = Console()
    console.print(t)
