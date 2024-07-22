import src.agenda_operations

def main():
    operations = src.agenda_operations.Operations()

    while True:
        operations.menu()
        client_choice = input("Select operation you need (1-9): ").strip()

        if client_choice == '1':
            operations.add_contact()
        elif client_choice == '2':
            operations.view_contacts()
        elif client_choice == '3':
            operations.edit_contacts()
        elif client_choice == '4':
            operations.deleting_contact()
        elif client_choice == '5':
            operations.search_contact()
        elif client_choice == '6':
            operations.save_contacts()
            #print("Agenda saved successfully.")
        elif client_choice == '7':
            operations.load_contacts()
            print("Agenda loaded successfully.")
        elif client_choice == '8':
            operations.agenda = operations.initialize_agenda()
            print("Agenda has been initialized.")
        elif client_choice == '9':
            print("Exiting the program. Thank you!")
            break
        else:
            print("Invalid option. Please select a number between 1 and 9.")

if __name__ == "__main__":
    main()