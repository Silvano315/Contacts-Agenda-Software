import json
from tld import is_tld

class Operations:
    def __init__(self) -> None:

        """Initialize the Operations class with the file path to the contacts agenda."""

        self.file_path = "Contacts/agenda.json"


    def is_empy(self, value, field):

        """
        Prompt the user to enter a value if the given value is empty.

        Args:
            value (str): The initial value.
            field (str): The field name to prompt for.

        Returns:
            str: The non-empty value entered by the user.
        """  

        while value == "":
            value = input(f"No input provided. Enter new contact's {field}:")
        return value
    

    def check_exit(self, command):

        """
        Check if the command is a request to exit the operation.

        Args:
            command (str): The command entered by the user.

        Returns:
            bool: True if the command is an exit request, False otherwise.
        """

        if command.lower() in ["no", "esc", "exit"]:
            print("Exiting the operation. Thank you!")
            return True
        return False

    
    def already_exist(self, agenda, value, field):

        """
        Prompt the user to update an existing contact if it already exists.

        Args:
            file (dict): The contacts file.
            value (str): The value to check.
            field (str): The field name to check.

        Returns:
            bool: True if the user chose to update the contact, False otherwise.
        """
        
        mod = input(f"This {field} already exists, would you like to update the contact? (Yes, No)")
        if mod.lower() == "yes":
            index = agenda[field].index(value)
            agenda = self.modify_contact(index, agenda)
            with open(self.file_path, "w") as agenda_file:
                json.dump(agenda, agenda_file, indent=4)
            return True
        return False 


    def view_contact(self,contact_name, agenda):

        """
        Display information about a specific contact.

        Args:
            contact_name (str): The name of the contact to view.
            agenda (dict): The contacts file.
        """

        index = agenda['name'].index(contact_name)
        for field in list(agenda.keys()):
            if field == 'address':
                for position in list(agenda[field].keys()):
                    if agenda[field][position][index] != "":
                        print(f"{position}: {agenda[field][position][index]}")
                continue
            if agenda[field][index] != "":
                print(f"{field}: {agenda[field][index]}")


    def modify_contact(self, index, agenda):

        """
        Modify the details of an existing contact.

        Args:
            index (int): The index of the contact to modify.
            agenda (dict): The contacts file.

        Returns:
            dict: The updated contacts file.
        """

        for field in list(agenda.keys()):
            edit_field = input(f"Would you like to edit {field}?")
            if edit_field.lower() == 'yes':
                if field == 'name':
                    new_value = input(f"Enter {field}")
                    new_value = self.is_name_valid(agenda, new_value)
                    if new_value:
                        agenda[field][index] = new_value
                    else:
                        print(f"{field.capitalize()} editing interruped!")
                    continue
                if field == 'phone':
                    new_value = input(f"Enter {field}")
                    new_value = self.is_phone_valid(agenda, new_value)
                    if new_value:
                        agenda[field][index] = new_value
                    else:
                        print(f"{field.capitalize()} editing interruped!")
                    continue
                if field == 'email':
                    new_value = input(f"Enter {field}:")
                    new_value = self.is_email_valid(new_value)
                    if new_value:
                        agenda[field][index] = new_value
                    else:
                        print(f"{field.capitalize()} editing interruped!")
                    continue
                if field == 'address':
                    for position in list(agenda[field].keys()):
                        agenda[field][position][index] = input(f"Enter {position}:")
                    continue
                agenda[field][index] = input(f"Enter {field}")
            else:
                continue
        return agenda
    
    
    def is_name_valid(self, file, val):

        """
        Validate a phone number and ensure it is unique and correctly formatted.

        Args:
            file (dict): The contacts file.
            val (str): The phone number to validate.

        Returns:
            str or None: The validated phone number or None if the operation was exited.
        """

        while val in file["name"] or val == "":
            if val == "":
                val = self.is_empy(val, "name") 
            else:
                val = input("Enter new contact's name or Esc for stopping operation:")
                if self.check_exit(val):
                    return None
        return val


    def is_phone_valid(self, file, val):

        """
        Validate a contact name and ensure it is unique.

        Args:
            file (dict): The contacts file.
            val (str): The contact name to validate.

        Returns:
            str or None: The validated contact name or None if the operation was exited.
        """

        while val in file["phone"] or val == "" or not all(v in '0123456789+-*#' for v in val):
            if val == "":
                val = self.is_empy(val, "phone") 
            elif val in file["phone"]:
                val = input("Enter new contact's phone or Esc for stopping operation:")
                if self.check_exit(val):
                    return None
            else:
                val = input("Enter a new correct contact's phone with '0123456789+-*#':")                
        return val


    def is_email_valid(self, val):

        """
        Validate an email address.

        Args:
            val (str): The email address to validate.

        Returns:
            str or None: The validated email address or None if the operation was exited.
        """

        while (len(val.split("@")) != 2 or not is_tld(val.split(".")[-1])) and val != "":
            val = input(f"Enter new contact's email with only one @ and appropriate TLD domain:")
            if self.check_exit(val):
                return None
        return val


    # this function has the purpose to check validity of input information and return the correct value
    def add_and_check_info(self, file, field):

        """
        Check the validity of input information and return the correct value.

        Args:
            file (dict): The contacts file.
            field (str): The field name to check.

        Returns:
            str or None: The validated field value or None if the operation was exited.
        """

        value = input(f"Enter new contact's {field}:")
        # Check validity for name, checking also if client wants to modify an existing contact
        if field == 'name':
            if value in file[field]:
                if self.already_exist(file, value, field):
                    return None
            return self.is_name_valid(file, value)
            

        # Check validity for phone number, checking also if client wants to modify an existing contact
        if field == 'phone':
            if value in file[field]:
                if self.already_exist(file, value, field):
                    return None
            return self.is_phone_valid(file, value)

        # Check validity for email
        if field == 'email':
            return self.is_email_valid(value)
        
        return value

    def add_contact(self):

        """
        Add a new contact to the contacts file. This method opens the file, 
        iterates through each field to insert the correct value, and updates the file.
        """
        
        # Take the json file in read option
        with open(self.file_path, "r") as agenda_file:
            agenda = json.load(agenda_file)

        # Iteration and appending new contact with correct values
        for field in list(agenda.keys()):
            if field == 'address':
                for position in list(agenda[field].keys()):
                    agenda[field][position].append(self.add_and_check_info(agenda, position))
                continue
            value = self.add_and_check_info(agenda, field)
            if field in ["name", "phone"] and value is None:
                return
            agenda[field].append(value)

        # Update the json file opening it in write option
        with open(self.file_path, "w") as agenda_file:
            json.dump(agenda, agenda_file, indent=4)


    def view_contacts(self):

        """
        View all contacts and optionally view detailed information for specific contacts.
        """

        with open(self.file_path, "r") as file:
            agenda = json.load(file)

        number_contacts = len(agenda['name'])
        names = sorted(agenda['name'], key=str.lower)
        for i in range(number_contacts):
            print(f"Contact {i+1}: {names[i]}")

        one_contact = input("Would you like to see all information about a specific contact?")
        while one_contact.lower() == "yes":
            contact_name = input("Digit contact name you would like to check information:")
            if self.check_exit(one_contact):
                    print("="*30)
                    return
            while contact_name not in agenda['name']:
                contact_name = input("Name not present. Digit a contat's name available:")
                if self.check_exit(contact_name):
                    print("="*30)
                    return
            print("="*30)
            self.view_contact(contact_name, agenda)
            one_contact = input("Would you like to see another specific contact?")
            print("="*30)
            if self.check_exit(one_contact):
                return
            
    
    def edit_contacts(self):

        """
        Edit the details of existing contacts. This method allows the user to choose
        and update the details of specific contacts and updates the file.
        """

        with open(self.file_path, "r") as agenda_file:
            agenda = json.load(agenda_file)

        edit_answer = input("Would you like to edit contact's details?")
        if self.check_exit(edit_answer):
            return
        while edit_answer == "yes":
            contact_name = input("Digit contact name you would like to edit details:")
            if self.check_exit(contact_name):
                return
            while contact_name not in agenda['name']:
                contact_name = input("Name not present. Digit a contat's name available:")
                if self.check_exit(contact_name):
                    return
            index = agenda['name'].index(contact_name)
            agenda = self.modify_contact(index, agenda)
            print("="*30)
            print("Modified contact:")
            self.view_contact(agenda['name'][index], agenda)
            print("="*30)
            edit_answer = input("Would you like to edit another contact's details?")
            if self.check_exit(edit_answer):
                    return

        with open(self.file_path, "w") as agenda_file:
            json.dump(agenda, agenda_file, indent=4)