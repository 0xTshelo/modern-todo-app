import tkinter as tk
from tkinter import messagebox
import json
import os

FILE = "tasks.json"

# ---------------- DATA FUNCTIONS ---------------- #

def load_tasks():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as file:
        return json.load(file)

def save_tasks(tasks):
    with open(FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# ---------------- GUI FUNCTIONS ---------------- #

def refresh_listbox():
    task_listbox.delete(0, tk.END)
    tasks = load_tasks()
    
    for task in tasks:
        status = "✔" if task["done"] else "✘"
        task_listbox.insert(tk.END, f'{task["id"]}. {task["task"]} [{status}]')

def add_task():
    task_name = entry.get().strip()
    
    if not task_name:
        messagebox.showwarning("Warning", "Task cannot be empty")
        return
    
    tasks = load_tasks()
    new_id = max([t["id"] for t in tasks], default=0) + 1
    
    task = {
        "id": new_id,
        "task": task_name,
        "done": False
    }
    
    tasks.append(task)
    save_tasks(tasks)
    
    entry.delete(0, tk.END)
    refresh_listbox()

def mark_done():
    try:
        selected = task_listbox.get(task_listbox.curselection())
        task_id = int(selected.split(".")[0])
    except:
        messagebox.showwarning("Warning", "Select a task first")
        return
    
    tasks = load_tasks()
    
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            break
    
    save_tasks(tasks)
    refresh_listbox()

def delete_task():
    try:
        selected = task_listbox.get(task_listbox.curselection())
        task_id = int(selected.split(".")[0])
    except:
        messagebox.showwarning("Warning", "Select a task first")
        return
    
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    
    save_tasks(tasks)
    refresh_listbox()

# ---------------- UI SETUP ---------------- #

root = tk.Tk()
root.title("To-Do List")
root.geometry("400x400")

# Entry
entry = tk.Entry(root, width=30)
entry.pack(pady=10)

# Buttons
btn_add = tk.Button(root, text="Add Task", command=add_task)
btn_add.pack()

btn_done = tk.Button(root, text="Mark as Done", command=mark_done)
btn_done.pack()

btn_delete = tk.Button(root, text="Delete Task", command=delete_task)
btn_delete.pack()

# Listbox
task_listbox = tk.Listbox(root, width=50)
task_listbox.pack(pady=20)

# Load tasks on startup
refresh_listbox()

root.mainloop()
