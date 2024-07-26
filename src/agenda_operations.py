import json
import os
from tld import is_tld
from constants import MAX_LENGTHS
import logging


logging.basicConfig(
    filename = 'Logs/agenda_operations.log',
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s',
    datefmt = '%Y-%m-%d %H-%M-%S'
)

class Operations:
    def __init__(self) -> None:
        self.file_path = "Contacts/agenda.json"
        self.agenda = self.load_or_initialize_agenda()


    def menu(self):
        print("\nManage your phone agenda:")
        print("1. Add Contact")
        print("2. View Contact")
        print("3. Edit Contact")
        print("4. Delete Contact")
        print("5. Search Contact")
        print("6. Save Agenda")
        print("7. Load Agenda")
        print("8. Initialize Agenda")
        print("9. Exit")


    def load_or_initialize_agenda(self):
        if not os.path.exists("Contacts"):
            os.makedirs("Contacts", exist_ok=True)
        
        if not os.path.exists(self.file_path):
            return self.initialize_agenda()
        
        return self.load_contacts()
    

    def initialize_agenda(self):
        phone_agenda = {
            'name': {
                'first name': [],
                'last name': []
            },
            'phone': [],
            'email': [],
            'group': [],
            'address': {
                'street': [],
                'city': [],
                'state': []
            },
            'note': []
        }
        with open(self.file_path, 'w') as agenda_file:
            json.dump(phone_agenda, agenda_file, indent=4)
            print("Agenda has been created!!")
            logging.info('Initialized new agenda.')
        
        return phone_agenda
        

    def load_contacts(self):
        try:
            with open(self.file_path, "r") as agenda_file:
                logging.info("Loaded contacts from file: %s", self.file_path)
                return json.load(agenda_file)
        except FileNotFoundError:
            print("Contacts file not found! Starting with an empty agenda.")
            logging.warning("Contacts file not found: %s. Starting with an empty agenda.", self.file_path)
            return {
                "name": {
                    "first name": [], 
                    "last name": []
                    },
                "phone": [],
                "email": [],
                "group": [],
                "address": {
                    "street": [], 
                    "city": [], 
                    "state": []
                    },
                "note": []
            }


    def save_contacts(self):
        with open(self.file_path, "w") as agenda_file:
            json.dump(self.agenda, agenda_file, indent=4)
        print("Contacts saved successfully.")
        logging.info("Saved contacts to file.")


    def is_empty(self, value, field):
        while value == "":
            value = input(f"No input provided. Enter new contact's {field}:")
        return value
    

    def check_exit(self, command):
        if command.lower() in ["no", "esc", "exit"]:
            print("Exiting the operation. Thank you!")
            return True
        return False
    

    def is_name_valid(self, first_name, last_name, temp_agenda):
        if len(first_name) > MAX_LENGTHS['first_name']:
            print(f"First name cannot exceed {MAX_LENGTHS['first name']} characters.")
            logging.warning(f"First name excedeed MAX LENGTH: {MAX_LENGTHS['first_name']}")
            return None, None
        if len(last_name) > MAX_LENGTHS['last_name']:
            print(f"Last name cannot exceed {MAX_LENGTHS['last name']} characters.")
            logging.warning(f"Last name excedeed MAX LENGTH: {MAX_LENGTHS['last_name']}")
            return None, None
        while any(fn == first_name and ln == last_name for fn, ln in zip(temp_agenda["name"]["first name"], temp_agenda["name"]["last name"])):
            #print("Contact with this first name and last name already exists.")
            logging.warning(f"Duplicate contact name: {first_name} {last_name}.")
            first_name = input("Enter new contact's first name or Esc for stopping operation:")
            if first_name == "":
                first_name = self.is_empty(first_name, "first name") 
            if self.check_exit(first_name):
                logging.info("Operation stopped by the user.")
                return None, None
            last_name = input("Enter new contact's last name or Esc for stopping operation:")
            #if last_name == "":
                #last_name = self.is_empty(last_name, "last name") 
            if self.check_exit(last_name):
                logging.info("Operation stopped by the user.")
                return None, None
        logging.info(f"Validated contact name: {first_name} {last_name}.")
        return first_name, last_name


    def is_phone_valid(self, val, temp_agenda):
        if len(val) > MAX_LENGTHS['phone']:
            print(f"Phone number cannot exceed {MAX_LENGTHS['phone']} characters.")
            logging.warning(f"Phone number excedeed MAX LENGTH: {MAX_LENGTHS['phone']}")
            return None
        while val in temp_agenda["phone"] or val == "" or not all(v in '0123456789+-*#' for v in val):
            if val == "":
                val = self.is_empty(val, "phone") 
            elif val in temp_agenda["phone"]:
                logging.warning(f"Phone number '{val}' already exists. Prompting for a new number.")
                val = input("Enter new contact's phone or Esc for stopping operation:")
                if self.check_exit(val):
                    logging.info("Operation stopped by the user.")
                    return None
            else:
                logging.warning(f"Invalid phone number format: '{val}'. Prompting for a new number.")
                val = input("Enter a new correct contact's phone with '0123456789+-*#':") 
                if self.check_exit(val):
                    logging.info("Operation stopped by the user.")
                    return None    
        logging.info(f"Validated phone number: '{val}'.")           
        return val


    def is_email_valid(self, val):
        if len(val) > MAX_LENGTHS['email']:
            print(f"Email cannot exceed {MAX_LENGTHS['email']} characters.")
            logging.warning(f"Email address excedeed MAX LENGTH: {MAX_LENGTHS['email']}")
            return None
        while (len(val.split("@")) != 2 or not is_tld(val.split(".")[-1])) and val != "":
            logging.warning(f"Invalid email format: '{val}'. Prompting for a new email.")
            val = input(f"Enter new contact's email with only one @ and appropriate TLD domain:")
            if self.check_exit(val):
                logging.info("Operation stopped by the user.")
                return None
        logging.info(f"Validated email: '{val}'.")
        return val

    
    def already_exist(self, value, field, last_name = None):
        if field == 'name':
            if value in self.agenda[field]["first name"]:
                indices = [i for i, name in enumerate(self.agenda[field]["first name"]) if name == value]
                for index in indices:
                    if self.agenda[field]["last name"][index] == last_name:
                        logging.info(f"Contact already exists with first name: '{value}' and last name: '{last_name}'.")
                        mod = input(f"This contact (first name: {value}, last name: {last_name}) already exists. Would you like to update the contact? (Yes, No)")
                        if mod.lower() == "yes":
                            self.agenda = self.modify_contact(index)
                            self.save_contacts()
                            logging.info(f"Contact updated: first name: '{value}', last name: '{last_name}'.")
                            return True
                        else:
                            logging.info(f"Contact update declined: first name: '{value}', last name: '{last_name}'.")
        elif field == 'phone':
            if value in self.agenda[field]:
                logging.info(f"Phone number already exists: '{value}'.")
                mod = input(f"This phone number ({value}) already exists. Would you like to update the contact? (Yes, No)")
                if mod.lower() == "yes":
                    index = self.agenda[field].index(value)
                    self.agenda = self.modify_contact(index)
                    self.save_contacts()
                    logging.info(f"Contact updated with phone number: '{value}'.")
                    return True
                else:
                    logging.info(f"Phone number update declined: '{value}'.")
        return False
    

    def add_and_check_info(self, field, temp_agenda):
        value = input(f"Enter new contact's {field}:")
        while len(value) > MAX_LENGTHS[field]:
             value = input(f"Enter new contact's {field} with correct length:")
             logging.warning(f"{field.capitalize()} excedeed MAX LENGTH: {MAX_LENGTHS[field]}")
             if self.check_exit(value):
                 if field == "first name" or field == "last name":
                     return None, None
                 else:
                     return None
        if field == 'first name':
            first_name = value
            if first_name == "":
                first_name = self.is_empty(first_name, "first name") 
            if self.check_exit(first_name):
                return None, None
            last_name = input("Enter new contact's last name:")
            while len(last_name) > MAX_LENGTHS["last name"]:
                value = input(f"Enter new contact's {field} with correct length:")
                logging.warning(f"{field.capitalize()} excedeed MAX LENGTH: {MAX_LENGTHS[field]}")
            if self.check_exit(last_name):
                return None, None
            if self.check_exit(first_name):
                return None, None
            if self.already_exist(first_name, "name", last_name):
                logging.info(f"Contact with first name '{first_name}' and last name '{last_name}' already exists.")
                return None, None
            return self.is_name_valid(first_name, last_name, temp_agenda)

        if field == 'phone':
            if value in temp_agenda["phone"]:
                logging.info(f"Phone number '{value}' already exists.")
                if self.already_exist(value, field):
                    return None
            return self.is_phone_valid(value, temp_agenda)

        if field == 'email':
            return self.is_email_valid(value)

        return value


    def view_contact(self, first_name, last_name):
        try:
            index = next(i for i, (fn, ln) in enumerate(zip(self.agenda['name']['first name'], self.agenda['name']['last name'])) if fn == first_name and ln == last_name)
            logging.info(f"Contact found: {first_name} {last_name} at index {index}")
        except StopIteration:
            logging.error(f"Contact not found: {first_name} {last_name}")
            print("Contact not found.")
            return
        
        for field in self.agenda.keys():
            if field == 'address':
                for position in self.agenda[field].keys():
                    if self.agenda[field][position][index] != "":
                        print(f"{position.capitalize()}: {self.agenda[field][position][index]}")
            elif field == 'name':
                print(f"First name: {self.agenda['name']['first name'][index]}")
                print(f"Last name: {self.agenda['name']['last name'][index]}")
            elif self.agenda[field][index] != "":
                print(f"{field.capitalize()}: {self.agenda[field][index]}")


    def modify_contact(self, index):
        temp_agenda = self.load_contacts()
        logging.info(f"Loaded contacts for modification. Editing contact at index {index}.")
        for field in temp_agenda.keys():
            edit_field = input(f"Would you like to edit {field}? (Yes, No):")
            if edit_field.lower() == 'yes':
                if field == 'name':
                    new_first_name = input(f"Enter new first name:")
                    while len(new_first_name) > MAX_LENGTHS["first name"]:
                        new_first_name = input("Enter new contact's first name with correct length:")
                        logging.warning(f"First name excedeed MAX LENGTH: {MAX_LENGTHS['first name']}")
                    if new_first_name == "":
                        new_first_name = self.is_empty(new_first_name, "first name") 
                    new_last_name = input(f"Enter new last name:")
                    while len(new_last_name) > MAX_LENGTHS["last name"]:
                        new_last_name = input("Enter new contact's last name with correct length:")
                        logging.warning(f"Last name excedeed MAX LENGTH: {MAX_LENGTHS['last name']}")
                    new_first_name, new_last_name = self.is_name_valid(new_first_name, new_last_name, temp_agenda)
                    if new_first_name and new_last_name:
                        temp_agenda['name']['first name'][index] = new_first_name
                        temp_agenda['name']['last name'][index] = new_last_name
                        logging.info(f"Updated {field} to First name: {new_first_name}, Last name: {new_last_name}")
                    else:
                        logging.warning(f"{field.capitalize()} editing interrupted!")
                        print(f"{field.capitalize()} editing interrupted!")
                elif field == 'phone':
                    new_value = input(f"Enter new phone number:")
                    while len(new_value) > MAX_LENGTHS["phone"]:
                        new_value = input("Enter new contact's phone with correct length:")
                        logging.warning(f"Phone number excedeed MAX LENGTH: {MAX_LENGTHS['phone']}")
                    new_value = self.is_phone_valid(new_value, temp_agenda)
                    if new_value:
                        temp_agenda[field][index] = new_value
                        logging.info(f"Updated {field} to {new_value}")
                    else:
                        logging.warning(f"{field.capitalize()} editing interrupted!")
                        print(f"{field.capitalize()} editing interrupted!")
                elif field == 'email':
                    new_value = input(f"Enter new email address:")
                    while len(new_value) > MAX_LENGTHS["email"]:
                        new_value = input("Enter new contact's email with correct length:")
                        logging.warning(f"Email address excedeed MAX LENGTH: {MAX_LENGTHS['email']}")
                    new_value = self.is_email_valid(new_value)
                    if new_value:
                        temp_agenda[field][index] = new_value
                        logging.info(f"Updated {field} to {new_value}")
                    else:
                        logging.warning(f"{field.capitalize()} editing interrupted!")
                        print(f"{field.capitalize()} editing interrupted!")
                elif field == 'address':
                    for position in temp_agenda[field].keys():
                        new_value = input(f"Enter new {position}:")
                        while len(new_value) > MAX_LENGTHS[position]:
                            new_value = input(f"Enter new {position} with correct length:")
                            logging.warning(f"{position.capitalize()} excedeed MAX LENGTH: {MAX_LENGTHS[position]}")
                        temp_agenda[field][position][index] = new_value
                        logging.info(f"Updated {field} - {position.capitalize()}: {temp_agenda[field][position][index]}")
                else:
                    new_value = input(f"Enter new {field}:")
                    while len(new_value) > MAX_LENGTHS[field]:
                            new_value = input(f"Enter new {field} with correct length:")
                            logging.warning(f"{field.capitalize()} excedeed MAX LENGTH: {MAX_LENGTHS[field]}")
                    temp_agenda[field][index] = new_value
                    logging.info(f"Updated {field} to {temp_agenda[field][index]}")
        self.agenda = temp_agenda
        self.save_contacts()
        logging.info(f"Contacts saved after modification at index {index}.")
        return self.agenda
    
    
    

    def add_contact(self):
        logging.info("Adding a new contact.")
        temp_agenda = self.load_contacts()
        for field in temp_agenda.keys():
            if field == 'name':
                first_name, last_name = self.add_and_check_info("first name", temp_agenda)
                if first_name is None or last_name is None:
                    logging.warning("Failed to add contact: invalid name.")
                    return
                temp_agenda["name"]["first name"].append(first_name)
                temp_agenda["name"]["last name"].append(last_name)
            elif field == 'address':
                for position in temp_agenda[field].keys():
                    temp_agenda["address"][position].append(self.add_and_check_info(position, temp_agenda))
            else:
                value = self.add_and_check_info(field, temp_agenda)
                if field in ["phone", "email"] and value is None:
                    logging.warning(f"Failed to add contact: invalid {field}.")
                    return
                temp_agenda[field].append(value)
        
        self.agenda = temp_agenda
        self.save_contacts()
        logging.info("Contact added successfully.")
        print("Contact added successfully.")


    def view_contacts(self):
        logging.info("Viewing all contacts.")
        names = sorted(zip(self.agenda['name']['first name'], self.agenda['name']['last name']), key=lambda x: (x[0].lower(), x[1].lower()))
        
        for i, (first_name, last_name) in enumerate(names):
            print(f"Contact {i + 1}: {first_name} {last_name}")

        one_contact = input("Would you like to see all information about a specific contact? (Yes, No):")
        if self.check_exit(one_contact):
            logging.info("View operation terminated by user.")
            return
        while one_contact.lower() == "yes":
            first_name = input("Enter the first name of the contact you would like to check information about:")
            if self.check_exit(first_name):
                logging.info("View operation terminated by user.")
                print("=" * 30)
                return
            last_name = input("Enter the last name of the contact you would like to check information about:")
            if self.check_exit(last_name):
                logging.info("View operation terminated by user.")
                print("=" * 30)
                return
            if (first_name, last_name) not in names:
                print("="*30)
                print("Name not present. Please enter a contact's name available:")
                logging.warning("Attempted to view non-existent contact: %s %s", first_name, last_name)
            else:
                logging.info("Viewing contact: %s %s", first_name, last_name)
                print("=" * 30)
                self.view_contact(first_name, last_name)
                print("=" * 30)
                one_contact = input("Would you like to see another specific contact? (Yes, No):")
                if self.check_exit(one_contact):
                    logging.info("View operation terminated by user.")
                    return
            """one_contact = input("Would you like to see another specific contact? (Yes, No):")
            if self.check_exit(one_contact):
                logging.info("View operation terminated by user.")
                return"""
                
        logging.info("Completed viewing contacts.")
            
    
    def edit_contacts(self):
        logging.info("Starting edit operation.")
        self.agenda = self.load_contacts()
        edit_answer = input("Would you like to edit contact's details? (Yes, No):")
        if self.check_exit(edit_answer):
            logging.info("Edit operation terminated by user.")
            return

        while edit_answer.lower() == "yes":
            first_name = input("Enter the first name of the contact you would like to edit details:")
            if self.check_exit(first_name):
                logging.info("Edit operation terminated by user.")
                return
            last_name = input("Enter the last name of the contact you would like to edit details:")
            if self.check_exit(last_name):
                logging.info("Edit operation terminated by user.")
                return

            try:
                index = next(i for i, (fn, ln) in enumerate(zip(self.agenda['name']['first name'], self.agenda['name']['last name'])) if fn == first_name and ln == last_name)
            except StopIteration:
                print("Name not present. Please enter a contact's name available.")
                logging.warning("Attempted to edit a non-existent contact: %s %s", first_name, last_name)
                continue
            
            logging.info("Editing contact: %s %s", first_name, last_name)
            self.agenda = self.modify_contact(index)
            #self.save_contacts()

            print("=" * 30)
            print("Modified contact:")
            self.view_contact(self.agenda['name']['first name'][index], self.agenda['name']['last name'][index])
            print("=" * 30)
            edit_answer = input("Would you like to edit another contact's details? (Yes, No):")
            if self.check_exit(edit_answer):
                logging.info("Edit operation terminated by user.")
                return
            logging.info("Edit operation completed.")


    def deleting_contact(self):
        logging.info("Starting deleting operation.")
        self.agenda = self.load_contacts()
        first_name = input("Enter the first name of the contact you would like to delete:")
        if self.check_exit(first_name):
            print("Terminate deleting operation")
            logging.info("Deleting operation terminated by user.")
            return
        last_name = input("Enter the last name of the contact you would like to delete:")
        if self.check_exit(last_name):
            print("Terminate deleting operation")
            logging.info("Deleting operation terminated by user.")
            return

        try:
            index = next(i for i, (fn, ln) in enumerate(zip(self.agenda['name']['first name'], self.agenda['name']['last name'])) if fn == first_name and ln == last_name)
        except StopIteration:
            print("Name not present. Terminate deleting operation")
            logging.warning("Attempted to delete a non-existent contact: %s %s", first_name, last_name)
            return

        for field in list(self.agenda.keys()):
            if field == 'address':
                for position in list(self.agenda[field].keys()):
                    self.agenda[field][position].pop(index)
                continue
            if field == 'name':
                for fl_name in list(self.agenda[field].keys()):
                    self.agenda[field][fl_name].pop(index)

        print(f"Contact '{first_name} {last_name}' has been deleted.")
        logging.info("Deleted contact: %s %s", first_name, last_name)
        self.save_contacts()


    def search_contact(self):
        logging.info("Starting search operation.")
        first_name = input("Enter the first name of the contact you are searching for (or press Enter to skip):")
        if self.check_exit(first_name):
            print("Terminate search operation")
            logging.info("Search operation terminated by user.")
            return
        
        matching_fn = []
        if first_name:
            matching_fn = [i for i, fn in enumerate(self.agenda['name']['first name']) if fn == first_name]

        if not first_name or not matching_fn:
            last_name = input("Enter the last name of the contact you are searching for (or press Enter to skip):")
            if self.check_exit(last_name):
                print("Terminate search operation")
                logging.info("Search operation terminated by user.")
                return
            
            matching_ls = [i for i, ln in enumerate(self.agenda['name']['last name']) if ln == last_name]
            if not matching_ls:
                print("No contacts found with this specified last name.")
                logging.info("No contacts found with last name: %s", last_name)
                return
            
            if len(matching_ls) > 1:
                print("Multiple contacts found with this last name:")
                for i in matching_ls:
                    print(f"First name: {self.agenda['name']['first name'][i]}, Last name: {self.agenda['name']['last name'][i]}")
                first_name = input("Enter the first name of the contact to refine your search:")
                if first_name == "":
                    first_name = self.is_empty(first_name, "first name") 
                if self.check_exit(first_name):
                    print("Terminate search operation")
                    logging.info("Search operation terminated by user.")
                    return
                
                matching_fn = [i for i in matching_ls if self.agenda['name']['first name'][i] == first_name]
                if not matching_fn:
                    print("No contacts found with this specified first name.")
                    logging.info("No contacts found with first name: %s", first_name)
                    return
        else:
            if len(matching_fn) > 1:
                print("Multiple contacts found with this first name:")
                for i in matching_fn:
                    print(f"First name: {self.agenda['name']['first name'][i]}, Last name: {self.agenda['name']['last name'][i]}")
                last_name = input("Enter the last name of the contact to refine your search:")
                if last_name == "":
                    last_name = self.is_empty(last_name, "last name") 
                if self.check_exit(last_name):
                    print("Terminate search operation")
                    logging.info("Search operation terminated by user.")
                    return

                matching_fn = [i for i in matching_fn if self.agenda['name']['last name'][i] == last_name]
                if not matching_fn:
                    print("No contacts found with the specified last name.")
                    logging.info("No contacts found with last name: %s", last_name)
                    return

        index = matching_fn[0]
        print("="*30)
        self.view_contact(self.agenda['name']['first name'][index], self.agenda['name']['last name'][index])
        logging.info("Viewed contact: %s %s", self.agenda['name']['first name'][index], self.agenda['name']['last name'][index])
        print("="*30)