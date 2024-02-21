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
        invalid_word = re.search("[^A-Za-z0-9 ,.$£:;*#-+%=!]+",word)

        if invalid_word:
            print("Only special characters , . $ £ : ; * # - + % = ! will be accepted.")
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
        else:
            print("Invalid password.")
#===================================================================================================

def task_file():
    """Create tasks.txt if it doesn't exist"""
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w", encoding="utf-8") as default_task_file:
            #default_task_file.write("Task List")
            default_task_file.write("admin;Add functionality to task manager;Add additional options and refactor the code.;2022-12-01;2022-11-22;No")

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
    username_password = {}
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password

    logged_in = False
    while not logged_in:

        print("LOGIN")
        curr_user = word_input("Username: ")
        # Admin bypass password validation
        if curr_user == "admin":
            curr_pass = input("Admin Password: ")
        else:
            curr_pass = password_validation("Password: ")
        if curr_user not in username_password: ## [consider-iterating-dictionary]
            print("User does not exist")
            continue
        elif username_password[curr_user] != curr_pass:
            print("Wrong password")
            continue
        else:
            print("Login Successful!")
            logged_in = True
            return username_password, curr_user
#===================================================================================================

def reg_user(username_password):
    '''Add a new user to the user.txt file'''
    # - Request input of a new username
    new_username = word_input("New Username: ")

    # - Request input of a new password
    new_password = password_validation("New Password: ")

    # - Request input of password confirmation.
    confirm_password = password_validation("Confirm Password: ")

    # - Check if user already exists in dictionary
    if new_username not in username_password:
        # - Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # - If they are the same, add them to the user.txt file,
            print(f"New user: {new_username} successfully added.")
            username_password[new_username] = new_password

            with open("user.txt", "w", encoding="utf-8") as out_file:
                new_user_data = []
                for k in username_password:
                    new_user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(new_user_data))

        # - Otherwise you present a relevant message and rerun if attempt fails.
        else:
            print("Passwords do no match.")
            reg_user(username_password)
    else:
        print("This user already exists.")
        reg_user(username_password)
#===================================================================================================

def add_task(username_password, task_list):
    '''Allow a user to add a new task to task.txt file
        Prompt a user for the following: 
        - A username of the person whom the task is assigned to,
        - A title of a task,
        - A description of the task and 
        - the due date of the task.'''

    task_username = word_input("Name of person assigned to task: ")

    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        #continue
    task_title = word_input("Title of Task: ")
    task_description = word_input("Description of Task: ")

    # Date object from todays date
    curr_date = date.today()
    # Cast to string as date() method cant compare to datetime()
    string_date = date.isoformat(curr_date)
    # Cast as date without time for datetime object comparison
    curr_date = datetime.strptime(string_date, DATETIME_STRING_FORMAT)

    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            print(curr_date)

            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            # Due date validation
            if due_date_time < curr_date:
                print("Must be due today or after todays date")
            else:
                break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w", encoding="utf-8") as add_task_file:
        task_list_to_write = []
        for t in task_list:
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
    print("Task successfully added.")
#===================================================================================================

def view_all(all_tasks):
    '''Reads the task from task.txt file and prints to the console
    '''
    if all_tasks == "":
        print("No current tasks.")

    # for t in all_tasks:
    #     disp_str = f"Task: \t\t {t['title']}\n"
    #     disp_str += f"Assigned to: \t {t['username']}\n"
    #     disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    #     disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    #     disp_str += f"Task Description: \n {t['description']}\n"
        #print(disp_str)
    print(tabulate(all_tasks))
#===================================================================================================

def view_mine(curr_user, my_tasks):
    '''Reads the task from task.txt file and prints to the console
    '''
    # choice = 1
    # # for t in my_tasks:
    # #     if t['username'] == curr_user:
    # #         disp_str = f"Task: \t\t {t['title']}\n"
    # #         disp_str += f"Assigned to: \t {t['username']}\n"
    # #         disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    # #         disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    # #         disp_str += f"Task Description: \n {t['description']}\n"
    #         #print(disp_str)
    # print(tabulate(my_tasks))
    
    # total_tasks = len(my_tasks)
    # if choice == 1:
    #     print(my_tasks[0]['title'])
    #     print(total_tasks)
#===================================================================================================

def user_menu():
    """Main menu of choices for user"""
    successful_log_in = user_log_in()
    # Dictionary of current users and passwords
    username_password = successful_log_in[0]
    curr_user = successful_log_in[1]

    #prints all username passwors dictionary
    #print(username_password)

    curr_tasks = task_file()

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
            '''admin can add new users.'''
            if curr_user == "admin":
                reg_user(username_password)
            else:
                print("You do not have the required permissions to add a new user.")

        elif menu == 'a':
            add_task(username_password, curr_tasks)

        elif menu == 'va':
            view_all(curr_tasks)

        elif menu == 'vm':
            view_mine(curr_user, curr_tasks)

        elif menu == 'ds':
            '''admin can display statistics about number of users and tasks.'''
            if curr_user == 'admin':
                num_users = len(username_password.keys())
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

# regex for password - 1 captial letter, 1 number, 1 special character
