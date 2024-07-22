import json
import os
from tld import is_tld

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
        
        return phone_agenda


    def load_contacts(self):
        try:
            with open(self.file_path, "r") as agenda_file:
                return json.load(agenda_file)
        except FileNotFoundError:
            print("Contacts file not found! Starting with an empty agenda.")
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
        while any(fn == first_name and ln == last_name for fn, ln in zip(temp_agenda["name"]["first name"], temp_agenda["name"]["last name"])):
            #print("Contact with this first name and last name already exists.")
            first_name = input("Enter new contact's first name or Esc for stopping operation:")
            if first_name == "":
                first_name = self.is_empty(first_name, "first name") 
            if self.check_exit(first_name):
                return None, None
            last_name = input("Enter new contact's last name or Esc for stopping operation:")
            #if last_name == "":
                #last_name = self.is_empty(last_name, "last name") 
            if self.check_exit(last_name):
                return None, None
        return first_name, last_name


    def is_phone_valid(self, val, temp_agenda):
        while val in temp_agenda["phone"] or val == "" or not all(v in '0123456789+-*#' for v in val):
            if val == "":
                val = self.is_empty(val, "phone") 
            elif val in temp_agenda["phone"]:
                val = input("Enter new contact's phone or Esc for stopping operation:")
                if self.check_exit(val):
                    return None
            else:
                val = input("Enter a new correct contact's phone with '0123456789+-*#':") 
                if self.check_exit(val):
                    return None               
        return val


    def is_email_valid(self, val):
        while (len(val.split("@")) != 2 or not is_tld(val.split(".")[-1])) and val != "":
            val = input(f"Enter new contact's email with only one @ and appropriate TLD domain:")
            if self.check_exit(val):
                return None
        return val

    
    def already_exist(self, value, field, last_name = None):
        if field == 'name':
            if value in self.agenda[field]["first name"]:
                indices = [i for i, name in enumerate(self.agenda[field]["first name"]) if name == value]
                for index in indices:
                    if self.agenda[field]["last name"][index] == last_name:
                        mod = input(f"This contact (first name: {value}, last name: {last_name}) already exists. Would you like to update the contact? (Yes, No)")
                        if mod.lower() == "yes":
                            self.agenda = self.modify_contact(index)
                            self.save_contacts()
                            return True
        elif field == 'phone':
            if value in self.agenda[field]:
                mod = input(f"This phone number ({value}) already exists. Would you like to update the contact? (Yes, No)")
                if mod.lower() == "yes":
                    index = self.agenda[field].index(value)
                    self.agenda = self.modify_contact(index)
                    self.save_contacts()
                    return True
        return False
    

    def add_and_check_info(self, field, temp_agenda):
        value = input(f"Enter new contact's {field}:")
        if field == 'first name':
            first_name = value
            if first_name == "":
                first_name = self.is_empty(first_name, "first name") 
            if self.check_exit(first_name):
                return None, None
            last_name = input("Enter new contact's last name:")
            if self.check_exit(last_name):
                return None, None
            if self.check_exit(first_name):
                return None, None
            if self.already_exist(first_name, "name", last_name):
                return None, None
            return self.is_name_valid(first_name, last_name, temp_agenda)

        if field == 'phone':
            if value in temp_agenda["phone"]:
                if self.already_exist(value, field):
                    return None
            return self.is_phone_valid(value, temp_agenda)

        if field == 'email':
            return self.is_email_valid(value)

        return value


    def view_contact(self, first_name, last_name):
        try:
            index = next(i for i, (fn, ln) in enumerate(zip(self.agenda['name']['first name'], self.agenda['name']['last name'])) if fn == first_name and ln == last_name)
        except StopIteration:
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
        for field in temp_agenda.keys():
            edit_field = input(f"Would you like to edit {field}? (Yes, No):")
            if edit_field.lower() == 'yes':
                if field == 'name':
                    new_first_name = input(f"Enter new first name:")
                    if new_first_name == "":
                        new_first_name = self.is_empty(new_first_name, "first name") 
                    new_last_name = input(f"Enter new last name:")
                    new_first_name, new_last_name = self.is_name_valid(new_first_name, new_last_name, temp_agenda)
                    if new_first_name and new_last_name:
                        temp_agenda['name']['first name'][index] = new_first_name
                        temp_agenda['name']['last name'][index] = new_last_name
                    else:
                        print(f"{field.capitalize()} editing interrupted!")
                elif field == 'phone':
                    new_value = input(f"Enter new phone number:")
                    new_value = self.is_phone_valid(new_value, temp_agenda)
                    if new_value:
                        temp_agenda[field][index] = new_value
                    else:
                        print(f"{field.capitalize()} editing interrupted!")
                elif field == 'email':
                    new_value = input(f"Enter new email address:")
                    new_value = self.is_email_valid(new_value)
                    if new_value:
                        temp_agenda[field][index] = new_value
                    else:
                        print(f"{field.capitalize()} editing interrupted!")
                elif field == 'address':
                    for position in temp_agenda[field].keys():
                        temp_agenda[field][position][index] = input(f"Enter new {position}:")
                else:
                    temp_agenda[field][index] = input(f"Enter new {field}:")
        self.agenda = temp_agenda
        self.save_contacts()
        return self.agenda
    
    
    

    def add_contact(self):
        temp_agenda = self.load_contacts()
        for field in temp_agenda.keys():
            if field == 'name':
                first_name, last_name = self.add_and_check_info("first name", temp_agenda)
                if first_name is None or last_name is None:
                    return
                temp_agenda["name"]["first name"].append(first_name)
                temp_agenda["name"]["last name"].append(last_name)
            elif field == 'address':
                for position in temp_agenda[field].keys():
                    temp_agenda["address"][position].append(self.add_and_check_info(position, temp_agenda))
            else:
                value = self.add_and_check_info(field, temp_agenda)
                if field in ["phone", "email"] and value is None:
                    return
                temp_agenda[field].append(value)
        
        self.agenda = temp_agenda
        self.save_contacts()
        print("Contact added successfully.")


    def view_contacts(self):
        names = sorted(zip(self.agenda['name']['first name'], self.agenda['name']['last name']), key=lambda x: (x[0].lower(), x[1].lower()))
        
        for i, (first_name, last_name) in enumerate(names):
            print(f"Contact {i + 1}: {first_name} {last_name}")

        one_contact = input("Would you like to see all information about a specific contact? (Yes, No):")
        while one_contact.lower() == "yes":
            first_name = input("Enter the first name of the contact you would like to check information about:")
            if self.check_exit(first_name):
                print("=" * 30)
                return
            last_name = input("Enter the last name of the contact you would like to check information about:")
            if self.check_exit(last_name):
                print("=" * 30)
                return
            if (first_name, last_name) not in names:
                print("="*30)
                print("Name not present. Please enter a contact's name available:")
            else:
                print("=" * 30)
                self.view_contact(first_name, last_name)
                print("=" * 30)
                one_contact = input("Would you like to see another specific contact? (Yes, No):")
                if self.check_exit(one_contact):
                    return
            
    
    def edit_contacts(self):
        self.agenda = self.load_contacts()
        edit_answer = input("Would you like to edit contact's details? (Yes, No):")
        if self.check_exit(edit_answer):
            return

        while edit_answer.lower() == "yes":
            first_name = input("Enter the first name of the contact you would like to edit details:")
            if self.check_exit(first_name):
                return
            last_name = input("Enter the last name of the contact you would like to edit details:")
            if self.check_exit(last_name):
                return

            try:
                index = next(i for i, (fn, ln) in enumerate(zip(self.agenda['name']['first name'], self.agenda['name']['last name'])) if fn == first_name and ln == last_name)
            except StopIteration:
                print("Name not present. Please enter a contact's name available.")
                continue

            self.agenda = self.modify_contact(index)
            #self.save_contacts()

            print("=" * 30)
            print("Modified contact:")
            self.view_contact(self.agenda['name']['first name'][index], self.agenda['name']['last name'][index])
            print("=" * 30)
            edit_answer = input("Would you like to edit another contact's details? (Yes, No):")
            if self.check_exit(edit_answer):
                return


    def deleting_contact(self):
        self.agenda = self.load_contacts()
        first_name = input("Enter the first name of the contact you would like to delete:")
        if self.check_exit(first_name):
            print("Terminate deleting operation")
            return
        last_name = input("Enter the last name of the contact you would like to delete:")
        if self.check_exit(last_name):
            print("Terminate deleting operation")
            return

        try:
            index = next(i for i, (fn, ln) in enumerate(zip(self.agenda['name']['first name'], self.agenda['name']['last name'])) if fn == first_name and ln == last_name)
        except StopIteration:
            print("Name not present. Terminate deleting operation")
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
        self.save_contacts()


    def search_contact(self):
        first_name = input("Enter the first name of the contact you are searching for (or press Enter to skip):")
        if self.check_exit(first_name):
            print("Terminate search operation")
            return
        
        matching_fn = []
        if first_name:
            matching_fn = [i for i, fn in enumerate(self.agenda['name']['first name']) if fn == first_name]

        if not first_name or not matching_fn:
            last_name = input("Enter the last name of the contact you are searching for (or press Enter to skip):")
            if self.check_exit(last_name):
                print("Terminate search operation")
                return
            
            matching_ls = [i for i, ln in enumerate(self.agenda['name']['last name']) if ln == last_name]
            if not matching_ls:
                print("No contacts found with this specified last name.")
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
                    return
                
                matching_fn = [i for i in matching_ls if self.agenda['name']['first name'][i] == first_name]
                if not matching_fn:
                    print("No contacts found with this specified first name.")
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
                    return

                matching_fn = [i for i in matching_fn if self.agenda['name']['last name'][i] == last_name]
                if not matching_fn:
                    print("No contacts found with the specified last name.")
                    return

        index = matching_fn[0]
        print("="*30)
        self.view_contact(self.agenda['name']['first name'][index], self.agenda['name']['last name'][index])
        print("="*30)