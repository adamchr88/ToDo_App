# todo_gui.py
# Full working To-Do GUI app (Tkinter) + file saving to todos.txt
# Features: clock, add, click-to-load, edit, complete, exit, auto-create todos.txt

import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import time

FILEPATH = Path(__file__).with_name("todos.txt")


def ensure_file():
    if not FILEPATH.exists():
        FILEPATH.write_text("", encoding="utf-8")


def load_todos():
    ensure_file()
    return FILEPATH.read_text(encoding="utf-8").splitlines()  # returns list without "\n"


def save_todos(todos):
    ensure_file()
    FILEPATH.write_text("\n".join(todos) + ("\n" if todos else ""), encoding="utf-8")


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do App")

        self.todos = load_todos()

        # Clock
        self.clock_label = tk.Label(root, font=("Helvetica", 12))
        self.clock_label.pack(anchor="w", padx=10, pady=(10, 0))

        # Label
        tk.Label(root, text="Type in a to-do:", font=("Helvetica", 14)).pack(
            anchor="w", padx=10, pady=(10, 0)
        )

        # Input + Add
        entry_row = tk.Frame(root)
        entry_row.pack(fill="x", padx=10, pady=8)

        self.entry = tk.Entry(entry_row, font=("Helvetica", 14))
        self.entry.pack(side="left", fill="x", expand=True)

        tk.Button(entry_row, text="Add", width=10, command=self.add_todo).pack(
            side="left", padx=(10, 0)
        )

        # Listbox + Scrollbar + Buttons
        mid = tk.Frame(root)
        mid.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.listbox = tk.Listbox(mid, font=("Helvetica", 14), height=10)
        self.listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(mid, command=self.listbox.yview)
        scrollbar.pack(side="left", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        btn_col = tk.Frame(mid)
        btn_col.pack(side="left", fill="y", padx=(10, 0))

        tk.Button(btn_col, text="Edit", width=10, command=self.edit_todo).pack(
            pady=(0, 10)
        )
        tk.Button(btn_col, text="Complete", width=10, command=self.complete_todo).pack()

        # Exit
        bottom = tk.Frame(root)
        bottom.pack(fill="x", padx=10, pady=(0, 10))

        tk.Button(bottom, text="Exit", width=10, command=root.destroy).pack(side="right")

        # Events
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        self.entry.bind("<Return>", self.on_enter)

        self.refresh_list()
        self.tick_clock()

    def tick_clock(self):
        self.clock_label.config(text=time.strftime("%d-%m-%y %H:%M:%S"))
        self.root.after(200, self.tick_clock)

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for item in self.todos:
            self.listbox.insert(tk.END, item)

    def on_select(self, _event=None):
        sel = self.listbox.curselection()
        if not sel:
            return
        selected_text = self.listbox.get(sel[0])
        self.entry.delete(0, tk.END)
        self.entry.insert(0, selected_text)

    def on_enter(self, _event=None):
        # Pressing Enter adds the todo
        self.add_todo()

    def add_todo(self):
        text = self.entry.get().strip()
        if text == "":
            return

        self.todos.append(text)
        save_todos(self.todos)
        self.refresh_list()
        self.entry.delete(0, tk.END)

    def edit_todo(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Edit", "Select an item first.")
            return

        new_text = self.entry.get().strip()
        if new_text == "":
            messagebox.showinfo("Edit", "Type the new text first.")
            return

        index = sel[0]
        self.todos[index] = new_text
        save_todos(self.todos)
        self.refresh_list()
        self.entry.delete(0, tk.END)

    def complete_todo(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Complete", "Select an item first.")
            return

        index = sel[0]
        self.todos.pop(index)
        save_todos(self.todos)
        self.refresh_list()
        self.entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x450")
    app = TodoApp(root)
    root.mainloop()
