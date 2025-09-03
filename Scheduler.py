import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

DATA_FILE = 'routine_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(routines, f, indent=4)

def refresh_listbox():
    listbox.delete(0, tk.END)
    for idx, r in enumerate(routines, 1):
        status = '✅' if r['status'] == 'done' else '🕒'
        listbox.insert(tk.END, f"{idx}. [{status}] {r['time']} - {r['task']}")

def add_routine():
    time = simpledialog.askstring("Time", "Enter time (HH:MM):")
    task = simpledialog.askstring("Task", "Enter task description:")
    if time and task:
        routines.append({"time": time, "task": task, "status": "pending"})
        refresh_listbox()
        save_data()
    else:
        messagebox.showwarning("Input Needed", "Both time and task are required.")

def mark_done():
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        routines[index]['status'] = 'done'
        refresh_listbox()
        save_data()
    else:
        messagebox.showinfo("No Selection", "Please select a task to mark as done.")

def reset_status():
    for r in routines:
        r['status'] = 'pending'
    refresh_listbox()
    save_data()
    messagebox.showinfo("Reset", "All tasks set to 'pending'.")

def on_exit():
    save_data()
    root.destroy()

# ---------------- GUI Setup ----------------
routines = load_data()

root = tk.Tk()
root.title("Windows Routine Manager")
root.geometry("400x400")

listbox = tk.Listbox(root, font=("Segoe UI", 12))
listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="➕ Add", command=add_routine, width=10).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="✅ Done", command=mark_done, width=10).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="🔁 Reset", command=reset_status, width=10).grid(row=0, column=2, padx=5)

refresh_listbox()

root.protocol("WM_DELETE_WINDOW", on_exit)
root.mainloop()
