import json
from tld import is_tld

class Operations:
    def __init__(self) -> None:

        self.file_path = "Contacts/agenda.json"


    def is_empty(self, value, field):

        while value == "":
            value = input(f"No input provided. Enter new contact's {field}:")
        return value
    

    def check_exit(self, command):

        if command.lower() in ["no", "esc", "exit"]:
            print("Exiting the operation. Thank you!")
            return True
        return False

    
    def already_exist(self, agenda, first_name, last_name):
        if first_name in agenda["name"]["first name"]:
            indices = [i for i, name in enumerate(agenda["name"]["first name"]) if name == first_name]
            for index in indices:
                if agenda["name"]["last name"][index] == last_name:
                    mod = input(f"This contact (first name: {first_name}, last name: {last_name}) already exists. Would you like to update the contact? (Yes, No)")
                    if mod.lower() == "yes":
                        agenda = self.modify_contact(index, agenda)
                        with open(self.file_path, "w") as agenda_file:
                            json.dump(agenda, agenda_file, indent=4)
                        return True
        return False


    def view_contact(self, first_name, last_name, agenda):
        try:
            index = next(i for i, (fn, ln) in enumerate(zip(agenda['name']['first name'], agenda['name']['last name'])) if fn == first_name and ln == last_name)
        except StopIteration:
            print("Contact not found.")
            return
        
        for field in agenda.keys():
            if field == 'address':
                for position in agenda[field].keys():
                    if agenda[field][position][index] != "":
                        print(f"{position.capitalize()}: {agenda[field][position][index]}")
            elif field == 'name':
                print(f"First name: {agenda['name']['first name'][index]}")
                print(f"Last name: {agenda['name']['last name'][index]}")
            elif agenda[field][index] != "":
                print(f"{field.capitalize()}: {agenda[field][index]}")


    def modify_contact(self, index, agenda):
        for field in agenda.keys():
            edit_field = input(f"Would you like to edit {field}? (Yes, No):")
            if edit_field.lower() == 'yes':
                if field == 'name':
                    new_first_name = input(f"Enter new first name:")
                    if new_first_name == "":
                        new_first_name = self.is_empty(new_first_name, "first name") 
                    new_last_name = input(f"Enter new last name:")
                    new_first_name, new_last_name = self.is_name_valid(agenda, new_first_name, new_last_name)
                    if new_first_name and new_last_name:
                        agenda['name']['first name'][index] = new_first_name
                        agenda['name']['last name'][index] = new_last_name
                    else:
                        print(f"{field.capitalize()} editing interrupted!")
                elif field == 'phone':
                    new_value = input(f"Enter new phone number:")
                    new_value = self.is_phone_valid(agenda, new_value)
                    if new_value:
                        agenda[field][index] = new_value
                    else:
                        print(f"{field.capitalize()} editing interrupted!")
                elif field == 'email':
                    new_value = input(f"Enter new email address:")
                    new_value = self.is_email_valid(new_value)
                    if new_value:
                        agenda[field][index] = new_value
                    else:
                        print(f"{field.capitalize()} editing interrupted!")
                elif field == 'address':
                    for position in agenda[field].keys():
                        agenda[field][position][index] = input(f"Enter new {position}:")
                else:
                    agenda[field][index] = input(f"Enter new {field}:")
        return agenda
    
    
    def is_name_valid(self, file, first_name, last_name):
        while any(fn == first_name and ln == last_name for fn, ln in zip(file["name"]["first name"], file["name"]["last name"])):
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


    def is_phone_valid(self, file, val):

        while val in file["phone"] or val == "" or not all(v in '0123456789+-*#' for v in val):
            if val == "":
                val = self.is_empty(val, "phone") 
            elif val in file["phone"]:
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


    def add_and_check_info(self, file, field):
        value = input(f"Enter new contact's {field}:")
        if field == 'first name':
            first_name = value
            if first_name == "":
                first_name = self.is_empty(first_name, "first name") 
            last_name = input("Enter new contact's last name:")
            if self.already_exist(file, first_name, last_name):
                return None, None
            return self.is_name_valid(file, first_name, last_name)

        if field == 'phone':
            if value in file["phone"]:
                if self.already_exist(file, value, field):
                    return None
            return self.is_phone_valid(file, value)

        if field == 'email':
            return self.is_email_valid(value)

        return value

    def add_contact(self):
        
        # Take the json file in read option
        with open(self.file_path, "r") as agenda_file:
            agenda = json.load(agenda_file)

        """new_contact = {
            "first name": "",
            "last name": "",
            "phone": "",
            "email": "",
            "group": "",
            "address": {
                "street": "",
                "city": "",
                "state": ""
            },
            "note": ""
        }"""

        for field in agenda.keys():
            if field == 'name':
                first_name, last_name = self.add_and_check_info(agenda, "first name")
                if first_name is None or last_name is None:
                    return
                #new_contact["first name"] = first_name
                #new_contact["last name"] = last_name
                agenda["name"]["first name"].append(first_name)
                agenda["name"]["last name"].append(last_name)
            elif field == 'address':
                for position in agenda[field].keys():
                    #new_contact["address"][position] = self.add_and_check_info(agenda, position)
                    agenda["address"][position].append(self.add_and_check_info(agenda, position))
            else:
                value = self.add_and_check_info(agenda, field)
                if field in ["phone", "email"] and value is None:
                    return
                agenda[field].append(value)


        """agenda["name"]["first name"].append(new_contact["first name"])
        agenda["name"]["last name"].append(new_contact["last name"])
        agenda["phone"].append(new_contact["phone"])
        agenda["email"].append(new_contact["email"])
        agenda["group"].append(new_contact["group"])
        for key in new_contact["address"].keys():
            agenda["address"][key].append(new_contact["address"][key])
        agenda["note"].append(new_contact["note"])"""

        # Update the json file opening it in write option
        with open(self.file_path, "w") as agenda_file:
            json.dump(agenda, agenda_file, indent=4)


    def view_contacts(self):

        with open(self.file_path, "r") as file:
            agenda = json.load(file)

        #number_contacts = len(agenda['name']['first name'])
        names = sorted(zip(agenda['name']['first name'], agenda['name']['last name']), key=lambda x: (x[0].lower(), x[1].lower()))
        
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
                print("Name not present. Please enter a contact's name available:")
            else:
                print("=" * 30)
                self.view_contact(first_name, last_name, agenda)
                one_contact = input("Would you like to see another specific contact? (Yes, No):")
                print("=" * 30)
                if self.check_exit(one_contact):
                    return
            
    
    def edit_contacts(self):

        with open(self.file_path, "r") as agenda_file:
            agenda = json.load(agenda_file)

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
                index = next(i for i, (fn, ln) in enumerate(zip(agenda['name']['first name'], agenda['name']['last name'])) if fn == first_name and ln == last_name)
            except StopIteration:
                print("Name not present. Please enter a contact's name available.")
                continue

            agenda = self.modify_contact(index, agenda)
            with open(self.file_path, "w") as agenda_file:
                json.dump(agenda, agenda_file, indent=4)
            print("=" * 30)
            print("Modified contact:")
            self.view_contact(agenda['name']['first name'][index], agenda['name']['last name'][index], agenda)
            print("=" * 30)
            edit_answer = input("Would you like to edit another contact's details? (Yes, No):")
            if self.check_exit(edit_answer):
                return


    def deleting_contact(self):

        with open(self.file_path, "r") as agenda_file:
            agenda = json.load(agenda_file)

        first_name = input("Enter the first name of the contact you would like to delete:")
        if self.check_exit(first_name):
            print("Terminate deleting operation")
            return
        last_name = input("Enter the last name of the contact you would like to delete:")
        if self.check_exit(last_name):
            print("Terminate deleting operation")
            return

        try:
            index = next(i for i, (fn, ln) in enumerate(zip(agenda['name']['first name'], agenda['name']['last name'])) if fn == first_name and ln == last_name)
        except StopIteration:
            print("Name not present. Terminate deleting operation")
            return

        for field in list(agenda.keys()):
            if field == 'address':
                for position in list(agenda[field].keys()):
                    agenda[field][position].pop(index)
                continue
            if field == 'name':
                for fl_name in list(agenda[field].keys()):
                    agenda[field][fl_name].pop(index)

        print(f"Contact '{first_name} {last_name}' has been deleted.")
        with open(self.file_path, "w") as agenda_file:
            json.dump(agenda, agenda_file, indent=4)


    def search_contact(self):
        with open(self.file_path, "r") as agenda_file:
            agenda = json.load(agenda_file)

        first_name = input("Enter the first name of the contact you are searching for (or press Enter to skip):")
        if self.check_exit(first_name):
            print("Terminate search operation")
            return
        
        matching_fn = []
        if first_name:
            matching_fn = [i for i, fn in enumerate(agenda['name']['first name']) if fn == first_name]

        if not first_name or not matching_fn:
            last_name = input("Enter the last name of the contact you are searching for (or press Enter to skip):")
            if self.check_exit(last_name):
                print("Terminate search operation")
                return
            
            matching_ls = [i for i, ln in enumerate(agenda['name']['last name']) if ln == last_name]
            if not matching_ls:
                print("No contacts found with this specified last name.")
                return
            
            if len(matching_ls) > 1:
                print("Multiple contacts found with this last name:")
                for i in matching_ls:
                    print(f"First name: {agenda['name']['first name'][i]}, Last name: {agenda['name']['last name'][i]}")
                first_name = input("Enter the first name of the contact to refine your search:")
                if first_name == "":
                    first_name = self.is_empty(first_name, "first name") 
                if self.check_exit(first_name):
                    print("Terminate search operation")
                    return
                
                matching_fn = [i for i in matching_ls if agenda['name']['first name'][i] == first_name]
                if not matching_ls:
                    print("No contacts found with this specified first name.")
                    return
        else:
            if len(matching_fn) > 1:
                print("Multiple contacts found with this first name:")
                for i in matching_fn:
                    print(f"First name: {agenda['name']['first name'][i]}, Last name: {agenda['name']['last name'][i]}")
                last_name = input("Enter the last name of the contact to refine your search:")
                if last_name == "":
                    last_name = self.is_empty(last_name, "last name") 
                if self.check_exit(last_name):
                    print("Terminate search operation")
                    return

                matching_fn = [i for i in matching_fn if agenda['name']['last name'][i] == last_name]
                if not matching_fn:
                    print("No contacts found with the specified last name.")
                    return

        index = matching_fn[0]
        print("="*30)
        self.view_contact(agenda['name']['first name'][index], agenda['name']['last name'][index], agenda)
        print("="*30)