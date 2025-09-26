import json
import os
import sys
from datetime import datetime

task_file = "tasks.json"
now = datetime.now().isoformat()

def load_tasks():
    if not os.path.exists(task_file):
        return []
    

    with open(task_file, "r") as f:
        return json.load(f)
    
def save_tasks(tasks):
    with open(task_file, "w") as f: 
        json.dump(tasks, f, indent = 2)

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    for task in tasks:
        print(f"[{task['id']}] {task['description']} - {task['status']}")

def add_task(description):
    tasks = load_tasks()
    task_id = 1 if not tasks else tasks[-1]["id"] + 1
    new_task = {
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now 
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task_id})")

def delete_task(task_id):
    tasks = load_tasks()
    task_found = False

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            task_found = True
            break
    
    if task_found:
        save_tasks(tasks)
        print(f"Task {task_id} deleted successfully")
    else:
        print(f"No task found with ID{task_id}")

def update_task(task_id, new_status):
    tasks = load_tasks()
    found = False
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = new_status
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            found = True
            break
    if not found:
        print(f"No task found with ID {task_id}")
        return



##################################################################################

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python task-cli.py <command> [arguments]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "list":
        list_tasks()
    elif command == "add":
        description = " ".join(sys.argv[2:])
        if not description:
            print("Please provide a task description.")
        else:
            add_task(description)
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Please provide the task ID to delete.")
        else:
            delete_task(int(sys.argv[2]))
    elif command == "update":
        if len(sys.argv) < 4:
            print("Usage: python task-cli.py update <id> <new description>")
        else:
            task_id = int(sys.argv[2])
            new_description = " ".join(sys.argv[3:])
            update_task(task_id, new_description)
    else:
        print(f"Unknown command: {command}")


        
