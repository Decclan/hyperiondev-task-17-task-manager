from datetime import date #datetime

# def valid_string_date(date_str):
#     try:
#         # parse date string into func
#         date_format = datetime.strptime(date_str, '%d-%m-%Y')
#         print(f"{date_str} is valid. Date format: {date_format}")
#         return date_format
#     except ValueError:
#         print("Invalid date. The date format is: dd-mm-yyyy")

# # def valid_due_date(user_input):
# due_date = valid_string_date("23-03-2024")

# current_date = datetime.now()
# current_date_str = current_date.strftime('%d-%m-%Y')
# due_date_str = due_date.strftime('%d-%m-%Y')

# if due_date > current_date:
#     print(f"""
# {current_date_str} 
# {due_date_str}
# {current_date}
# {due_date}
# """)

# input_date = "2024-02-28"
# input_date = input_date.split("-")
# input_date = list(map(lambda x: int(x), input_date))
# input_date = date(input_date[0], input_date[1], input_date[2])
# print(f"Input date as date object: {input_date}")
# print(date.today())

def date_from_string(string_date):
    try:
        string_date = string_date.split("-")
        mapped = list(map(lambda x: int(x), string_date))
        # Creates date object from string for comparison
        date_object = date(mapped[0], mapped[1], mapped[2])
        # If valid date create string
        if date_object:
            string_date = str(date_object)
            print(f"Original string: {string_date}")
        print(f"Date: {date_object} is valid.")
        return date_object
    except ValueError:
        print(f"Date: {string_date} is invalid.")

date_from_string("2024-04-23")

# def valid_due_date():
#     try:
#         input_date = "2024-02-18" 
#         input_date = input_date.split("-")
#         input_date = list(map(lambda x: int(x), input_date))
#         # Creates date object from string for comparison
#         input_date = date(input_date[0], input_date[1], input_date[2])

#         if input_date < date.today():
#             print("Sorry, this date has passed.")
#         else:
#             print(f"Return valid date {input_date}")
#     except ValueError:
#         print("Invalid input.")

# valid_due_date()