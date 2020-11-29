# TODO
from cs50 import SQL
import csv
from sys import argv, exit

# Check for input
if(len(argv) != 2):
    print("Only two arguments are accepted.")
    exit()

db = SQL("sqlite:///students.db")

# Open the character file and create a reader
with open(argv[1], newline="") as charFile:
    characters = csv.reader(charFile)
    for char in characters:
        if(char[0] == "name"):
            continue

        # Split the full name into first, middle and last name
        listOfNames = char[0].split()
        length = len(listOfNames)

        # Check if a person has all three names
        if length == 3:
            db.execute("INSERT INTO students(first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                       listOfNames[0], listOfNames[1], listOfNames[2], char[1], char[2])
        # Otherwise it does not have middle name
        else:
            db.execute("INSERT INTO students(first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                       listOfNames[0], None, listOfNames[1], char[1], char[2])