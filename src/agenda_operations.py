import json
from tld import is_tld

class Operations:
    def __init__(self) -> None:
        self.file_path = "Contacts/agenda.json"

    # this function has the purpose to check validity of input information and return the correct value
    def add_and_check_info(self, file, field = None):

        """
        file: loaded json file as a dict
        field: key of the json file

        This function is used in add_contact() method to append a value to json file for each field. It checks
        some conditions for 'phone', 'name', 'email' field.
        """

        value = input(f"Enter new contact's {field}:")

        if field == 'phone':
            while not all(val in '0123456789+-*#' for val in value):
                value = input(f"Enter a new correct contact's {field} with '0123456789+-*#':")

        if field in ['name', 'phone'] and value in file[field]:
            mod = input("Name already exists, would you like to update the contact? (Yes, No)")
            if mod.lower() == "yes":
                # function to modify the contact having the field
                pass
            else:
                while value in file[field]:
                    value = input(f"Enter new contact's {field} or Esc for stopping operation:")
                    if value.lower() == 'esc':
                        # function to terminate operation (is it necessary?)
                        pass
        if field == 'email':
            while (len(value.split("@")) != 2 or not is_tld(value.split(".")[-1])) and value != "":
                value = input(f"Enter new contact's {field} with only one @ and appropriate TLD domain:")
                if value.lower() == 'esc':
                        # function to terminate operation (is it necessary?)
                        pass
        return value

    def add_contact(self):
        
        # Take the json file in read option
        with open(self.file_path, "r") as agenda_file:
            agenda = json.load(agenda_file)

        for field in list(agenda.keys()):
            if field == 'address':
                for position in list(agenda[field].keys()):
                    agenda[field][position].append(self.add_and_check_info(agenda, position))
                continue
            agenda[field].append(self.add_and_check_info(agenda, field))

        with open(self.file_path, "w") as agenda_file:
            json.dump(agenda, agenda_file, indent=4)