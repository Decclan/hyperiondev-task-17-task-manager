from datetime import datetime

#DATETIME_STRING_FORMAT = "%Y-%m-%d"

def valid_string_date(date_str):
    try:
        # parse date string into func
        date_format = datetime.strptime(date_str, '%d-%m-%Y')
        print(f"{date_str} is valid. Date format: {date_format}")
        return date_format
    except ValueError:
        print("Invalid date. The date format is: dd-mm-yyyy")



# def valid_due_date(user_input):

due_date = valid_string_date("23-03-2024")

current_date = datetime.now()
current_date_str = current_date.strftime('%d-%m-%Y')
due_date_str = due_date.strftime('%d-%m-%Y')

if due_date > current_date:


    print(f"""
{current_date_str} 
{due_date_str}

{current_date}
{due_date}
""")