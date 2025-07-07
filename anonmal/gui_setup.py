import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, Listbox, END, Scrollbar, StringVar, BooleanVar
import json
import os

SETTINGS_DIR = os.path.join(os.path.dirname(__file__), '../settings')
CONTAINER_PATH = os.path.join(SETTINGS_DIR, 'container-settings.json')
TERMINAL_PATH = os.path.join(SETTINGS_DIR, 'terminal-settings.json')
VPN_PATH = os.path.join(SETTINGS_DIR, 'vpn-settings.json')

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def center_window(window, width, height):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_cordinate = int((screen_width / 2) - (width / 2))
    y_cordinate = int((screen_height / 2) - (height / 2))
    window.geometry("{}x{}+{}+{}".format(width, height, x_cordinate, y_cordinate))

class SettingsEditor:
    def __init__(self, master):
        self.master = master
        master.title("Anonmal Settings Editor")
        width, height = 650, 500
        center_window(master, width, height)

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill='both', expand=True)

        self.container_settings = load_json(CONTAINER_PATH)
        self.terminal_settings = load_json(TERMINAL_PATH)
        self.vpn_settings = load_json(VPN_PATH)

        self.container_tab = ttk.Frame(self.notebook)
        self.terminal_tab = ttk.Frame(self.notebook)
        self.vpn_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.container_tab, text="Container")
        self.notebook.add(self.terminal_tab, text="Terminal")
        self.notebook.add(self.vpn_tab, text="VPN")

        self.entries = {}

        self.build_tab(self.container_tab, self.container_settings, CONTAINER_PATH)
        self.build_tab(self.terminal_tab, self.terminal_settings, TERMINAL_PATH)
        self.build_tab(self.vpn_tab, self.vpn_settings, VPN_PATH)

    def build_tab(self, tab, settings, path):
        row = 0
        if tab not in self.entries:
            self.entries[tab] = {}

        for key, value in settings.items():
            label = tk.Label(tab, text=key, anchor='w')
            label.grid(row=row, column=0, sticky='w', padx=8, pady=4)

            if isinstance(value, bool):
                var = BooleanVar(value=value)
                entry = tk.Checkbutton(tab, variable=var)
                entry.var = var
            elif isinstance(value, list):
                entry = tk.Button(tab, text="Edit List", command=lambda k=key, p=path, t=tab: self.edit_list(tab, k, p, t))
                entry.var = value
            elif isinstance(value, dict):
                entry = tk.Button(tab, text="Edit Dict", command=lambda k=key, p=path, t=tab: self.edit_dict(tab, k, p, t))
                entry.var = value
            else:
                var = StringVar(value=str(value))
                entry = tk.Entry(tab, textvariable=var, width=40)
                entry.var = var

            entry.grid(row=row, column=1, sticky='w', padx=8, pady=4)
            self.entries[tab][key] = entry
            row += 1

        save_btn = tk.Button(tab, text="Save", command=lambda s=settings, p=path, t=tab: self.save_tab(s, p, t))
        save_btn.grid(row=row, column=0, columnspan=2, pady=10)

    def edit_list(self, parent, key, path, tab):
        settings = load_json(path)
        value = settings.get(key, [])
        win = tk.Toplevel(parent)
        win.title(f"Edit List: {key}")
        width, height = 400, 350
        center_window(win, width, height)

        listbox = Listbox(win, width=40, height=12)
        listbox.pack(pady=10)
        for item in value:
            listbox.insert(END, item)

        def add_item():
            item = simpledialog.askstring("Add Item", f"Add to {key}:", parent=win)
            if item:
                listbox.insert(END, item)

        def remove_item():
            sel = listbox.curselection()
            if sel:
                listbox.delete(sel[0])

        def save_list():
            new_list = [listbox.get(i) for i in range(listbox.size())]
            settings = load_json(path)
            settings[key] = new_list
            save_json(path, settings)
            if tab == self.container_tab:
                self.container_settings[key] = new_list
            elif tab == self.terminal_tab:
                self.terminal_settings[key] = new_list
            elif tab == self.vpn_tab:
                self.vpn_settings[key] = new_list
            messagebox.showinfo("Saved", f"List '{key}' saved.", parent=win)
            win.destroy()

        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Add", command=add_item).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Remove", command=remove_item).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Save", command=save_list).pack(side=tk.LEFT, padx=5)

    def edit_dict(self, parent, key, path, tab):
        settings = load_json(path)
        value = settings.get(key, {})
        win = tk.Toplevel(parent)
        win.title(f"Edit Dict: {key}")
        width, height = 400, 350
        center_window(win, width, height)

        entries = {}
        row = 0
        for k, v in value.items():
            tk.Label(win, text=k).grid(row=row, column=0, sticky='w', padx=8, pady=4)
            var = StringVar(value=str(v))
            entry = tk.Entry(win, textvariable=var, width=30)
            entry.grid(row=row, column=1, padx=8, pady=4)
            entries[k] = var
            row += 1

        def save_dict():
            new_dict = {k: v.get() for k, v in entries.items()}
            for k, v in new_dict.items():
                if isinstance(value[k], bool):
                    new_dict[k] = v.lower() == "true"
                else:
                    try:
                        new_dict[k] = int(v)
                    except ValueError:
                        try:
                            new_dict[k] = float(v)
                        except ValueError:
                            new_dict[k] = v
            settings = load_json(path)
            settings[key] = new_dict
            save_json(path, settings)
            if tab == self.container_tab:
                self.container_settings[key] = new_dict
            elif tab == self.terminal_tab:
                self.terminal_settings[key] = new_dict
            elif tab == self.vpn_tab:
                self.vpn_settings[key] = new_dict
            messagebox.showinfo("Saved", f"Dict '{key}' saved.", parent=win)
            win.destroy()

        tk.Button(win, text="Save", command=save_dict).grid(row=row, column=0, columnspan=2, pady=10)

    def save_tab(self, settings, path, tab):
        file_settings = load_json(path)
        for key, entry in self.entries[tab].items():
            if isinstance(entry, tk.Entry):
                val = entry.var.get()
                if val.lower() == "true":
                    val = True
                elif val.lower() == "false":
                    val = False
                else:
                    try:
                        val = int(val)
                    except ValueError:
                        try:
                            val = float(val)
                        except ValueError:
                            pass
                file_settings[key] = val
            elif isinstance(entry, tk.Checkbutton):
                file_settings[key] = entry.var.get()

        save_json(path, file_settings)

        if tab == self.container_tab:
            self.container_settings = file_settings
        elif tab == self.terminal_tab:
            self.terminal_settings = file_settings
        elif tab == self.vpn_tab:
            self.vpn_settings = file_settings
        messagebox.showinfo("Saved", "Settings saved!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SettingsEditor(root)
    root.mainloop()