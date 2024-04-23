# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

# ====================================================================================
#   Importing libraries:
# ====================================================================================
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
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


# ====================================================================================
#   Login:
# ====================================================================================
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

# ====================================================================================
#   r - Register a new user:
# ====================================================================================


def reg_user():


# Request the user to input a new username
    new_username = input("New Username: ")

# If the username exists, prompt the user to enter a different username
    while True:
        if new_username in username_password:
            print("\nUser already exists. Please try a different username.")
            new_username = input("New Username: ")
        else:
            break

# Request a password for the new user
    new_password = input("New Password: ")

# Request the input of the password again so it can be compared
    confirm_password = input("Confirm Password: ")

# Check if the new password and confirmed password are the same
    if new_password == confirm_password:
# If they are the same, add them to the user.txt file
        print("New user added")
        username_password[new_username] = new_password

        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))
# If the passwords don't match display an error message
    else:
        print("Passwords do not match")



# ====================================================================================
#   a - Adding a task:
# ====================================================================================


def add_task():


# Allow a user to add a new task to task.txt file
# Prompt a user for the following:
# A username of the person whom the task is assigned to
# A title of a task
# A description of the task
# The due date of the task

# Prompt the user to declare who the task will be assigned to  
    task_username = input("Name of person assigned to task: ")

# If the provided username does not exist in the user.txt file request it again  
    while True:
        if task_username not in username_password.keys():
          print("User does not exist. Please enter a valid username")
          task_username = input("Name of person assigned to task: ")
        else:
          break

# Prompt the user to provide:
# The name/title of the task  
# A description of the task 
# The due date for completion
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
          task_due_date = input("Due date of task (YYYY-MM-DD): ")
          due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
          break

# If the provided due date does not follow the requested format display an error message
        except ValueError:
            print("Invalid datetime format. Please use the format specified")


# Retrieve the current date
    curr_date = date.today()

# Write the data to the file task.txt
# Initially mark this added task as not completed
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
}

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
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
        task_file.write("\n".join(task_list_to_write))
    print("\nTask successfully added.")



# ====================================================================================
# va - View all tasks
# ====================================================================================


def view_all():


# Reads & displays all tasks from the task.txt file
# Prints to the console including spacing and labelling
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)



# ====================================================================================
# vm - View my tasks
# ====================================================================================


def view_mine():


# Find a match between the username field and the logged in user
    user_tasks = [t for t in task_list if t['username'] == curr_user]

# If no tasks are matched display a notification
    if not user_tasks:
      print("\nNo tasks have been assigned to you.\n")
# Display all tasks assigned to the logged in user
    else:
        for i, t in enumerate(user_tasks, start=1):
            disp_str = f"\nTask {i}:\n"
            disp_str += f"\nTitle:\n{t['title']}\n"
            disp_str += f"\nAssigned date:\n{t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"\nDue date:\n{t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"\nDescription:\n{t['description']}\n"
            print(disp_str)

# Prompt the user to select a task to edit
        while True:
            print("\nWhich task would you like to amend?")
            task_number = input('''Enter its number or enter '-1' to go back to the main menu):\n''')

# Take the user back to the main menu if '-1' is entered
            if task_number == '-1':
                print("\nCancelled.")
                break
# Display the title of the task selected
            try:
                task_number = int(task_number)
                if 1 <= task_number <= len(user_tasks):
                    selected_task = user_tasks[task_number - 1]
                    print(f"\nSelected task: {selected_task['title']}\n")
# If selected task is already marked as complete
# Return user to main menu
                    if selected_task['completed']:
                        print("\nThis task has already been completed and cannot be edited.")
# Request user to enter 'complete' or 'edit'
                    else:
                        action = input("Type 'complete' to mark this task as complete or 'edit' to edit the task:\n")
# Change task status to complete
# Write the updated task list back to the tasks file
                        if action.lower() == 'complete':
                            selected_task['completed'] = True
                            with open("tasks.txt", "w") as task_file:
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
                                task_file.write("\n".join(task_list_to_write))
                            print("\nTask marked as complete!")
# Prompt user to choose between username or due date
                        elif action.lower() == 'edit':
                            while True:
                                edit_option = input("\nType 'username' to change the assigned username or 'due date' to change the due date:\n").lower()
                                if edit_option == 'username':
# Request new user to assign to selected task
# Write the updated task list back to the tasks file
                                    new_username = input("Enter the new username: ")
                                    if new_username in username_password:
                                        selected_task['username'] = new_username
                                        with open("tasks.txt", "w") as task_file:
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
                                            task_file.write("\n".join(task_list_to_write))
                                        print("\nUsername updated successfully!\n")
                                        break
# Invalid username notification
                                    else:
                                        print("\nThis username does not exist, please enter a valid username")
# Request new due date for selected task
# Write the updated task list back to the tasks file
                                elif edit_option == 'due date':
                                        new_due_date = input("Enter the new due date (YYYY-MM-DD): ")
                                        try:
                                            new_due_date = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                                            selected_task['due_date'] = new_due_date
                                            with open("tasks.txt", "w") as task_file:
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
                                                task_file.write("\n".join(task_list_to_write))
                                            print("\nDue date updated successfully!")
                                            break
# Various error notifications for invalid input
                                        except ValueError:
                                            print("\nInvalid datetime format. Please use the format specified (YYYY-MM-DD)\n")
                                else:
                                    print("\nInvalid option. Please enter 'username' or 'due date'.\n")
                        else:
                            print("\nInvalid action. Please enter 'complete' or 'edit'.\n")
                else:
                    print("\nInvalid task number. Please enter a valid task number.\n")
            except ValueError:
                print("\nInvalid input. Please enter a valid task number or '-1' to go back.\n")


# ====================================================================================
# gr - Generate Reports
# ====================================================================================


def gen_reports():


# Count the total number of tasks in the task list    
    total_tasks = len(task_list)

# Count the number of tasks that are marked as complete  
    completed_tasks = sum(task['completed'] for task in task_list)

# Calculate the number of tasks that are not complete    
    incomplete_tasks = total_tasks - completed_tasks

# Count the number of incomplete tasks that are also overdue    
    overdue_tasks = sum(1 for task in task_list if not task['completed'] and task['due_date'] < datetime.now())

# Calculate percentages
    percentage_incomplete = (incomplete_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    percentage_overdue = (overdue_tasks / total_tasks) * 100 if total_tasks > 0 else 0

# Open the task overview file in write mode, creating a new file if it doesn't already exist
    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write("Task Overview\n")
        task_overview_file.write("=============\n\n")
        task_overview_file.write(f"Total Tasks: {total_tasks}\n")
        task_overview_file.write(f"Completed Tasks: {completed_tasks}\n")
        task_overview_file.write(f"Incomplete Tasks: {incomplete_tasks}\n")
        task_overview_file.write(f"Incomplete & Overdue Tasks: {overdue_tasks}\n")
        task_overview_file.write(f"Percentage of Incomplete Tasks: {percentage_incomplete:.2f}%\n")
        task_overview_file.write(f"Percentage of Overdue Tasks: {percentage_overdue:.2f}%\n\n")

# Generate the User Overview report

# Get the total number of users
    num_users = len(username_password)

# Open the user overview file in write mode, creating a new file if it doesn't already exist
    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write("User Overview\n")
        user_overview_file.write("=============\n\n")

# Write the total number of users
        user_overview_file.write(f"Total Users: {num_users}\n\n")

# Write the total number of tasks
        user_overview_file.write(f"Total Tasks: {total_tasks}\n\n")

# Loop through each user and their password in the username_password dictionary
        for username, password in username_password.items():

# Count the total number of tasks assigned to each user
            num_user_tasks = sum(1 for task in task_list if task['username'] == username)

# Calculate the % of the total number of tasks assigned to each user            
            percentage_user_tasks = (num_user_tasks / total_tasks) * 100 if total_tasks > 0 else 0

# Calculate the % of tasks assigned to the user that are not yet completed and overdue
            percentage_incomplete_overdue_user_tasks = (sum(1 for task in task_list if task['username'] == username and not task['completed'] and task['due_date'] < datetime.now()) / total_tasks) * 100 if total_tasks > 0 else 0

# Count the total number of completed tasks assigned
            num_completed_user_tasks = sum(1 for task in task_list if task['username'] == username and task['completed'])

# Calculate the % of completed tasks based on user
            percentage_completed_user_tasks = (num_completed_user_tasks / num_user_tasks) * 100 if num_user_tasks > 0 else 0

# Calculate the % of incomplete tasks based on user
            percentage_incomplete_user_tasks = (incomplete_tasks / total_tasks) * 100 if total_tasks > 0 else 0

# Write the above calculations to the user overview file
            user_overview_file.write(f"User: {username}\n")
            user_overview_file.write(f"Total Tasks Assigned: {num_user_tasks}\n")
            user_overview_file.write(f"Percentage of Total Tasks: {percentage_user_tasks:.2f}%\n")
            user_overview_file.write(f"Total Completed Tasks: {num_completed_user_tasks}\n")
            user_overview_file.write(f"Percentage of Completed Tasks: {percentage_completed_user_tasks:.2f}%\n")
            user_overview_file.write(f"Percentage of Incomplete Tasks: {percentage_incomplete_user_tasks:.2f}%\n")
            user_overview_file.write(f"Percentage of Incomplete & Overdue Tasks: {percentage_incomplete_overdue_user_tasks:.2f}%\n\n")
    print("\nReports generated\n")



# ====================================================================================
#     Main Menu
# ====================================================================================

while True:
# Presenting the menu to the user 
# Convert user input to lower case
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - generate reports
ds - Display statistics
e - Exit
: ''').lower()

# Registering a new user
    if menu == 'r':
        reg_user()
# Add a new task
    elif menu == 'a':
        add_task()
# View all tasks
    elif menu == 'va':
        view_all()
# View tasks of currently logged in user
    elif menu == 'vm':
        view_mine()
# Generate reports
    elif menu == 'gr':
        gen_reports()
# Display statistics (admin only)
    elif menu == 'ds' and curr_user == 'admin': 
# Call the gen_reports function to generate the reports
        gen_reports()
# Display the contents of both files in the console
        with open("task_overview.txt", "r") as task_overview_file:
            print(task_overview_file.read())
            print()
        with open("user_overview.txt", "r") as user_overview_file:
            print(user_overview_file.read())
# Exit  
    elif menu == 'e':
        print('Goodbye!!!')
        exit()
# Invalid input message
    else:
        print("You have made a wrong choice, Please Try again")