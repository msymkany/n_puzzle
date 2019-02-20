def check_if_puzzle_is_solvable(a, p):
    inver = 0
    size = a - 1
    i = 0

    while p[i] != 0:
        i += 1
    p[i] = a * a

    row_t = 0
    col_t = -1
    way_row_t = 0
    way_col_t = 1
    step_t = 1
    zone00_t = 0
    zone01_t = 0
    zone11_t = 0
    zone10_t = 0
    while step_t < a * a:
        row_t += way_row_t
        col_t += way_col_t
        if (row_t == (zone00_t) and col_t == zone00_t - 1): # 0 0
            way_row_t = 0
            way_col_t = 1
            zone10_t += 1
        elif (col_t == (size - zone01_t) and row_t == (0 + zone01_t)): # 0 1
            way_row_t = 1
            way_col_t = 0
            zone00_t += 1
        elif (row_t == (size - zone11_t) and col_t == (size - zone11_t)): # 1 1
            way_row_t = 0
            way_col_t = -1
            zone01_t += 1
        elif (col_t == (zone10_t) and row_t == (size - zone10_t)): # 1 0
            way_row_t = -1
            way_col_t = 0
            zone11_t += 1
        step_t += 1

        row = 0
        col = -1
        way_row = 0
        way_col = 1
        step = 1
        zone00 = 0
        zone01 = 0
        zone11 = 0
        zone10 = 0
        while step <= a * a:
            row += way_row
            col += way_col
            if (p[row * a + col] < p[row_t * a + col_t]) and p[row * a + col] != 0:
                inver += 1
            if (row == (zone00) and col == zone00 - 1): # 0 0
                way_row = 0
                way_col = 1
                zone10 += 1
            elif (col == (size - zone01) and row == (0 + zone01)): # 0 1
                way_row = 1
                way_col = 0
                zone00 += 1
            elif (row == (size - zone11) and col == (size - zone11)): # 1 1
                way_row = 0
                way_col = -1
                zone01 += 1
            elif (col == (zone10) and row == (size - zone10)): # 1 0
                way_row = -1
                way_col = 0
                zone11 += 1
            step += 1
        p[row_t * a + col_t] = 0
    if inver % 2 == 0:
         return (1)
    return (0)