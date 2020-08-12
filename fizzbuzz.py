for i in range(100):
    j = str(i)
    if i == 0:
        continue
    if i % 3 == 0 and i % 5 == 0:   
        print( j + " is fizzbuzz")
    elif i % 3 == 0:
        print(j + " is fizz")
    elif i % 5 == 0:
        print(j + " is buzz")
    else:
        pass