# Kadoo

![Example](./media/example1.png)

> The priorities management CLI you never knew you needed

Kadoo organises your priorities using the Eisenhower Decision Matric.  

## Usage

```sh
# view default table
$ kadoo

# create a new table: kadoo -ct <TABLE_NAME> <TABLE_DESCRIPTION>
$ kadoo -ct dev "My developer tasks"

# add an item to quadrant 1
$ kadoo dev -a "Work on a new project" -q 1

# add an item to quadrant 2
$ kadoo dev -a "Star this repo xDD" -q 2

# mark a task as done: kadoo <TABLE_NAME> -d "<TASK_NAME>" -q <QUADRANT>
$ kadoo dev -a "Work on a new project" -q 1
```

## About 
The matrix sorts tasks based on urgency and importance.  

<img src="https://luxafor.com/wp-content/uploads/2022/06/The-Eisenhower-Decision-Matrix-png-1024x768.png" alt="Eisenhower Matrix" width="400">

