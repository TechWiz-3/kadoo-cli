import sys
import json
import argparse
import textwrap

from sys import argv

from rich.console import Console
from rich.table import Table
from rich import box

from kadoo.entry_utils import Quadrant
from kadoo.table_utils import get_yaml_config
from kadoo.table_utils import get_tables_names
from kadoo.table_utils import get_table_description
import kadoo.start_utils

KADOO = kadoo.start_utils.KADOO

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


def crazy_table(rows, default=True, style=None):
    if default:
        table_style = ["cyan", "cyan", "magenta"]
    else:
        table_style = ["", "", ""]

    table = Table(box=box.MINIMAL)

    table.add_column("", justify="right", style=table_style[0], no_wrap=True)
    table.add_column("More Urgent", justify="left", style=table_style[1], no_wrap=True)
    table.add_column("Not Urgent", style=table_style[2])

    for i, row in enumerate(rows):
        row = Quadrant.get_row(i+1, row, style=style)
        table.add_row(*row)

    return table


def cli():
    c = Console()

    description = "Just your local (awesome) Eisenhower Decision Matrix"
    epilog = "styles:\n\tgreen, purple, cap (my favorite), cap-frappe, solarized, nord, nord-aurora"
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=description, epilog=textwrap.dedent(epilog))

    subparsers = parser.add_subparsers(dest="command")
    tables_used = get_tables_names()
    subparsers_loaded = []
    subparsers_only = []
    for table in tables_used:
        subparser = None
        subparser = subparsers.add_parser(name=table[0], help=get_table_description(table[0]))
        subparsers_loaded.append((table[0], table[1]))
        subparsers_only.append(table[0])
        # if only default table then load regular argparse
        # else load the subparsers and add arguements

        subparser.add_argument("-a", "--add", type=str, required=False)
        subparser.add_argument("-q", "--quadrant", type=int, choices={1, 2, 3, 4}, required=argv in ("-a", "--add"))
        subparser.add_argument("-b", "--base", action="store_true", required=False)
        subparser.add_argument("-r", "--remove", type=str, required=False)
        subparser.add_argument("-d", "--done", type=str, metavar="todo_name", required=False)
        subparser.add_argument("-ud", "--undone", type=str, metavar="todo_name", required=False)

        subparser.add_argument("--style", type=str, metavar="STYLE_NAME", required=False)

    # load normal args
    parser.add_argument(
                "-ct", "--create-table", type=str, metavar=("TABLE_NAME", "TABLE_DESCRIPTION"), nargs=2, required=False
                    )
    parser.add_argument(
                "-rt", "--remove-table", type=str, metavar="TABLE_NAME", required=False
                    )  # create archived tables in the future
    # colorschemes
    parser.add_argument("--style", type=str, metavar="STYLE_NAME", required=False)
    args = parser.parse_args()


    if "-ct" in sys.argv and not args.create_table:
        parser.error("bruh")

    first_run = False
    # first time running
    if not start_utils.is_kadoo_setup():
        first_run = True
        print("Setting up...")
        start_utils.setup_kadoo()
        if not args.create_table:  # create a new table since the user hasn't
            table_name = c.input("Enter the name of your first todo table: ")
            description = c.input(
                "Enter the description you'd like to give the table: "
            )
            # TODO: change this to absolute path later
            location = f"{KADOO}/{table_name.lower()}.json"
            from kadoo.table_utils import create_new_table
            create_new_table(
                table_name, location, description=description, first=True
            )

    # table related operations
    if args.create_table:
        name, description = args.create_table
        # TODO: change this to absolute path later
        location = f"{KADOO}/{name.lower()}.json"
        from kadoo.table_utils import create_new_table
        create_new_table(
            name, location, description=description, first=first_run
        )
        sys.exit(0)
    elif args.remove_table:
        name = args.remove_table
        from kadoo.table_utils import delete_table
        delete_table(name)
        sys.exit(0)
    # regular operations
    else:  # load table based on subparsers used, if any
        for table_subparser in subparsers_loaded:
            if args.command == table_subparser[0]:
                selected_table_path = table_subparser[1]
                # don't want to be working with
                # multiple tables at the same time
                break
        else:  # no table subparser was used, use default table
            from kadoo.table_utils import get_def_table
            # use default
            selected_table_path = get_def_table()

    if not args.command:
        print("Presenting default table")
        with open(selected_table_path) as j_file:
            j = json.load(j_file)
            rows = Quadrant.get_all_quadrants(j)
            t = crazy_table(rows, style=args.style)
        console = Console()
        console.print(t)
        sys.exit(0)

    if args.base:
        base_table()
        sys.exit(0)


    if args.add and not args.quadrant:
        args.quadrant = c.input("Which quadrant would you like to place the item in? [1/2/3/4] ")
        try:
            args.quadrant = int(args.quadrant)
        except ValueError:
            print("Please enter an integer between 1 and 4")
            sys.exit(1)
        if args.quadrant not in (1, 2, 3, 4):
            print("You can only enter a number between 1 and 4! There is no 5th quadrant xD")

    if args.done and not args.quadrant:
        args.quadrant = c.input("Which quadrant is the item in? [1/2/3/4] ")
        try:
            args.quadrant = int(args.quadrant)
        except ValueError:
            print("Please enter an integer between 1 and 4")
            sys.exit(1)
        if args.quadrant not in (1, 2, 3, 4):
            print("You can only enter a number between 1 and 4! There is no 5th quadrant xD")

    if args.undone and not args.quadrant:
        args.quadrant = c.input("Which quadrant is the item in? [1/2/3/4] ")
        try:
            args.quadrant = int(args.quadrant)
        except ValueError:
            print("Please enter an integer between 1 and 4")
            sys.exit(1)
        if args.quadrant not in (1, 2, 3, 4):
            print("You can only enter a number between 1 and 4! There is no 5th quadrant xD")

    if args.done:
        Quadrant.mark_complete(name=args.done, quadrant=args.quadrant, path=selected_table_path)
    elif args.undone:
        Quadrant.mark_undone(name=args.undone, quadrant=args.quadrant, path=selected_table_path)

    if args.remove:
        Quadrant.remove_entry(args.quadrant, args.remove, path=selected_table_path)

    if args.add:
        Quadrant.add_json(args.quadrant, args.add, path=selected_table_path)


    with open(selected_table_path) as j_file:
        j = json.load(j_file)
    rows = Quadrant.get_all_quadrants(j)
    t = crazy_table(rows, style=args.style)
    console = Console()
    console.print(t)


if __name__ == "__main__":
    cli()
