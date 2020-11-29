from sys import argv
from csv import reader, DictReader

# Checking for valid input
if len(argv) != 3:
    print("Usage: 3 arguments should be given")
    exit()

# Open a CSV file and read contents into a list
# https://docs.python.org/3/library/csv.html
with open(argv[1]) as DNAdatabase:
    database = reader(DNAdatabase)
    for row in database:
        DNAPattern = row
        DNAPattern.pop(0)
        break

# Declaring empty list
sequences = {}

for item in DNAPattern:
    sequences[item] = 1

# https://docs.python.org/3/library/csv.html
with open(argv[2]) as DNAsequence:
    sequenceData = reader(DNAsequence)
    for row in sequenceData:
        DNAsequence = row  # python just knows the data type
        # print(DNAlist)

DNA = DNAsequence[0]

# now lets check for repetitions
for k in sequences:

    # we need to reset the value of counters at the start of the loop
    lenghtSequence = len(k)
    max_counter = 0
    counter = 0
    lengthDNA = len(DNA)

    for i in range(lengthDNA):

        while counter > 0:
            counter -= 1
            continue

        # if the sequence matches the "k" and repeates, we start counting in the while loop
        if DNA[i: i + lenghtSequence] == k:
            while DNA[i: i + lenghtSequence] == DNA[i - lenghtSequence: i]:
                counter += 1
                i += lenghtSequence
            max_counter = max(max_counter, counter)

    sequences[k] += max_counter

# print person if he has been found
with open(argv[1]) as DNAdatabase:

    DNApeople = DictReader(DNAdatabase)

    for DNAperson in DNApeople:
        counter1 = 0
        for DNA in sequences:
            if sequences[DNA] == int(DNAperson[DNA]):
                counter1 += 1

        if counter1 == len(sequences):
            print(DNAperson["name"])
            exit()

    print("No match")