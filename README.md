# Contacts Agenda Software with Python

## Table of Contents
1. [Introduction](#introduction)
2. [Data Structure](#data-structure)
3. [Methods](#methods)
4. [Final Implementation](#final-implementation)
5. [Extra: GUI](#extra-gui)
6. [Requirements](#requirements)


## Introduction

This repository is the first project of the master's degree in AI Engineering with [Profession AI](https://profession.ai), all the credits for the requests and idea go to this team.

ContactEase Solutions aims to simplify the management of phone contacts for its users, developing intuitive and interactive software that optimizes the organization and access to personal information.
Users often find it difficult to manage and organize their phone contacts efficiently. There are few simple and intuitive solutions that allow you to add, edit, delete, view and search contacts in one place, directly from the terminal.
ContactEase Solutions will provide an interactive console application which, thanks to the principles of object-oriented programming (OOP) in Python, will allow simple and structured contact management. Users will be able to easily save and upload contacts in a file format (e.g. JSON), ensuring efficient and secure data management.

Functionality:
- Adding a Contact: Allow the insertion of new contacts.
- Contacts View: Show all your contacts.
- Editing a Contact: Allow editing details of existing contacts.
- Deleting a Contact: Remove contacts from your phone agenda.
- Search for a Contact: Search for contacts by first name or last name.
- Saving and Loading: Save contacts to a file and load them at startup.

User Interface: 
- The interface will be command line based, offering a main menu with clear options for the various operations, thus ensuring a fluid and accessible user experience even for less experienced users.

Some useful integrations:
- As an extra part for this project, I will implement a GUI solution with a Web Application framework (TBD)
- Implement a log file to save all the operations done by the client, saving datetime and operation's name (**DONE**)
- Constrincts for length in each field of the phone agenda (first name and last name less than 30 words, note less than 150...) (**DONE**)


## Data Structure

The JSON data structure for storing contacts is as follows:

```json
{
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
```


## Methods

### 1. Add Contact

* **Method:** [`add_contact`](src/agenda_operations.py) 
* **Process:**
  * Prompts for first name, last name, phone number, email, group, address (street, city, state), and note.
  * Checks for duplicates and validates the inputs.
  * Saves the contact to the in-memory data structure.

### 2. View Contact

* **Method:** [`view_contact`](src/agenda_operations.py) 
* **Process:**
  * Prompts for the contact's first name and last name (if needed).
  * Displays all details of the contact.

### 3. Edit Contact

* **Method:** [`edit_contacts`](src/agenda_operations.py) 
* **Process:**
  * Prompts for the contact's first name and last name (if needed).
  * Allows editing of any field (first name, last name, phone, email, group, address, note).

### 4. Delete Contact

* **Method:** [`delete_contact`](src/agenda_operations.py) 
* **Process:**
  * Prompts for the contact's first name and last name (if needed).
  * Deletes the contact and updates the agenda.

### 5. Search Contact

* **Method:** [`search_contact`](src/agenda_operations.py) 
* **Process:**
  * Prompts for the first name or last name.
  * Displays matching contacts and allows viewing details.

### 6. Save Agenda

* **Method:** [`save_contacts`](src/agenda_operations.py) 
* **Process:**
  * Writes the current state of the agenda to a JSON file.

### 7. Load Agenda

* **Method:** [`load_contacts`](src/agenda_operations.py) 
* **Process:**
  * Reads the agenda from a JSON file and updates the in-memory data structure.

### 8. Initialize Agenda

* **Method:** [`initialize_agenda`](src/agenda_operations.py) 
* **Process:**
  * Creates a new agenda structure and saves it to a JSON file.


## Final Implementation

The final implementation includes a main script (`main.py`) and a class (`Operations`) that encapsulates all the functionality needed for managing your phone contacts.

In [menu.py](main.py), you can handles user interaction through a command-line menu, allowing users to perform various operations on the contact agenda. The menu will look like this:

Manage your phone agenda:
1. Add Contact
2. View Contact
3. Edit Contact
4. Delete Contact
5. Search Contact
6. Save Agenda
7. Load Agenda
8. Initialize Agenda
9. Exit

In the folder Logs, you can find the [log file](Logs/agenda_operations.log), where each operation is saved. The log file records informational messages, warnings, and errors, providing a detailed history of actions performed within the application. The log entries are formatted with a timestamp, log level, and message, such as:

```bash
2024-07-26 09-58-03 - INFO - Loaded contacts from file: Contacts/agenda.json
```

## Extra: GUI with Tkinter

This project is a graphical user interface (GUI) application built with Python's Tkinter library, designed to manage a simple phone agenda. It allows users to perform basic CRUD (Create, Read, Update, Delete) operations on contacts and save/load the agenda data to/from a JSON file.

What I used:
- **Tkinter**: The standard GUI toolkit for Python, used to create the application's windows, buttons, forms, and other interface elements.
- **JSON**: For saving and loading contact data in a structured format.
- **tld**: A library used for email validation by checking the validity of domain names.

In order to run the application, you need to execute the script to launch the agenda GUI:

    ```bash
    python agenda_gui.py
    ```

The GUI will open, providing a menu with options to add, view, edit, delete, and search for contacts. You can also save and load the agenda from a JSON file.

Feel free to use this application to manage your contacts efficiently. The interface is intuitive, and the functionalities are designed to be user-friendly, so you can focus more on managing your contacts rather than understanding the code. If you have any suggestions or improvements, contributions are welcome!


## Requirements

- Python 3.x
- JSON (for saving and loading contacts)

Requirements.txt file is [here](requirements.txt). To set up the virtual environment and install any required packages:

```bash
python -m venv .venv
source .venv/bin/activate  
pip install -r requirements.txt
