import cs50 as cs


# if true loop
while True:
    change = cs.get_float("Change owed: ")
    if (change > 0):
        break

cents = round(change * 100)
# print(cents)
counter = 0
remain = cents


quarter = 25
while(cents >= quarter):
    cents -= quarter
    counter += 1
# print(counter)
dimes = 10
while(cents >= dimes):
    cents -= dimes
    counter += 1
# print(counter)
nickles = 5
while(cents >= nickles):
    cents -= nickles
    counter += 1
# print(counter)
pennies = 1
while(cents >= pennies):
    cents -= pennies
    counter += 1

print(counter)
