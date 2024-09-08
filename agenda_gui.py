import os
import json
import tkinter as tk
from tkinter import messagebox
from tld import get_tld

# Suppress Tkinter deprecation warnings
os.environ['TK_SILENCE_DEPRECATION'] = '1'

class AgendaGUI:
    MAX_LENGTHS = {
        'first name': 30,
        'last name': 30,
        'phone': 15,
        'email': 50,
        'group': 20,
        'street': 50,
        'city': 30,
        'state': 20,
        'note': 100
    }

    VALID_PHONE_CHARS = '0123456789+-*#'

    def __init__(self, root):
        self.root = root
        self.root.title("Phone Agenda")
        self.root.geometry("500x500")  # Increased size for better layout

        # Path to file JSON
        self.file_path = "Contacts/agenda_gui.json"

        # Data initialization
        self.data = {
            "name": {"first name": [], "last name": []},
            "phone": [],
            "email": [],
            "group": [],
            "address": {"street": [], "city": [], "state": []},
            "note": []
        }

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
        operations_menu.add_command(label="Add Contact", command=self.show_add_contact_form)
        operations_menu.add_command(label="View Contacts", command=self.view_contacts)
        operations_menu.add_command(label="Edit Contact", command=self.edit_contact)
        operations_menu.add_command(label="Delete Contact", command=self.delete_contact)
        operations_menu.add_command(label="Search Contact", command=self.search_contact)

        # Create Widgets
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Manage your Phone Agenda", font=('Arial', 16)).pack(pady=20)

        # Add Buttons
        tk.Button(self.root, text="Initialize Agenda", width=20, command=self.initialize_agenda).pack(pady=10)
        tk.Button(self.root, text="Load Agenda", width=20, command=self.load_agenda).pack(pady=10)
        tk.Button(self.root, text="Save Agenda", width=20, command=self.save_agenda).pack(pady=10)
        tk.Button(self.root, text="Add Contact", width=20, command=self.show_add_contact_form).pack(pady=10)
        tk.Button(self.root, text="View Contacts", width=20, command=self.view_contacts).pack(pady=10)
        tk.Button(self.root, text="Edit Contact", width=20, command=self.edit_contact).pack(pady=10)
        tk.Button(self.root, text="Delete Contact", width=20, command=self.delete_contact).pack(pady=10)
        tk.Button(self.root, text="Search Contact", width=20, command=self.search_contact).pack(pady=10)

    def initialize_agenda(self):
        self.data = {
            "name": {"first name": [], "last name": []},
            "phone": [],
            "email": [],
            "group": [],
            "address": {"street": [], "city": [], "state": []},
            "note": []
        }
        tk.messagebox.showinfo("Info", "Agenda Initialized")
        self.reset_to_main_menu() 

    def load_agenda(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                self.data = json.load(file)
                tk.messagebox.showinfo("Info", "Agenda Loaded Successfully")
        else:
            tk.messagebox.showwarning("Warning", "No file found to load")
        self.reset_to_main_menu()

    def save_agenda(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file, indent=4)
            tk.messagebox.showinfo("Info", "Agenda Saved Successfully")
        self.reset_to_main_menu() 


    def show_add_contact_form(self):
        # Clear existing widgets
        self.clear_widgets()

        # Create a new window for adding contacts
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Contact")
        add_window.geometry("500x600")

        # Create a frame for the form
        form_frame = tk.Frame(add_window)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Field labels and entries
        fields = [
            ('First Name', 'first name'), ('Last Name', 'last name'), 
            ('Phone', 'phone'), ('Email', 'email'), ('Group', 'group'),
            ('Street', 'street'), ('City', 'city'), ('State', 'state'), ('Note', 'note')
        ]
        self.entries = {}
        self.error_labels = {}

        for i, (label, field) in enumerate(fields):
            tk.Label(form_frame, text=label).grid(row=i, column=0, sticky='e', pady=5)
            entry = tk.Entry(form_frame, width=40)
            entry.grid(row=i, column=1, sticky='w', pady=5)
            self.entries[field] = entry

            error_label = tk.Label(form_frame, text="", fg="red")
            error_label.grid(row=i, column=2, sticky='w', pady=5)
            self.error_labels[field] = error_label

        # Add and Cancel Buttons
        tk.Button(form_frame, text="Add Contact", command=self.validate_and_add_contact).grid(row=len(fields), column=0, columnspan=2, pady=20)
        tk.Button(form_frame, text="Cancel", command=add_window.destroy).grid(row=len(fields), column=1, columnspan=2, pady=20)

    def create_add_contact_form(self):
        # Clear existing widgets
        self.clear_widgets()

        tk.Label(self.root, text="Add Contact", font=('Arial', 14)).grid(row=0, column=0, columnspan=2, pady=10)

        # Field labels, entries, and error messages
        fields = ['First Name', 'Last Name', 'Phone', 'Email', 'Group', 'Street', 'City', 'State', 'Note']
        self.entries = {}
        self.error_labels = {}

        for i, field in enumerate(fields):
            # Label for the field
            tk.Label(self.root, text=field).grid(row=i * 2 + 1, column=0, pady=5, padx=10, sticky='e')
            
            # Entry for the field
            entry = tk.Entry(self.root, width=50)
            entry.grid(row=i * 2 + 1, column=1, pady=5, padx=10)
            self.entries[field] = entry

            # Error label for the field
            error_label = tk.Label(self.root, text="", fg="red", wraplength=400)  # Wrap text to fit within the window
            error_label.grid(row=i * 2 + 2, column=1, pady=5, padx=10, sticky='w')
            self.error_labels[field] = error_label

        # Add and Back Buttons
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=len(fields) * 2 + 2, column=0, columnspan=2, pady=20)

        tk.Button(button_frame, text="Add", width=20, command=self.validate_and_add_contact).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Back", width=20, command=self.reset_to_main_menu).pack(side=tk.LEFT, padx=10)


    def validate_and_add_contact(self):
        errors = []
        contact_data = {}

        for field, entry in self.entries.items():
            value = entry.get().strip()
            contact_data[field] = value

            # Basic validation
            if field in ['first name', 'phone'] and not value:
                errors.append((field, f"{field.capitalize()} is required"))
            elif len(value) > self.MAX_LENGTHS.get(field, 100):
                errors.append((field, f"{field.capitalize()} cannot exceed {self.MAX_LENGTHS.get(field, 100)} characters"))

        # Specific validations
        if contact_data['phone'] and not all(c in self.VALID_PHONE_CHARS for c in contact_data['phone']):
            errors.append(('phone', "Phone number contains invalid characters"))
        
        if contact_data['email']:
            if '@' not in contact_data['email']:
                errors.append(('email', "Email must contain '@'"))
            elif not self.validate_email_domain(contact_data['email']):
                errors.append(('email', "Email domain is not valid"))

        # Clear previous error messages
        for error_label in self.error_labels.values():
            error_label.config(text="")

        # Display new error messages
        for field, error in errors:
            self.error_labels[field].config(text=error)

        if not errors:
            self.add_contact_data(**contact_data)
            tk.messagebox.showinfo("Success", "Contact added successfully")
            self.reset_to_main_menu()

    def validate_email_domain(self, email):
        try:
            domain = email.split('@')[1]
            get_tld(f"http://{domain}", as_object=True)
            return True
        except:
            return False

    def add_contact_data(self, **kwargs):
        for key, value in kwargs.items():
            if key in ['first name', 'last name']:
                self.data['name'][key].append(value)
            elif key in ['street', 'city', 'state']:
                self.data['address'][key].append(value)
            else:
                self.data[key].append(value)

    def reset_to_main_menu(self):
        self.clear_widgets()
        self.create_widgets()

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()


    # Function to display contact details
    def view_contacts(self):
        # Clear existing widgets
        self.clear_widgets()

        # Create a new window for viewing contacts
        view_window = tk.Toplevel(self.root)
        view_window.title("View Contacts")
        view_window.geometry("600x400")

        # Create a frame for the contact list
        list_frame = tk.Frame(view_window)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a listbox for contacts
        contact_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        contact_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configure the scrollbar
        scrollbar.config(command=contact_listbox.yview)

        # Populate the listbox with contacts
        names = sorted(zip(self.data['name']['first name'], self.data['name']['last name']), 
                    key=lambda x: (x[0].lower(), x[1].lower()))
        for first_name, last_name in names:
            contact_listbox.insert(tk.END, f"{first_name} {last_name}")

        # Function to display contact details
        def show_contact_details():
            selection = contact_listbox.curselection()
            if selection:
                index = selection[0]
                first_name, last_name = names[index]
                self.view_contact_details(first_name, last_name)

        # Create a button to view contact details
        view_button = tk.Button(view_window, text="View Details", command=show_contact_details)
        view_button.pack(pady=10)

        # Create a button to return to the main menu
        back_button = tk.Button(view_window, text="Back to Main Menu", command=self.reset_to_main_menu)
        back_button.pack(pady=10)

    def view_contact_details(self, first_name, last_name):
        # Create a new window for contact details
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Contact Details: {first_name} {last_name}")
        details_window.geometry("400x300")

        # Find the index of the contact
        index = self.data['name']['first name'].index(first_name)

        # Create labels for each piece of information
        tk.Label(details_window, text=f"Name: {first_name} {last_name}").pack(anchor='w', padx=10, pady=5)
        tk.Label(details_window, text=f"Phone: {self.data['phone'][index]}").pack(anchor='w', padx=10, pady=5)
        tk.Label(details_window, text=f"Email: {self.data['email'][index]}").pack(anchor='w', padx=10, pady=5)
        tk.Label(details_window, text=f"Group: {self.data['group'][index]}").pack(anchor='w', padx=10, pady=5)
        tk.Label(details_window, text=f"Address: {self.data['address']['street'][index]}, "
                                    f"{self.data['address']['city'][index]}, "
                                    f"{self.data['address']['state'][index]}").pack(anchor='w', padx=10, pady=5)
        tk.Label(details_window, text=f"Note: {self.data['note'][index]}").pack(anchor='w', padx=10, pady=5)

        # Create a button to close the details window
        tk.Button(details_window, text="Close", command=details_window.destroy).pack(pady=10)

    def edit_contact(self):
        # Clear existing widgets
        self.clear_widgets()

        # Create a new window for editing contacts
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Contact")
        edit_window.geometry("600x700")

        # Create a frame for the contact list
        list_frame = tk.Frame(edit_window)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a listbox for contacts
        contact_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        contact_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configure the scrollbar
        scrollbar.config(command=contact_listbox.yview)

        # Populate the listbox with contacts
        names = sorted(zip(self.data['name']['first name'], self.data['name']['last name']), 
                    key=lambda x: (x[0].lower(), x[1].lower()))
        for first_name, last_name in names:
            contact_listbox.insert(tk.END, f"{first_name} {last_name}")

        # Function to load contact details for editing
        def load_contact_for_edit():
            selection = contact_listbox.curselection()
            if selection:
                index = selection[0]
                first_name, last_name = names[index]
                self.show_edit_form(first_name, last_name)

        # Create a button to load contact for editing
        edit_button = tk.Button(edit_window, text="Edit Selected Contact", command=load_contact_for_edit)
        edit_button.pack(pady=10)

        # Create a button to return to the main menu
        back_button = tk.Button(edit_window, text="Back to Main Menu", command=self.reset_to_main_menu)
        back_button.pack(pady=10)

    def show_edit_form(self, first_name, last_name):
        # Create a new window for editing the contact
        edit_form = tk.Toplevel(self.root)
        edit_form.title(f"Edit Contact: {first_name} {last_name}")
        edit_form.geometry("500x600")

        # Create a frame for the form
        form_frame = tk.Frame(edit_form)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Find the index of the contact
        index = self.data['name']['first name'].index(first_name)

        # Field labels, entries, and current values
        fields = [
            ('First Name', 'first name', self.data['name']['first name'][index]),
            ('Last Name', 'last name', self.data['name']['last name'][index]),
            ('Phone', 'phone', self.data['phone'][index]),
            ('Email', 'email', self.data['email'][index]),
            ('Group', 'group', self.data['group'][index]),
            ('Street', 'street', self.data['address']['street'][index]),
            ('City', 'city', self.data['address']['city'][index]),
            ('State', 'state', self.data['address']['state'][index]),
            ('Note', 'note', self.data['note'][index])
        ]

        self.entries = {}
        self.error_labels = {}

        for i, (label, field, current_value) in enumerate(fields):
            tk.Label(form_frame, text=label).grid(row=i, column=0, sticky='e', pady=5)
            entry = tk.Entry(form_frame, width=40)
            entry.insert(0, current_value)
            entry.grid(row=i, column=1, sticky='w', pady=5)
            self.entries[field] = entry

            error_label = tk.Label(form_frame, text="", fg="red")
            error_label.grid(row=i, column=2, sticky='w', pady=5)
            self.error_labels[field] = error_label

        # Update and Cancel Buttons
        tk.Button(form_frame, text="Update Contact", command=lambda: self.validate_and_update_contact(index)).grid(row=len(fields), column=0, columnspan=2, pady=20)
        tk.Button(form_frame, text="Cancel", command=edit_form.destroy).grid(row=len(fields), column=1, columnspan=2, pady=20)

    def validate_and_update_contact(self, index):
        errors = []
        updated_data = {}

        for field, entry in self.entries.items():
            value = entry.get().strip()
            updated_data[field] = value

            # Basic validation
            if field in ['first name', 'phone'] and not value:
                errors.append((field, f"{field.capitalize()} is required"))
            elif len(value) > self.MAX_LENGTHS.get(field, 100):
                errors.append((field, f"{field.capitalize()} cannot exceed {self.MAX_LENGTHS.get(field, 100)} characters"))

        # Specific validations
        if updated_data['phone'] and not all(c in self.VALID_PHONE_CHARS for c in updated_data['phone']):
            errors.append(('phone', "Phone number contains invalid characters"))
        
        if updated_data['email']:
            if '@' not in updated_data['email']:
                errors.append(('email', "Email must contain '@'"))
            elif not self.validate_email_domain(updated_data['email']):
                errors.append(('email', "Email domain is not valid"))

        # Clear previous error messages
        for error_label in self.error_labels.values():
            error_label.config(text="")

        # Display new error messages
        for field, error in errors:
            self.error_labels[field].config(text=error)

        if not errors:
            self.update_contact_data(index, **updated_data)
            tk.messagebox.showinfo("Success", "Contact updated successfully")
            self.reset_to_main_menu()

    def update_contact_data(self, index, **kwargs):
        for key, value in kwargs.items():
            if key in ['first name', 'last name']:
                self.data['name'][key][index] = value
            elif key in ['street', 'city', 'state']:
                self.data['address'][key][index] = value
            else:
                self.data[key][index] = value

    def delete_contact(self):
        tk.messagebox.showinfo("Info", "Delete Contact clicked")
        # TO DO 

    def search_contact(self):
        tk.messagebox.showinfo("Info", "Search Contact clicked")
        # TO DO 

        
if __name__ == "__main__":
    root = tk.Tk()
    app = AgendaGUI(root)
    root.mainloop()