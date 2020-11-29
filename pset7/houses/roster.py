# TODO
from cs50 import SQL
from sys import argv

# Check for valid input
if len(argv) != 2:
    print("Only two arguments are accepted.")
    exit()

db = SQL("sqlite:///students.db")

house = argv[1]

students = db.execute("SELECT * FROM students WHERE house = (?) ORDER BY last", house)

for student in students:
    hasMiddle = student["middle"]
    if hasMiddle == None:
        # print if student has middle name
        print(f"{student['first']} {student['last']}, born {student['birth']}")
    else:
        # print if student does not have middle
        print(f"{student['first']} {student['middle']} {student['last']}, born {student['birth']}")