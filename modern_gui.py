import customtkinter as ctk
import json
import os
from tkinter import messagebox

ctk.set_appearance_mode("dark")  # dark mode
ctk.set_default_color_theme("blue")

FILE = "tasks.json"

# ---------------- DATA ---------------- #

def load_tasks():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as file:
        return json.load(file)

def save_tasks(tasks):
    with open(FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# ---------------- APP ---------------- #

class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("To-Do App")
        self.geometry("500x500")

        # Title
        self.label = ctk.CTkLabel(self, text="My Tasks", font=("Arial", 24))
        self.label.pack(pady=15)

        # Input
        self.entry = ctk.CTkEntry(self, placeholder_text="Enter a task...", width=300)
        self.entry.pack(pady=10)

        # Buttons frame
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=10)

        self.add_btn = ctk.CTkButton(btn_frame, text="Add", command=self.add_task)
        self.add_btn.grid(row=0, column=0, padx=5)

        self.done_btn = ctk.CTkButton(btn_frame, text="Done", command=self.mark_done)
        self.done_btn.grid(row=0, column=1, padx=5)

        self.delete_btn = ctk.CTkButton(btn_frame, text="Delete", command=self.delete_task, fg_color="red")
        self.delete_btn.grid(row=0, column=2, padx=5)

        # Task list
        self.task_frame = ctk.CTkScrollableFrame(self, width=400, height=300)
        self.task_frame.pack(pady=20)

        self.refresh_tasks()

    def refresh_tasks(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        tasks = load_tasks()

        for task in tasks:
            status = "✔" if task["done"] else "✘"

            task_text = f"{task['id']}. {task['task']} [{status}]"

            label = ctk.CTkLabel(self.task_frame, text=task_text, anchor="w")
            label.pack(fill="x", padx=10, pady=5)

            label.bind("<Button-1>", lambda e, t=task["id"]: self.select_task(t))

    def select_task(self, task_id):
        self.selected_id = task_id

    def add_task(self):
        task_name = self.entry.get().strip()

        if not task_name:
            messagebox.showwarning("Warning", "Task cannot be empty")
            return

        tasks = load_tasks()
        new_id = max([t["id"] for t in tasks], default=0) + 1

        tasks.append({
            "id": new_id,
            "task": task_name,
            "done": False
        })

        save_tasks(tasks)
        self.entry.delete(0, "end")
        self.refresh_tasks()

    def mark_done(self):
        if not hasattr(self, "selected_id"):
            messagebox.showwarning("Warning", "Select a task")
            return

        tasks = load_tasks()

        for task in tasks:
            if task["id"] == self.selected_id:
                task["done"] = True

        save_tasks(tasks)
        self.refresh_tasks()

    def delete_task(self):
        if not hasattr(self, "selected_id"):
            messagebox.showwarning("Warning", "Select a task")
            return

        tasks = load_tasks()
        tasks = [t for t in tasks if t["id"] != self.selected_id]

        save_tasks(tasks)
        self.refresh_tasks()


if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
