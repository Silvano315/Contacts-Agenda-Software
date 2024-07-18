import json

class Operations:
    def __init__(self) -> None:
        self.file_path = "Contacts/agenda.json"

    def add_info(self, file, field = None):

        value = input(f"Enter new contact's {field}:")

        if field == 'phone':
            while not all(val in '0123456789+-*#' for val in value):
                value = input(f"Enter a new correct contact's {field} with '0123456789+-*#':")

        if field in ['name', 'phone'] and value in file[field]:
            mod = input("Name already exists, would you like to update the contact? (Yes, No)")
            if mod.lower() == "yes":
                # function to modify the contact having the name
                pass
            else:
                while value in file[field]:
                    value = input(f"Enter new contact's {field} or Esc for stopping operation:")
                    if value.lower() == 'esc':
                        # function to terminate operation
                        pass
        return value

    def add_contact(self):
        
        # Take the json file in read option
        with open(self.file_path, "r") as agenda_file:
            agenda = json.load(agenda_file)

        for field in list(agenda.keys()):
            if field == 'address':
                for position in list(agenda[field].keys()):
                    agenda[field][position].append(self.add_info(agenda, position))
                continue
            agenda[field].append(self.add_info(agenda, field))

        with open(self.file_path, "w") as agenda_file:
            json.dump(agenda, agenda_file, indent=4)