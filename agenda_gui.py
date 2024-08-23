import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'

import tkinter as tk
from tkinter import messagebox


class AgendaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Phone Agenda")
        self.root.geometry("400x400")
        
        # Main Menu
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        
        # Menu File
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Agenda", command=self.load_agenda)
        file_menu.add_command(label="Save Agenda", command=self.save_agenda)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Menu Operations
        operations_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Operations", menu=operations_menu)
        operations_menu.add_command(label="Add Contact", command=self.add_contact)
        operations_menu.add_command(label="View Contacts", command=self.view_contacts)
        operations_menu.add_command(label="Edit Contact", command=self.edit_contact)
        operations_menu.add_command(label="Delete Contact", command=self.delete_contact)
        operations_menu.add_command(label="Search Contact", command=self.search_contact)
        
        # Operations buttons
        self.create_widgets()
    
    def create_widgets(self):
        tk.Label(self.root, text="Manage your Phone Agenda", font=('Arial', 16)).pack(pady=20)
        
        tk.Button(self.root, text="Add Contact", width=20, command=self.add_contact).pack(pady=10)
        tk.Button(self.root, text="View Contacts", width=20, command=self.view_contacts).pack(pady=10)
        tk.Button(self.root, text="Edit Contact", width=20, command=self.edit_contact).pack(pady=10)
        tk.Button(self.root, text="Delete Contact", width=20, command=self.delete_contact).pack(pady=10)
        tk.Button(self.root, text="Search Contact", width=20, command=self.search_contact).pack(pady=10)
    
    def load_agenda(self):
        messagebox.showinfo("Info", "Load Agenda clicked")
    
    def save_agenda(self):
        messagebox.showinfo("Info", "Save Agenda clicked")
    
    def add_contact(self):
        messagebox.showinfo("Info", "Add Contact clicked")
    
    def view_contacts(self):
        messagebox.showinfo("Info", "View Contacts clicked")
    
    def edit_contact(self):
        messagebox.showinfo("Info", "Edit Contact clicked")
    
    def delete_contact(self):
        messagebox.showinfo("Info", "Delete Contact clicked")
    
    def search_contact(self):
        messagebox.showinfo("Info", "Search Contact clicked")

if __name__ == "__main__":
    root = tk.Tk()
    app = AgendaGUI(root)
    root.mainloop()