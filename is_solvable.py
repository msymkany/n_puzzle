def check_if_puzzle_is_solvable(a, p, solved):
    inver = 0

    i = 0
    while p[i] != 0:
        i += 1
    p[i] = a * a
    if (a % 2 == 0):
        inver += i // a
    i = 0
    while solved[i] != 0:
        i += 1
    solved[i] = a * a
    if (a % 2 == 0):
        inver += i // a
    i = 0
    sol = 0
    while i < (a * a):
        j = i
        j += 1
        while j < (a * a):
            if (p[j] < p[i] and p[i] != (a * a)):
            #if (p[j] < p[i] and (tm % 2 == 0 or (tm % 2 != 0 and p[i] != (a * a)))):
                inver += 1
            if (solved[j] < solved[i] and solved[i] != (a * a)):
                sol += 1
                inver += 1
            j += 1
        i += 1
    if inver % 2 == 0:
        return 1
    else:
        return 0