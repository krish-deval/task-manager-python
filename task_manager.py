import tkinter as tk
from tkinter import messagebox, ttk
import json, os
from datetime import datetime

root = tk.Tk()
root.title("Task Manager")
root.geometry("620x620")
root.config(bg="#f5f7fb")

tasks = []

# ---------- FILE ----------
def load_tasks():
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as f:
            tasks.extend(json.load(f))
            update_listbox()

def save_tasks():
    with open("tasks.json", "w") as f:
        json.dump(tasks, f)

# ---------- FUNCTIONS ----------
def add_task():
    title = title_entry.get()
    details = details_text.get("1.0", tk.END).strip()
    priority = priority_var.get()

    # NEW DATE FORMAT FROM DROPDOWN
    date = f"{year_var.get()}-{month_var.get()}-{day_var.get()}"
    time = time_entry.get()

    if title == "":
        messagebox.showwarning("Warning", "Title required")
        return

    task = {
        "title": title,
        "details": details,
        "priority": priority,
        "date": date,
        "time": time,
        "done": False
    }

    tasks.append(task)
    save_tasks()
    update_listbox()
    clear_inputs()

def update_listbox():
    listbox.delete(0, tk.END)

    for task in tasks:
        status = "✔" if task["done"] else "○"
        overdue = ""

        if not task["done"] and task["date"] and task["time"]:
            try:
                t_time = datetime.strptime(task["date"]+" "+task["time"], "%Y-%m-%d %H:%M")
                if datetime.now() > t_time:
                    overdue = " ⚠"
            except:
                pass

        text = f"{status} [{task['priority']}] {task['title']}{overdue}"
        listbox.insert(tk.END, text)

    update_dashboard()

def show_details(event):
    try:
        index = listbox.curselection()[0]
        task = tasks[index]
        messagebox.showinfo("Task Details",
                            f"Title: {task['title']}\n\n"
                            f"Details: {task['details']}\n\n"
                            f"Priority: {task['priority']}\n"
                            f"Date: {task['date']} {task['time']}")
    except:
        pass

def mark_done():
    try:
        index = listbox.curselection()[0]
        tasks[index]["done"] = True
        save_tasks()
        update_listbox()
    except:
        messagebox.showwarning("Warning", "Select a task")

def delete_task():
    try:
        index = listbox.curselection()[0]
        tasks.pop(index)
        save_tasks()
        update_listbox()
    except:
        messagebox.showwarning("Warning", "Select a task")

def clear_inputs():
    title_entry.delete(0, tk.END)
    details_text.delete("1.0", tk.END)
    time_entry.delete(0, tk.END)

    # RESET DATE DROPDOWNS
    day_var.set("01")
    month_var.set("01")
    year_var.set("2026")

# ---------- DASHBOARD ----------
def update_dashboard():
    total = len(tasks)
    done = sum(1 for t in tasks if t["done"])
    overdue = 0

    for t in tasks:
        if not t["done"] and t["date"] and t["time"]:
            try:
                t_time = datetime.strptime(t["date"]+" "+t["time"], "%Y-%m-%d %H:%M")
                if datetime.now() > t_time:
                    overdue += 1
            except:
                pass

    total_label.config(text=f"Total Tasks: {total}")
    done_label.config(text=f"Completed: {done}")
    overdue_label.config(text=f"Overdue: {overdue}")

# ---------- TABS ----------
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

task_tab = tk.Frame(notebook, bg="#f5f7fb")
dashboard_tab = tk.Frame(notebook, bg="#f5f7fb")

notebook.add(task_tab, text="Tasks")
notebook.add(dashboard_tab, text="Dashboard")

# ---------- TASK TAB ----------
tk.Label(task_tab, text="Add Task", font=("Arial", 16, "bold"),
         bg="#f5f7fb").pack(pady=10)

title_entry = tk.Entry(task_tab, width=40)
title_entry.pack(pady=5)

details_text = tk.Text(task_tab, width=40, height=4)
details_text.pack(pady=5)

priority_var = tk.StringVar(value="Low")
ttk.Combobox(task_tab, textvariable=priority_var,
             values=["Low", "Medium", "High"]).pack(pady=5)

# ---------- DATE DROPDOWN ----------
date_frame = tk.Frame(task_tab, bg="#f5f7fb")
date_frame.pack(pady=5)

day_var = tk.StringVar(value="01")
month_var = tk.StringVar(value="01")
year_var = tk.StringVar(value="2026")

days = [f"{i:02d}" for i in range(1, 32)]
months = [f"{i:02d}" for i in range(1, 13)]
years = [str(i) for i in range(2024, 2031)]

ttk.Combobox(date_frame, textvariable=day_var, values=days, width=5).grid(row=0, column=0, padx=2)
ttk.Combobox(date_frame, textvariable=month_var, values=months, width=5).grid(row=0, column=1, padx=2)
ttk.Combobox(date_frame, textvariable=year_var, values=years, width=7).grid(row=0, column=2, padx=2)

# ---------- TIME ----------
time_entry = tk.Entry(task_tab)
time_entry.insert(0, "HH:MM")
time_entry.pack(pady=5)

# ---------- BUTTONS ----------
btn_frame = tk.Frame(task_tab, bg="#f5f7fb")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add", bg="#4CAF50", fg="white",
          width=10, command=add_task).grid(row=0, column=0, padx=5)

tk.Button(btn_frame, text="Done", bg="#2196F3", fg="white",
          width=10, command=mark_done).grid(row=0, column=1, padx=5)

tk.Button(btn_frame, text="Delete", bg="#f44336", fg="white",
          width=10, command=delete_task).grid(row=0, column=2, padx=5)

# ---------- LISTBOX ----------
listbox = tk.Listbox(task_tab, width=60, height=12)
listbox.pack(pady=10)

listbox.bind("<Double-Button-1>", show_details)

# ---------- DASHBOARD ----------
total_label = tk.Label(dashboard_tab, font=("Arial", 14), bg="#f5f7fb")
total_label.pack(pady=10)

done_label = tk.Label(dashboard_tab, font=("Arial", 14), bg="#f5f7fb")
done_label.pack(pady=10)

overdue_label = tk.Label(dashboard_tab, font=("Arial", 14), bg="#f5f7fb")
overdue_label.pack(pady=10)

# ---------- START ----------
load_tasks()
root.mainloop()