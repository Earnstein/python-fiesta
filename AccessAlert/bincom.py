import os
import  re


# 1 Creating a text file with my full name
with open("bincom.txt", "w") as file:
    file.write("Bakare Damilola Ayomide")


def get_names(filename):
    try:
        with open(filename, "r") as file:
            content = file.read().strip()
        names = content.split()
        if len(names) == 3:
            first_name, middle_name, last_name = names
            print("My First Name is:", first_name)
            print("My Middle Name is:", middle_name)
            print("My Last Name is:", last_name)
        else:
            print("Invalid format: The file should contain three names separated by spaces.")
    except FileNotFoundError:
        print(f"The file {filename} does not exist.")
    except Exception as e:
        print("An error occurred:", e)


# printing the names
get_names("bincom.txt")

# 2 Printing the local file path with the os module
print("Local File Path:", os.path.abspath("bincom.txt"))


# 3 print baby names in an html file with regular expression


pattern = '<tr[^>]*>\s*<td[^>]*>\d+</td>\s*<td[^>]*>([^<]+)</td>\s*<td[^>]*>([^<]+)</td>\s*</tr>'
patterns = re.compile(pattern)
with open("baby2008.html", "r") as file:
    html_content = file.read()
# Find all matches in the HTML content
matches = re.findall(patterns, html_content)

# Extracted babies names
for match in matches:
    first_name, last_name = match
    print(f"First Name: {first_name}, Last Name: {last_name}")