# Notes:
# 1. Use the following username and password to access the admin rights
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the
# program will look in your root directory for the text files.

"""=========importing libraries========="""
import os
import re
from datetime import datetime, date
from tabulate import tabulate

DATETIME_STRING_FORMAT = "%Y-%m-%d"

"""Input Validation functions"""

def word_input(prompt):
    """Word or sentence validation"""
    while True:
        word = input(prompt)
        # Regex check for basic sentence characters.
        invalid_word = re.search("[^A-Za-z0-9 ,.$£:;*#+%=!\-]+",word)
        # You have to escape the minus sign using backslash.
        # var alphaExp = /^[a-zA-ZåäöÅÄÖ\s\-]+$/;
        # To stop them from using it in the beginning or the end, try something like this:
        # var alphaExp = /^[a-zA-ZåäöÅÄÖ\s]+[a-zA-ZåäöÅÄÖ\s\-]*[a-zA-ZåäöÅÄÖ\s]+$/;

        if invalid_word:
            print("Only special characters , . $ £ : ; * # + % = ! - will be accepted.")
        # If empty
        elif word == "":
            print("Please enter a value.")
        else:
            # Remove trailing whitespace
            word = word.strip()
            # If only whitespace was entered
            if word == "":
                word = "null"
            return word
#===================================================================================================

def password_validation(prompt):
    """Password must be 8 characters long and meet complexity criteria"""
    while True:
        try_password = input(prompt)
        # The .fullmatch requires entire string to match the limits - 8 character length
        if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', try_password):
            # Must have one of each
            upper = re.search("[^a-z]+",try_password)
            lower = re.search("[^A-Z]+",try_password)
            number = re.search("[^0-9]+",try_password)
            special = re.search("[^@#$£%^&+=!]+",try_password)
            if upper and lower and number and special:
                return try_password
        else:
            print("""\nInvalid input.
Please enter at least:
one capital letter
one lowercase letter
one number
one special character: @ # $ £ % ^ & + = !\n""")
#===================================================================================================

def task_file():
    """Create tasks.txt if it doesn't exist"""
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w", encoding="utf-8") as default_task_file:
            #default_task_file.write("Task List")
            default_task_file.write("admin;no-file;this is a default task file;2024-03-14;2024-02-21;No")

    with open("tasks.txt", 'r', encoding="utf-8") as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    task_list = []
    for t_str in task_data:
        curr_t = {}

        # Split by semicolon and manually add each component
        task_components = t_str.split(";")
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False
        task_list.append(curr_t)

    return task_list
    # if deleted/file empty index error occurs
#===================================================================================================

def user_log_in():
    '''This code reads usernames and password from the user.txt file to 
        allow a user to login.
    '''
    # If no user.txt file, write one with a default account
    if not os.path.exists("user.txt"):
        with open("user.txt", "w", encoding="utf-8") as default_user_file:
            default_user_file.write("admin;password")

    # Read in user_data
    with open("user.txt", 'r', encoding="utf-8") as user_file:
        user_data = user_file.read().split("\n")

    # Convert to a dictionary
    all_users_dict = {}
    for user in user_data:
        username, password = user.split(';')
        all_users_dict[username] = password

    logged_in = False
    while not logged_in:

        print("LOGIN")
        curr_user = word_input("Username: ")
        # Admin bypass password validation
        if curr_user == "admin":
            curr_pass = input("Admin Password: ")
        else:
            curr_pass = password_validation("Password: ")
        if curr_user not in all_users_dict:
            print("User does not exist")
            continue
        elif all_users_dict[curr_user] != curr_pass:
            print("Wrong password")
            continue
        else:
            print("\nLogin Successful!")
            logged_in = True
            # [0] for curr_user [1] for all users
            return curr_user, all_users_dict
#===================================================================================================

def reg_user(original_user_dict):
    '''Add a new user to the user.txt file'''
    while True:
        try:
            # - Request input of a new username
            new_username = word_input("New Username: ")

            # - Request input of a new password
            new_password = password_validation("New Password: ")

            # - Request input of password confirmation.
            confirm_password = password_validation("Confirm Password: ")

            # - Check if user already exists in dictionary
            if new_username not in original_user_dict:
                # - Check if the new password and confirmed password are the same.
                if new_password == confirm_password:
                    # - If they are the same, add them to the user.txt file,
                    print(f"New user: {new_username} successfully added.")
                    original_user_dict[new_username] = new_password

                    with open("user.txt", "w", encoding="utf-8") as out_file:
                        new_user_data = []
                        for k in original_user_dict:
                            new_user_data.append(f"{k};{original_user_dict[k]}")
                        out_file.write("\n".join(new_user_data))
                    break
                # - Otherwise you present a relevant message and rerun if attempt fails.
                else:
                    print("Passwords do no match.")
            else:
                print("This user already exists.")
        except ValueError:
            print("Invalid input.")
#===================================================================================================

def add_task(username_password, main_task_list):
    '''Allow a user to add a new task.
        Prompt a user for the following: 
        - A username of the person whom the task is assigned to,
        - A title of a task,
        - A description of the task and 
        - the due date of the task.'''

    # Date object from todays date
    curr_date = date.today()
    # Cast to string as date() method cant compare to datetime()
    string_date = date.isoformat(curr_date)
    # Cast as date without time for datetime object comparison
    curr_date = datetime.strptime(string_date, DATETIME_STRING_FORMAT)

    while True:
        try:
            # Assign to user if they exist
            task_username = word_input("Name of person assigned to task: ")
            if task_username not in username_password.keys():
                print("User does not exist. Please enter a valid username")

            else:
                task_title = word_input("Title of Task: ")
                task_description = word_input("Description of Task: ")

                task_due_date = input("Due date of task (YYYY-MM-DD): ")

                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                # Due date validation
                if due_date_time < curr_date:
                    print("Must be due today or after todays date")
                else:
                    break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")
    # New task dict data format
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time, #due_date_time, adds 00:00:00 time stamp try string_date,
        "assigned_date": curr_date,
        "completed": False # No
    }
    # Adds to tasks.txt file function
    add_task_to_file(main_task_list, new_task)
#===================================================================================================

def add_task_to_file(main_task_list, task):
    """Add task to main list of tasks in tasks.txt"""
    try:
        if task not in main_task_list:
            main_task_list.append(task)
        with open("tasks.txt", "w", encoding="utf-8") as add_task_file:
            task_list_to_write = []
            for t in main_task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            add_task_file.write("\n".join(task_list_to_write))
        print("Task successfully added to file.")
    except ValueError:
        print("Unable to add task")
#===================================================================================================

def edit_task(original_task_list, curr_user):
    """Option to edit current user tasks"""
    if not original_task_list:
        print("Error: The list of dictionaries is empty.")
        return

    while True:
        try:
            # Creates a list of curr_user tasks for editing
            this_user_tasks = [user for user in original_task_list if user['username'] in curr_user]
            if not this_user_tasks:
                print("No users found with the specified usernames.")
                return

            # Create a custom index based on length of curr_user tasks
            display_index = [index for index in range(len(this_user_tasks) + 1)]
            # Remove the 0 from start
            display_index.pop(0)
            # Build a table of all curr_user tasks for display only
            table = tabulate(this_user_tasks, showindex=display_index)
            print(table)

            # Ask the user to select a task dictionary by index
            index_to_edit = int(input(f"Enter the index of the dictionary to edit (1 to {len(this_user_tasks)}) or -1 to exit: "))

            if index_to_edit == -1:
                print("Returned to main menu.")
                return
            # Ask user if selected task is complete
            task_completed = input("Has this task been completed? y/n\n").lower()
            # Ensure the index is valid/in range
            if 1 <= index_to_edit <= len(this_user_tasks):
                selected_dict = this_user_tasks[index_to_edit - 1]
                # Create tabulate object of this task for print/display only
                # Iterable inside list
                # Prompt user if this task has been completed
            else:
                print("Invalid index. Please enter a valid index.")

            if task_completed == "y":
                selected_dict['completed'] = True
                # Call write to file function with new values
                add_task_to_file(original_task_list, selected_dict)
                print(f"\nCongratulations on completing task '{index_to_edit}'.\n{tabulate([selected_dict])}")
                # Cant edit further once completed
                return
            elif task_completed == "n":
                # Change back to false if previously changed to true
                selected_dict['completed'] = False
                print(tabulate([selected_dict]))

                # Option for user to assign task to another user - needs due date functionality
                change_user_assigned = input("Would you like to assign this task to another user? y/n\n").lower()
                change_due_date = input("Would you like to change this tasks due date? y/n\n").lower()
                if change_user_assigned == "y":
                    key_to_edit = 'username'
                    new_value = input(f"Enter the new user to assign task '{index_to_edit}' to: ")

                    for key_in_dict in selected_dict.keys():
                        if key_to_edit == key_in_dict:
                            selected_dict[key_to_edit] = new_value
                            print(f"Successfully assigned the task to {new_value}.")

                    print(f"\nDictionary updated:\n{tabulate([selected_dict])}")
                    add_task_to_file(original_task_list, selected_dict)
                    return # Redundant?
                elif change_user_assigned == "n":
                    print(f"\nYou remain assigned to this task. Dictionary updated:\n{tabulate([selected_dict])}")
                    add_task_to_file(original_task_list, selected_dict)
                    break # Redundant?
                else:
                    print("Invalid option. Changes have not been saved.")
            else:
                print("Invalid option. Changes have not been saved.")
        except ValueError:
            print("Invalid input. Please try again.")
#===================================================================================================

def view_all(all_tasks):
    '''Reads all tasks from task.txt file and prints to the console
    '''
    if all_tasks == "": # If task adding crashes, all tasks data is lost
        print("No current tasks.")
    print(tabulate(all_tasks))
#===================================================================================================

def view_mine(all_tasks, curr_user):
    '''Reads user tasks from task.txt file and prints to the console
    offers option to edit specific task by number and dictionary key
    '''
    if all_tasks == "": # If task adding crashes, all tasks data is lost
        print("No current tasks.")
    edit_task(all_tasks, curr_user)
#===================================================================================================

def user_menu():
    """Main menu of choices for user"""
    # Main log in
    main_log_in = user_log_in() # returns curr_user [0] dict of all users [1]
    curr_user = main_log_in[0]
    all_users_dict = main_log_in[1]
    # Read or create list of dictionaries for all tasks from tasks.txt
    curr_tasks = task_file()
    # Main loop
    while True:
        # presenting the menu to the user and
        # making sure that the user input is converted to lower case.
        print()
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my task
    ds - Display statistics
    e - Exit
    : ''').lower()

        if menu == 'r':
            reg_user(all_users_dict)

        elif menu == 'a':
            add_task(all_users_dict, curr_tasks)

        elif menu == 'va':
            view_all(curr_tasks)

        elif menu == 'vm':
            view_mine(curr_tasks, curr_user)

        elif menu == 'ds':
            '''admin can display statistics about number of users and tasks.'''
            if curr_user == 'admin':
                num_users = len(all_users_dict.keys())
                num_tasks = len(curr_tasks)

                print("-----------------------------------")
                print(f"Number of users: \t\t {num_users}")
                print(f"Number of tasks: \t\t {num_tasks}")
                print("-----------------------------------")
            else:
                print("You do not have the required permissions to view the statistics.")

        elif menu == 'e':
            print('Goodbye!!!')
            exit()

        else:
            print("You have made a wrong choice, Please Try again")
#===================================================================================================

user_menu()
