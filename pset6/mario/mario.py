import cs50 as cs


# if true loop
while True:
    height = cs.get_int("Height: ")
    if (height >= 1 and height <= 8):
        break

# one liner code for drawing pyramid
for i in range(1, height+1):
    print(' '*(height-i), end='')
    print('#'*(i))

