import sys
import json
import argparse

from sys import argv

from rich.console import Console
from rich.table import Table
from rich import box

from entry_utils import Quadrant
from table_utils import get_yaml_config
from table_utils import get_tables_names

def base_table(new=None,info=None, quadrant=0, table_name=None):
    table = Table(box=box.MINIMAL, title=table_name)

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
    subparsers_only = []
    for table in tables_used:
        subparser = None
        subparser = subparsers.add_parser(name=table[0], help="ayoo")
        subparsers_loaded.append((table[0], table[1]))
        subparsers_only.append(table[0])
        # if only default table then load regular argparse
        # else load the subparsers and add arguements

        subparser.add_argument("-a", "--add", type=str, required=False)
        subparser.add_argument("-q", "--quadrant", type=int, choices={1, 2, 3, 4}, required=argv in ("-a", "--add"))
        subparser.add_argument("-b", "--base", action="store_true", required=False)
        subparser.add_argument("-r", "--remove", type=str, required=False)
        subparser.add_argument("-c", "--complete", type=str, metavar="todo_name", required=False)

        subparser.add_argument("--green", action="store_true", required=False)
        subparser.add_argument("--purple", action="store_true", required=False)
        subparser.add_argument("--cap", action="store_true", required=False)
        subparser.add_argument("--solarized", action="store_true", required=False)
        subparser.add_argument("--nord", action="store_true", required=False)
        subparser.add_argument("--nord-aurora", action="store_true", required=False)

    """
    parser.add_argument("-a", "--add", type=str, required=argv in ("-a",
                                                                   "--add",
                                                                   "-r",
                                                                   "--remove") and argv not in subparsers_loaded)
    parser.add_argument("-q", "--quadrant", type=int, choices={1, 2, 3, 4},
                        required="-a" in argv or "--add" in argv and argv not
                        in subparsers_loaded)
    parser.add_argument("-r", "--remove", type=str, required=False)
    """


    parser.add_argument("-ct", "--create-table", type=str, metavar="TABLE_NAME", required=False)
    parser.add_argument( "-rt", "--remove-table", type=str,
                        metavar="TABLE_NAME", required=False
        )  # create archived tables in the future
    parser.add_argument("--green", action="store_true", required=False)
    parser.add_argument("--purple", action="store_true", required=False)
    parser.add_argument("--cap", action="store_true", required=False)
    parser.add_argument("--solarized", action="store_true", required=False)
    parser.add_argument("--nord", action="store_true", required=False)
    parser.add_argument("--nord-aurora", action="store_true", required=False)
    args = parser.parse_args()

    if "-ct" in sys.argv and not args.create_table:
        parser.error("bruh")

    # table related operations
    if args.create_table:
        name = args.create_table
        # change this to absolute path later
        location = f"./{name.lower()}.json"
        from table_utils import create_new_table
        from table_utils import initialise_table
        create_new_table(name, location)
        initialise_table(name)
        sys.exit(0)
    elif args.remove_table:
        name = args.remove_table
        from table_utils import delete_table
        delete_table(name)
        sys.exit(0)
    # regular operations
    else:  # load subparsers used, if any
        for table_subparser in subparsers_loaded:
            if args.command == table_subparser[0]:
                selected_table_path = table_subparser[1]
                # don't want to be working with
                # multiple tables at the same time
                break
        else:
            from table_utils import get_def_table
            # use default
            selected_table_path = get_def_table()

    if not args.command:
        print("Presenting default table")
        with open(selected_table_path) as j_file:
            j = json.load(j_file)
            rows = Quadrant.get_all_quadrants(j)
            t = crazy_table(rows)
        console = Console()
        console.print(t)
        sys.exit(0)

    if args.base:
        base_table()
        sys.exit(0)


    if args.quadrant and not args.add and not args.complete:
        print("bruh")
        sys.exit(0)
    if args.add and not args.quadrant:
        print("bruh")
        sys.exit(1)
    if args.complete and not args.quadrant:
        print("bruh")
        sys.exit(1)

    if args.complete:
        Quadrant.mark_complete(name=args.complete, quadrant=args.quadrant, path=selected_table_path)

    if args.remove:
        Quadrant.remove_entry(args.quadrant, args.remove, path=selected_table_path)

    if args.add:
        Quadrant.add_json(args.quadrant, args.add, path=selected_table_path)


    with open(selected_table_path) as j_file:
        j = json.load(j_file)
    rows = Quadrant.get_all_quadrants(j)
    if args.green:
        t = crazy_table(rows, default=False)
    else:
        t = crazy_table(rows)
    console = Console()
    console.print(t)
