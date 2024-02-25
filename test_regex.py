import re

def basic_keyboard_input(prompt, is_password):
    """Check input against a regex pattern for basic keyboard characters
    Option for password validation"""
    while True:
        try:
            input_string = input(prompt)
            pattern = re.compile(r'^[a-zA-Z0-9 !"#$%&\'()*+,-./:;<=>?@^_`{|}~]+$')

            if re.match(pattern, input_string):
                # Check password had 1 lowercase, 1 uppercase, 1 number and one special char
                # Must be 8 char or longer {8,}
                if is_password:
                    pattern = re.compile(r'(?=^.{8,}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^a-zA-Z\d])')
                    upper = re.search("[^a-z]+",input_string)
                    lower = re.search("[^A-Z]+",input_string)
                    number = re.search("[^0-9]+",input_string)
                    special = re.search("[^@#$£%^&+=!]+",input_string)
                    if upper and lower and number and special:
                        return input_string
                    else:
                        print("Does not meet password requirements.")
                # Otherwise return basic character string
                else:
                    return input_string
            else:
                print("Input contains characters outside the basic keyboard set.")
        except ValueError:
            print("Input does not meet requirements.")

# Example usage:
test_string = basic_keyboard_input("Enter a string to check: ", False)
print(test_string)

# chars outside keyboard ╏┊┇║〣
#======================================================================

# Expression for 8 char password
# regex_pattern = re.compile(
#     r'(?=^.{8,}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^a-zA-Z\d])'
# )

# # Test the pattern
# test_strings = [
#     "Abcd123!",   # Valid
#     "Abcdefgh",   # Invalid (missing special character)
#     "abcd1234",   # Invalid (missing uppercase character)
#     "ABCD1234",   # Invalid (missing lowercase character)
#     "aB1!cD2@",    # Valid
#     "!@#$%^&*()",  # Invalid (missing alphanumeric characters)
# ]

# for test_string in test_strings:
#     result = bool(regex_pattern.match(test_string))
#     print(f'{test_string}: {"Valid" if result else "Invalid"}')




