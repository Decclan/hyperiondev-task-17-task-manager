# Notes:
# 1. Use the following username and password to access the admin rights
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the
# program will look in your root directory for the text files.

"""=========importing libraries========="""
import os
import re
from datetime import date
from tabulate import tabulate

def open_files():
    """Check if main program required files exist otherwise create them"""
    # If no user.txt file, write one with a default account
    if not os.path.exists("user.txt"):
        with open("user.txt", "w", encoding="utf-8") as default_user_file:
            default_user_file.write("admin;password")

    # Create tasks.txt if it doesn't exist
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w", encoding="utf-8") as default_task_file:
            #default_task_file.write("Task List")
            default_task_file.write("admin;no-file;this is a default task file;2154-03-14;2154-02-11;No")
#===================================================================================================

def date_from_string(string_date):
    """"Returns date object from string"""
    try:
        string_date = string_date.split("-")
        string_date = list(map(lambda x: int(x), string_date))
        # Creates date object from string
        date_object = date(string_date[0], string_date[1], string_date[2])
        return date_object
    except ValueError:
        print("Date is invalid.")
#===================================================================================================

def valid_due_date():
    """Prompts user input due date string
    Compares to todays date
    Returns valid due date object"""
    while True:
        try:
            input_date = input("Please enter a due date in the format yyyy-mm-dd: ") 
            date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
            if date_pattern.match(input_date):
                input_date = input_date.split("-")
                input_date = list(map(lambda x: int(x), input_date))
                # Creates date object from string for comparison
                input_date = date(input_date[0], input_date[1], input_date[2])
                if input_date < date.today():
                    print("Sorry, this date has passed.")
                else:
                    print(f"{input_date} has been accepted.")
                    return input_date
            else:
                print("Invalid date input. Please try again.")
        except ValueError:
            print("Invalid date.")
#===================================================================================================

def basic_keyboard_input(prompt, is_password):
    """Basic keyboard input validation:
    True parameter is is password;
    - 1 lowercase char
    - 1 uppercase char
    - 1 number
    - special character
    otherwise returns valid string"""
    while True:
        try:
            input_string = input(prompt)
            # Basic keyboard character set
            pattern = re.compile(r'^[a-zA-Z0-9 !"#$%&\'()*+,-./:;<=>?@^_`{|}~]+$')

            if re.match(pattern, input_string):
                if is_password:
                    # Check password had 1 lowercase, 1 uppercase, 1 number and one special char
                    # Must be 8 char or longer {8,}
                    password_pattern = re.compile(r'(?=^.{8,}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^a-zA-Z\d])')
                    if re.match(password_pattern, input_string):
                        return input_string
                    else:
                        print("""\nDoes not meet password requirements. You need:
    8 characters minimum,
    1 lowercase character, 
    1 uppercase character, 
    1 numerical character, 
    1 special character\n""")
                # Otherwise return basic character string
                else:
                    return input_string
            else:
                print("Input contains characters outside the basic keyboard set.")
        except ValueError:
            print("Input does not meet requirements.")

# # Null check/Remove trailing whitespace
# word = word.strip()
# # If only whitespace was entered
# if word == "":
#     word = "null"
# return word
#===================================================================================================

def tasks_from_file():
    """Reads tasks.txt, return list of task dictionaries"""
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
        curr_t['due_date'] = task_components[3]
        curr_t['assigned_date'] = task_components[4]
        curr_t['completed'] = True if task_components[5] == "Yes" else False
        task_list.append(curr_t)

    return task_list
#===================================================================================================

def user_log_in():
    '''Reads usernames and passwords from the user.txt file to allow a user to login.'''
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
        curr_user = basic_keyboard_input("Username: ", False)
        # Admin bypass password validation
        if curr_user == "admin":
            curr_pass = input("Admin Password: ")
        else:
            curr_pass = basic_keyboard_input("Password: ", True)
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
            new_username = basic_keyboard_input("New Username: ", False)
            # - Request input of a new password
            new_password = basic_keyboard_input("New Password: ", True)
            # - Request input of password confirmation.
            confirm_password = basic_keyboard_input("Confirm Password: ", True)
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
                        return
                # - Otherwise you present a relevant message and rerun if attempt fails.
                else:
                    print("Passwords do no match.")
            else:
                print("This user already exists.")
        except ValueError:
            print("Invalid input.")
#===================================================================================================

def add_task(all_users_dict, main_task_list):
    '''Allow a user create new task dictionary.
        Prompt a user for the following: 
        - A username of the person whom the task is assigned to,
        - A title of a task,
        - A description of the task and 
        - the due date of the task.'''

    while True:
        try:
            # Assign to user if they exist
            task_username = basic_keyboard_input("Name of person assigned to task: ", False)
            if task_username not in all_users_dict:
                print("User does not exist. Please enter a valid username")
            else:
                task_title = basic_keyboard_input("Title of Task: ", False)
                task_description = basic_keyboard_input("Description of Task: ", False)
                task_due_date = valid_due_date()
                curr_date = date.today()
                task_due_date = str(task_due_date)
                curr_date = str(curr_date)

                print(task_due_date)
                print(curr_date)
                # New task dict data format
                new_task = {
                    "username": task_username,
                    "title": task_title,
                    "description": task_description,
                    "due_date": task_due_date,
                    "assigned_date": curr_date,
                    "completed": False # No
                }
                # Adds to tasks.txt file function
                add_task_to_file(main_task_list, new_task)
                return

        except ValueError:
            print("Invalid input.")
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
                    t['due_date'],
                    t['assigned_date'],
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            add_task_file.write("\n".join(task_list_to_write))
        print(f"\nTask was successfully added to the file.\n'{tabulate([task])}'\n")
    except ValueError:
        print(f"\nUnable to add this task:\n'{tabulate([task])}'\n")
#===================================================================================================

def edit_task(original_task_list, curr_user):
    """Option to edit current user tasks"""
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

                # Option for user to assign task to another user
                change_user_assigned = input("Would you like to assign this task to another user? y/n\n").lower()
                if change_user_assigned == "y":
                    key_to_edit = 'username'
                    new_user_value = input(f"Enter the new user to assign task '{index_to_edit}' to: ")

                    for key_in_dict in selected_dict.keys():
                        if key_to_edit == key_in_dict:
                            selected_dict[key_to_edit] = new_user_value
                            print(f"Successfully assigned the task to: {new_user_value}.")

                    print(f"\nTask updated:\n{tabulate([selected_dict])}")
                    add_task_to_file(original_task_list, selected_dict)
                    #return
                elif change_user_assigned == "n":
                    print(f"\nYou remain assigned to this task. Task updated:\n{tabulate([selected_dict])}")
                    add_task_to_file(original_task_list, selected_dict)
                    #break
                else:
                    print("Invalid option. Changes have not been saved.")
                # Option to change the due date of the task
                change_due_date = input("Would you like to change the due date of this task? y/n\n").lower()
                if change_due_date == "y":
                    key_to_edit = 'due_date'
                    new_date_value = str(valid_due_date())

                    for key_in_dict in selected_dict.keys():
                        if key_to_edit == key_in_dict:
                            selected_dict[key_to_edit] = new_date_value
                            print(f"Successfully changed the due date to: {new_date_value}.")
                    
                    print(f"\nTask updated:\n{tabulate([selected_dict])}")
                    add_task_to_file(original_task_list, selected_dict)
                    return
                elif change_user_assigned == "n":
                    print(f"\nThe due date remains the same. Task updated:\n{tabulate([selected_dict])}")
                    add_task_to_file(original_task_list, selected_dict)
                    break
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
    if not all_tasks:
        print("\nError: There are no tasks to display.")
        return
    print(tabulate(all_tasks))
#===================================================================================================

def view_mine(all_tasks, curr_user):
    '''Reads user tasks from task.txt file and prints to the console
    offers option to edit specific task by number and dictionary key
    '''
    if not all_tasks:
        print("\nError: You dont have any tasks to display.")
        return
    # Shows curr_user tasks and offers to edit them
    edit_task(all_tasks, curr_user)
#===================================================================================================

def display_statistics(all_users_dict, curr_tasks):
    """Admin display statistics menu option"""
    statistics_list = []
    num_users = len(all_users_dict.keys())
    num_tasks = len(curr_tasks)
    statistics_strings = [
        f"Number of users: {num_users}",
        f"Number of tasks: {num_tasks}"
    ]
    statistics_list.append("\n".join(statistics_strings))
    print(tabulate([statistics_list]))
#===================================================================================================

def generate_task_overview(curr_tasks):
    """ task_overview
        - number of tasks
        - number of completed tasks
        - number of uncompleted tasks
        - number of uncompleted overdue tasks
        - percentage of tasks that are incomplete
        - percentage of tasks that are overdue
    """
    # If no task_overview.txt file, create empty one
    if not os.path.exists("task_overview.txt"):
        with open("task_overview.txt", "w", encoding="utf-8"):
            pass
    if curr_tasks == "":
        print("No tasks to generate reports for.")
        return
    else:
        try:
            completed = 0
            incomplete = 0
            overdue_incomplete = 0
            num_tasks = len(curr_tasks)
            # Generate statistics from task list
            for task in curr_tasks:
                if task['completed'] is True:
                    completed += 1
                elif task['completed'] is False:
                    incomplete += 1
                    if date_from_string(task['due_date']) <= date.today():
                        overdue_incomplete +=1
            percentage_incomplete = round(incomplete / num_tasks * 100, 2)
            percentage_overdue = round(overdue_incomplete / num_tasks * 100, 2)
            # Create dictionary of required values
            tasks_overview_dict = {
                "total_number_of_tasks": num_tasks,
                "completed_tasks": completed,
                "incomplete_tasks": incomplete,
                "overdue_incomplete_tasks": overdue_incomplete,
                "percentage_tasks_incomplete": percentage_incomplete,
                "percentage_tasks_overdue": percentage_overdue # No
            }
            with open("task_overview.txt", "w", encoding="utf-8") as task_overview_file:
                task_list_to_write =[]
                str_attrs = [
                    f"The total number of tasks: {tasks_overview_dict['total_number_of_tasks']}",
                    f"The total number of completed tasks: {tasks_overview_dict['completed_tasks']}",
                    f"The total number of incomplete tasks: {tasks_overview_dict['incomplete_tasks']}",
                    f"The total number of overdue incomplete tasks: {tasks_overview_dict['overdue_incomplete_tasks']}",
                    f"The percentage of incomplete tasks: {tasks_overview_dict['percentage_tasks_incomplete']}",
                    f"The percentage of over due tasks: {tasks_overview_dict['percentage_tasks_overdue']}"
                ]
                task_list_to_write.append("\n".join(str_attrs))
                task_overview_file.write("\n".join(task_list_to_write))
                print(tabulate([task_list_to_write]))
            print("Your task overview report has been successfully generated.")
            return
        except ValueError:
            print("Unfortunately, something went wrong. Unable to generate task overview reports.")
#===================================================================================================

def generate_user_overview(curr_tasks, all_users_dict):
    """ user_overview
    - number of users
    - number of tasks
    for each user:
    - number of tasks assigned
    - percentage of the total tasks assigned to user
    - percentage of assigned tasks completed
    - percentage of uncompleted assigned tasks
    - percentage of tasks uncompleted and overdue
    """
    if not os.path.exists("user_overview.txt"):
        with open("user_overview.txt", "w", encoding="utf-8"):
            pass
    if curr_tasks == "":
        print("No tasks to generate reports for.")
        return
    else:
        try:
            num_users = len(all_users_dict)
            num_tasks = len(curr_tasks)

            # Create list of every user - avoids passwords for security
            all_users_list = list(all_users_dict)
            each_user_stats = []

            # For every user in the users.txt
            for user in all_users_list:
                # Check number of tasks assigned
                tasks_assigned = key_occurrences('username', user, curr_tasks)
                tasks_completed = 0
                need_completing = 0
                overdue = 0
                # Check how many tasks user has completed
                for task in curr_tasks:
                    if task['completed'] is True and user == task['username']:
                        tasks_completed += 1
                    elif task['completed'] is False and user == task['username']:
                        if date_from_string(task['due_date']) > date.today():
                            need_completing += 1
                        else:
                            overdue += 1

                # Percentage calculations if not zero - avoids zero division error
                if tasks_assigned != 0:
                    percent_of_total = round(tasks_assigned / num_tasks * 100, 2)
                    percent_completed = round(tasks_completed / tasks_assigned * 100, 2)
                    percent_need_completing = round(need_completing / tasks_assigned * 100, 2)
                    percent_overdue = round(overdue / tasks_assigned * 100, 2)
                else:
                    # Needs reassigning to avoid rogue values
                    percent_of_total = 0
                    percent_completed = 0
                    percent_need_completing = 0
                    percent_overdue = 0
                # Individual user stats
                user_tasks = {
                    'user' : (user, tasks_assigned),
                    'percent_of_total' : percent_of_total,
                    'percent_completed' : percent_completed,
                    'need_completing' : percent_need_completing,
                    'overdue' : percent_overdue
                }
                each_user_stats.append(user_tasks)

            with open("user_overview.txt", "w", encoding="utf-8") as task_overview_file:
                task_list_to_write =[]
                str_attrs = [
                    f"The total number of users: {num_users}",
                    f"The total number of tasks: {num_tasks}\n",
                ]
                for each_dict in each_user_stats:
                    str_attrs.append(f"Total tasks assigned for user: {each_dict['user']}")
                    str_attrs.append(f"Percent of total tasks assigned to user: {each_dict['percent_of_total']}")
                    str_attrs.append(f"Percent of total assigned tasks completed: {each_dict['percent_completed']}")
                    str_attrs.append(f"Percent of tasks that still need completing: {each_dict['need_completing']}")
                    str_attrs.append(f"Percent of tasks that are incomplete and overdue: {each_dict['overdue']}\n")

                task_list_to_write.append("\n".join(str_attrs))
                task_overview_file.write("\n".join(task_list_to_write))
                print(tabulate([task_list_to_write]))
            print("Your user overview report has been successfully generated.")
            return
        except ValueError:
            print("Unfortunately, something went wrong. Unable to generate user overview reports.")
#===================================================================================================

def key_occurrences(key, value, dictionary_list):
    """Checks number of tasks fro each user for user overview"""
    count = 0
    for dictionary in dictionary_list:
        if key in dictionary and dictionary[key] == value:
            count += 1
    return count
#===================================================================================================

def user_menu():
    """Main menu of choices for user"""
    open_files()
    main_log_in = user_log_in() # returns curr_user [0] dict of all users [1]
    curr_user = main_log_in[0]
    all_users_dict = main_log_in[1]
    # Create list of dictionaries for all tasks from tasks.txt
    curr_tasks = tasks_from_file()
    # Main menu loop
    while True:
        # presenting the menu to the user and
        # making sure that the user input is converted to lower case.
        print()
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my tasks
    gr - Generate reports
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
        elif menu == 'gr':
            if curr_user == 'admin':
                generate_task_overview(curr_tasks)
                generate_user_overview(curr_tasks, all_users_dict)
            else:
                print("You do not have the required permissions to generate reports.")
        elif menu == 'ds':
            if curr_user == 'admin':
                display_statistics(all_users_dict, curr_tasks)
            else:
                print("You do not have the required permissions to view the statistics.")
        elif menu == 'e':
            print('Goodbye!!!')
            exit()
        else:
            print("You have made a wrong choice, Please Try again")
#===================================================================================================

user_menu()
