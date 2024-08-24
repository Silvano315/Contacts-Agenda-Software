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
        self.clear_widgets()
        self.create_add_contact_form()

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

        # Get data from entries
        first_name = self.entries['First Name'].get().strip()
        last_name = self.entries['Last Name'].get().strip()
        phone = self.entries['Phone'].get().strip()
        email = self.entries['Email'].get().strip()
        group = self.entries['Group'].get().strip()
        street = self.entries['Street'].get().strip()
        city = self.entries['City'].get().strip()
        state = self.entries['State'].get().strip()
        note = self.entries['Note'].get().strip()

        # Validation
        if not first_name:
            errors.append(('First Name', "First name is required"))
        if not phone:
            errors.append(('Phone', "Phone number is required"))
        if len(phone) > self.MAX_LENGTHS['phone']:
            errors.append(('Phone', f"Phone number cannot exceed {self.MAX_LENGTHS['phone']} characters"))
        if any(c not in self.VALID_PHONE_CHARS for c in phone):
            errors.append(('Phone', "Phone number contains invalid characters"))

        if len(first_name) > self.MAX_LENGTHS['first name']:
            errors.append(('First Name', f"First name cannot exceed {self.MAX_LENGTHS['first name']} characters"))
        if len(last_name) > self.MAX_LENGTHS['last name']:
            errors.append(('Last Name', f"Last name cannot exceed {self.MAX_LENGTHS['last name']} characters"))
        if len(email) > self.MAX_LENGTHS['email']:
            errors.append(('Email', f"Email cannot exceed {self.MAX_LENGTHS['email']} characters"))
        if email and '@' not in email:
            errors.append(('Email', "Email must contain '@'"))
        if email and not self.validate_email_domain(email):
            errors.append(('Email', "Email domain is not valid"))
        if len(group) > self.MAX_LENGTHS['group']:
            errors.append(('Group', f"Group cannot exceed {self.MAX_LENGTHS['group']} characters"))
        if len(street) > self.MAX_LENGTHS['street']:
            errors.append(('Street', f"Street cannot exceed {self.MAX_LENGTHS['street']} characters"))
        if len(city) > self.MAX_LENGTHS['city']:
            errors.append(('City', f"City cannot exceed {self.MAX_LENGTHS['city']} characters"))
        if len(state) > self.MAX_LENGTHS['state']:
            errors.append(('State', f"State cannot exceed {self.MAX_LENGTHS['state']} characters"))
        if len(note) > self.MAX_LENGTHS['note']:
            errors.append(('Note', f"Note cannot exceed {self.MAX_LENGTHS['note']} characters"))

        # Display errors
        for field, error in errors:
            self.error_labels[field].config(text=error)

        if not errors:
            self.add_contact_data(first_name, last_name, phone, email, group, street, city, state, note)
            tk.messagebox.showinfo("Info", "Contact added successfully")
            self.reset_to_main_menu()

    def validate_email_domain(self, email):
        try:
            domain = email.split('@')[1]
            get_tld(f"http://{domain}", as_object=True)
            return True
        except:
            return False

    def add_contact_data(self, first_name, last_name, phone, email, group, street, city, state, note):
        self.data['name']['first name'].append(first_name)
        self.data['name']['last name'].append(last_name)
        self.data['phone'].append(phone)
        self.data['email'].append(email)
        self.data['group'].append(group)
        self.data['address']['street'].append(street)
        self.data['address']['city'].append(city)
        self.data['address']['state'].append(state)
        self.data['note'].append(note)

    def reset_to_main_menu(self):
        self.clear_widgets()
        self.create_widgets()

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def view_contacts(self):
        tk.messagebox.showinfo("Info", "View Contacts clicked")
        # TO DO 

    def edit_contact(self):
        tk.messagebox.showinfo("Info", "Edit Contact clicked")
        # TO DO 

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