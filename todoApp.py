import tkinter as tk
from tkinter import messagebox


def add_task():
    task = entry.get()
    if task:
        listbox.insert(tk.END, task)
        entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter a task.")


def delete_task():
    try:
        selected_index = listbox.curselection()[0]
        listbox.delete(selected_index)
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to delete.")


def mark_done():
    try:
        selected_index = listbox.curselection()[0]
        listbox.itemconfig(selected_index, bg="light green")
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to mark as done.")


def save_tasks():
    with open("tasks.txt", "w") as file:
        for i in range(listbox.size()):
            task = listbox.get(i)
            bg_color = listbox.itemcget(i, "bg")
            if bg_color == "light green":
                file.write(f"[COMPLETED]{task}\n")
            else:
                file.write(f"{task}\n")


def load_tasks():
    try:
        with open("tasks.txt", "r") as file:
            for line in file:
                task = line.strip()
                if task.startswith("[COMPLETED]"):
                    task = task[11:]  # Remove the "[COMPLETED]" prefix
                    index = listbox.size()  # Get current size before insertion
                    listbox.insert(tk.END, task)
                    listbox.itemconfig(index, bg="light green")  # Use valid index
                else:
                    listbox.insert(tk.END, task)
    except FileNotFoundError:
        pass


# Main window setup
root = tk.Tk()
root.title("To-Do List App")

# Entry frame for task input and add button
entry_frame = tk.Frame(root)
entry_frame.pack(pady=10)

entry = tk.Entry(entry_frame, width=40)
entry.pack(side=tk.LEFT, padx=5)

add_button = tk.Button(entry_frame, text="Add Task", command=add_task)
add_button.pack(side=tk.LEFT)

# Listbox with scrollbar
listbox_frame = tk.Frame(root)
listbox_frame.pack(pady=10)

scrollbar = tk.Scrollbar(listbox_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(listbox_frame, width=50, height=15, yscrollcommand=scrollbar.set)
listbox.pack(side=tk.LEFT)
scrollbar.config(command=listbox.yview)

# Buttons for delete and mark as done
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

delete_button = tk.Button(button_frame, text="Delete Task", command=delete_task)
delete_button.pack(side=tk.LEFT, padx=5)

mark_done_button = tk.Button(button_frame, text="Mark as Done", command=mark_done)
mark_done_button.pack(side=tk.LEFT, padx=5)

# Load tasks on startup
load_tasks()

# Save tasks on closing the window
root.protocol("WM_DELETE_WINDOW", lambda: [save_tasks(), root.destroy()])

root.mainloop()
