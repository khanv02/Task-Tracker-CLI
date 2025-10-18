import json
import sys
import os
import argparse
from datetime import datetime
FILENAME = "tasks.json"
VALID_STATUS = ["in-progress", "done", "todo"]

def load_tasks():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r") as f:
        return json.load(f)
    
def save_tasks(tasks):
    with open(FILENAME, "w") as f:
        return json.dump(tasks, f, indent=2)
    
def get_args():
    parser = argparse.ArgumentParser(description="Task tracker of user")
    parser.add_argument("command", choices=["add", "update", "mark", "list", "delete", "clear"], help="Choose command")
    parser.add_argument("--id", type=int, help="Task ID")
    parser.add_argument("--status", choices=["todo", "in-progress", "done"], help="New status for mark command")
    parser.add_argument("--desc", type=str, help="Task description")
    return parser.parse_args()
    
def add_task(description, tasks):
    ts = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    task = {
        "id" : len(tasks) + 1,
        "description" : description,
        "status" : "todo",
        "created_at" : ts,
        "updated_at" : ts
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task #{task['id']}: {description}")

def list_task(tasks, status=None):
    if len(tasks) == 0:
        print("The list is empty!")
        return
    else:
        if status in VALID_STATUS:
            tasks = [task for task in tasks if task["status"] == status]
            if len(tasks) == 0:
                print("The list is empty!")
                return
        for task in tasks:
            print(f'#{task["id"]}: {task["description"]} [{task["status"]}] [created: {task["created_at"]}] [lastUpdate: {task["updated_at"]}]')

def update_task(id, description, tasks):
    ts = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    changed = 0
    for task in tasks:
        if id == task["id"]:
            task["description"] = description
            task["updated_at"] = ts
            changed = 1
            break
    if changed == 1:
        print("Update task successfully")
        save_tasks(tasks)
    else:
        print("Task not found")

def delete_task(id, tasks):
    changed = 0
    for task in tasks:
        if id == task["id"]:
            tasks.remove(task)
            changed = 1
            break
    if changed == 1:
        index = 0
        for task in tasks:
            task["id"] = index + 1
            index += 1
        print("Delete task successfully")
        save_tasks(tasks)
    else:
        print("Task not found")
        
def mark_task(id, status, tasks):
    ts = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    changed = 0
    for task in tasks:
        if id == task["id"]:
            if status in VALID_STATUS:
                task["status"] = status
                task["updated_at"] = ts 
                changed = 1
                break
    if changed == 1: 
        print("Update status task successfully")
        save_tasks(tasks)
    else:
        print("Task not found")

def main():
    tasks = load_tasks()
    args = get_args()
    command = args.command
    
    check = 0
    if command == "add":
        if args.desc:
            add_task(args.desc, tasks)
            check = 1
    elif command == "update":
        if args.desc and args.id:
            update_task(args.id, args.desc, tasks)
            check = 1
    elif command == "mark":
        if args.id and args.status:
            mark_task(args.id, args.status, tasks)
            check = 1
    elif command == "list":
        if args.status:
            list_task(tasks, args.status)
        else:
            list_task(tasks)
        check = 1
    elif command == "delete":
        if args.id:
            delete_task(args.id, tasks)
            check = 1
    elif command == "clear":
        tasks.clear()
        save_tasks(tasks)
        check = 1
    
    if check == 1:
        print("-------------[Command successfully]-------------")
    else:
        print("-------------[Error]]-------------")
    
if __name__ == "__main__":
    main()
    
""" 
[------------------{GUIDE}--------------------]
# Adding a new task

task-cli-parse add --desc "Buy groceries"
# Output: Added task #{id}: {description}

# Updating and deleting tasks
task-cli update --id 1 --desc "Buy groceries and cook dinner"
task-cli delete --id 1

# Marking a task as in progress or done
task-cli mark --status in-progress --id 1
task-cli mark --stauts done --id 1
# Listing all tasks
task-cli list

# Listing tasks by status
task-cli list --status done
task-cli list --status todo
task-cli list --status in-progress
[------------------{THANK YOU}--------------------]
""" 