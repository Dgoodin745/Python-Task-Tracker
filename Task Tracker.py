import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
import json
import os
import csv
from datetime import datetime

class TaskTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Tracker")
        self.root.geometry("800x600")  # Set the window size
        self.tasks = []

        self.load_tasks()

        self.apply_dark_mode()

        self.tab_control = ttk.Notebook(self.root)
        
        self.tab_active = ttk.Frame(self.tab_control)
        self.tab_completed = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.tab_active, text='Active Tasks')
        self.tab_control.add(self.tab_completed, text='Completed Tasks')
        self.tab_control.pack(expand=1, fill="both")

        # Active Tasks Tab
        self.active_task_frame = tk.Frame(self.tab_active, bg="#2e2e2e")
        self.active_task_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.new_task_label = tk.Label(self.active_task_frame, text="New Task", fg="white", bg="#2e2e2e")
        self.new_task_label.pack()

        self.new_task_entry = tk.Entry(self.active_task_frame, bg="#3e3e3e", fg="white")
        self.new_task_entry.pack(fill="x")

        self.add_task_button = tk.Button(self.active_task_frame, text="Add Task", command=self.add_task, bg="#3e3e3e", fg="white")
        self.add_task_button.pack()

        self.active_task_listbox = tk.Listbox(self.active_task_frame, selectmode=tk.SINGLE, bg="#3e3e3e", fg="white")
        self.active_task_listbox.pack(fill="both", expand=True)
        self.active_task_listbox.bind('<<ListboxSelect>>', self.display_comment)

        self.complete_task_button = tk.Button(self.active_task_frame, text="Complete Task", command=self.complete_task, bg="#3e3e3e", fg="white")
        self.complete_task_button.pack()

        self.comment_label = tk.Label(self.active_task_frame, text="Comment", fg="white", bg="#2e2e2e")
        self.comment_label.pack()

        self.comment_entry = scrolledtext.ScrolledText(self.active_task_frame, wrap=tk.WORD, height=4, bg="#3e3e3e", fg="white")
        self.comment_entry.pack(fill="x")

        self.add_comment_button = tk.Button(self.active_task_frame, text="Add Comment", command=self.add_comment, bg="#3e3e3e", fg="white")
        self.add_comment_button.pack()

        # Completed Tasks Tab
        self.completed_task_frame = tk.Frame(self.tab_completed, bg="#2e2e2e")
        self.completed_task_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.completed_task_listbox = tk.Listbox(self.completed_task_frame, selectmode=tk.SINGLE, bg="#3e3e3e", fg="white")
        self.completed_task_listbox.pack(fill="both", expand=True)
        self.completed_task_listbox.bind('<<ListboxSelect>>', self.display_comment)

        self.comment_display_label = tk.Label(self.completed_task_frame, text="Comments:", fg="white", bg="#2e2e2e")
        self.comment_display_label.pack()

        self.completed_comment_entry = scrolledtext.ScrolledText(self.completed_task_frame, wrap=tk.WORD, height=4, bg="#3e3e3e", fg="white")
        self.completed_comment_entry.pack(fill="x")

        self.add_completed_comment_button = tk.Button(self.completed_task_frame, text="Add Comment to Completed Task", command=self.add_comment, bg="#3e3e3e", fg="white")
        self.add_completed_comment_button.pack()

        self.move_to_active_button = tk.Button(self.completed_task_frame, text="Move to Active", command=self.move_to_active, bg="#3e3e3e", fg="white")
        self.move_to_active_button.pack()

        self.export_button = tk.Button(self.completed_task_frame, text="Export Completed Tasks to CSV", command=self.export_to_csv, bg="#3e3e3e", fg="white")
        self.export_button.pack()

        self.load_tasks_into_listboxes()

    def apply_dark_mode(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background="#2e2e2e", foreground="white")
        style.configure("TNotebook.Tab", background="#3e3e3e", foreground="white")
        style.map("TNotebook.Tab", background=[("selected", "#2e2e2e")], foreground=[("selected", "white")])

    def load_tasks(self):
        if os.path.exists('tasks.json'):
            with open('tasks.json', 'r') as file:
                self.tasks = json.load(file)
            # Ensure all tasks have date_added and date_completed fields
            for task in self.tasks:
                if 'date_added' not in task:
                    task['date_added'] = "Unknown"
                if 'date_completed' not in task:
                    task['date_completed'] = None

    def save_tasks(self):
        with open('tasks.json', 'w') as file:
            json.dump(self.tasks, file)

    def add_task(self):
        task = self.new_task_entry.get()
        if task:
            self.tasks.append({"task": task, "completed": False, "comment": "", "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "date_completed": None})
            self.new_task_entry.delete(0, tk.END)
            self.save_tasks()
            self.load_tasks_into_listboxes()
        else:
            messagebox.showwarning("Input Error", "Please enter a task.")

    def complete_task(self):
        selected_task_index = self.active_task_listbox.curselection()
        if selected_task_index:
            task_index = self.get_task_index_from_active(selected_task_index[0])
            self.tasks[task_index]["completed"] = True
            self.tasks[task_index]["date_completed"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.save_tasks()
            self.load_tasks_into_listboxes()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to complete.")

    def add_comment(self):
        if self.tab_control.index("current") == 0:
            selected_task_index = self.active_task_listbox.curselection()
            if selected_task_index:
                task_index = self.get_task_index_from_active(selected_task_index[0])
                comment = self.comment_entry.get("1.0", tk.END).strip()
                self.tasks[task_index]["comment"] = comment
                self.save_tasks()
                self.load_tasks_into_listboxes()
            else:
                messagebox.showwarning("Selection Error", "Please select a task to add a comment.")
        else:
            selected_task_index = self.completed_task_listbox.curselection()
            if selected_task_index:
                task_index = self.get_task_index_from_completed(selected_task_index[0])
                comment = self.completed_comment_entry.get("1.0", tk.END).strip()
                self.tasks[task_index]["comment"] = comment
                self.save_tasks()
                self.load_tasks_into_listboxes()
            else:
                messagebox.showwarning("Selection Error", "Please select a task to add a comment.")

    def move_to_active(self):
        selected_task_index = self.completed_task_listbox.curselection()
        if selected_task_index:
            task_index = self.get_task_index_from_completed(selected_task_index[0])
            self.tasks[task_index]["completed"] = False
            self.tasks[task_index]["date_completed"] = None
            self.save_tasks()
            self.load_tasks_into_listboxes()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to move to active.")

    def export_to_csv(self):
        completed_tasks = [task for task in self.tasks if task["completed"]]
        if completed_tasks:
            with open('completed_tasks.csv', 'w', newline='') as csvfile:
                fieldnames = ['task', 'comment', 'date_added', 'date_completed']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for task in completed_tasks:
                    writer.writerow({'task': task['task'], 'comment': task['comment'], 'date_added': task['date_added'], 'date_completed': task['date_completed']})
            messagebox.showinfo("Export Successful", "Completed tasks have been exported to completed_tasks.csv")
        else:
            messagebox.showwarning("No Completed Tasks", "There are no completed tasks to export.")

    def load_tasks_into_listboxes(self):
        self.active_task_listbox.delete(0, tk.END)
        self.completed_task_listbox.delete(0, tk.END)
        for i, task in enumerate(self.tasks):
            date_added = task.get('date_added', 'Unknown')
            task_display = f"{task['task']} (Added: {date_added})"
            if task["completed"]:
                date_completed = task.get('date_completed', 'Unknown')
                self.completed_task_listbox.insert(tk.END, f"{task_display} (Completed: {date_completed})")
            else:
                self.active_task_listbox.insert(tk.END, task_display)

        # Clear the comment fields
        self.comment_entry.delete("1.0", tk.END)
        self.completed_comment_entry.delete("1.0", tk.END)

    def display_comment(self, event):
        selected_task_index = event.widget.curselection()
        if selected_task_index:
            index = selected_task_index[0]
            task_index = self.get_task_index_from_listbox(event.widget, index)
            task = self.tasks[task_index]
            if event.widget == self.active_task_listbox:
                self.comment_entry.delete("1.0", tk.END)
                self.comment_entry.insert(tk.END, task["comment"])
            else:
                self.completed_comment_entry.delete("1.0", tk.END)
                self.completed_comment_entry.insert(tk.END, task["comment"])

    def get_task_index_from_listbox(self, listbox, listbox_index):
        if listbox == self.active_task_listbox:
            return self.get_task_index_from_active(listbox_index)
        else:
            return self.get_task_index_from_completed(listbox_index)

    def get_task_index_from_active(self, listbox_index):
        active_tasks = [i for i, task in enumerate(self.tasks) if not task["completed"]]
        return active_tasks[listbox_index]

    def get_task_index_from_completed(self, listbox_index):
        completed_tasks = [i for i, task in enumerate(self.tasks) if task["completed"]]
        return completed_tasks[listbox_index]

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskTracker(root)
    root.mainloop()
