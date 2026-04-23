# To do list 


from asyncio import tasks
import json
import os


FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(FILE):
        return []
    
    with open(FILE, "r") as file:
        return json.load(file)

def save_tasks(tasks):
    with open(FILE, "w") as file:
        json.dump(tasks, file, indent=4)


def add_task():
    tasks = load_tasks()
    
    task_name = input("Enter task: ").strip()
    
    new_id = max([t["id"] for t in tasks], default=0) + 1
    
    task = {
        "id": new_id,
        "task": task_name,
        "done": False
    }
    
    tasks.append(task)
    save_tasks(tasks)


def view_tasks():
    tasks = load_tasks()
    
    if not tasks:
        print("No tasks found.")
        return
    
    for task in tasks:
        status = "✔" if task["done"] else "✘"
        print(f'{task["id"]}. {task["task"]} [{status}]')

def mark_done():
    tasks = load_tasks()
    
    try:
        task_id = int(input("Enter task ID to mark as done: "))
    except ValueError:
        print("Please enter a valid number.")
        return
    
    for task in tasks:
        if task["id"] == task_id:
            if task["done"]:
                print("Task is already marked as done.")
                return
            
            task["done"] = True
            print("Task marked as done!")
            save_tasks(tasks)
            return
    
    print("Task not found.")

   
def delete_task():
    task_list = load_tasks()
    
    try:
        task_id = int(input("Enter task ID to delete: "))
    except ValueError:
        print("Please enter a valid number.")
        return
    
    new_tasks = [task for task in task_list if task["id"] != task_id]
    
    if len(new_tasks) == len(task_list):
        print("Task not found.")
    else:
        save_tasks(new_tasks)
        print("Task deleted!")

def menu():
    while True:
        print("\n==== TO-DO LIST ====")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Done")
        print("4. Delete Task")
        print("5. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            mark_done()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

menu()

