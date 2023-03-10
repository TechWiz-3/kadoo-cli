# Kadoo

![Example](https://github.com/TechWiz-3/kadoo-cli/blob/main/media/example2.png?raw=true)

> The priorities management CLI you never knew you needed

Kadoo organises your priorities using the Eisenhower Decision Matrix.  

## Installation
```sh
pip install kadoo
```

## Usage

```sh
# get started by creating your first matrix board
$ kadoo

# to perform actions on your new table, use it's name
$ kadoo <table_name>

# add an item to quadrant 1
$ kadoo <table_name> -a "My first item" -q 1

# create a new table: kadoo -ct <TABLE_NAME> <TABLE_DESCRIPTION>
$ kadoo -ct dev "My developer tasks"

# add an item to quadrant 1
$ kadoo dev -a "Work on a new project" -q 1

# add an item to quadrant 2
$ kadoo dev -a "Star this repo xDD" -q 2

# mark a task as done: kadoo <TABLE_NAME> -d "<TASK_NAME>" -q <QUADRANT>
$ kadoo dev -d "Work on a new project" -q 1
```

## About 
The matrix sorts tasks based on urgency and importance.  

<img src="https://luxafor.com/wp-content/uploads/2022/06/The-Eisenhower-Decision-Matrix-png-1024x768.png" alt="Eisenhower Matrix" width="400">

## Configuration

Kadoo is highly configurable. Data files are stored in the `~/.kadoo` directory.  
Tables can be added manually to `~/.kadoo/tables.yml` and the default table can be changed there (a command for this will be released in future updates).  

The `kadoo.toml` file allows configuration of the style (colorscheme), completed task style and emoji.  

Configuration for `kadoo.toml` follows [Rich Markup](https://rich.readthedocs.io/en/latest/markup.html). A recommended value for `completed_style` would be `dim strikethrough`

In the future configuration options will be added for:
1. Incompleted task emoji
2. Table style
