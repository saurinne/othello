def move(disks, new_coordinates, symbol):
    """Returns list of coordinates, which the move changes, or ValueError, if the move is against rules. """
    changes = []
    line, column = new_coordinates
    for coordinate in disks.keys():
        x, y = coordinate

        #looks for discs in lines
        if x == line and disks[coordinate] == symbol:
            possibility = []
            for between in range(min(y, column) + 1, max(y, column)):
                possible_change = line, between
                if possible_change in disks:
                    if disks[possible_change] != symbol:
                        possibility.append(possible_change)
            if len(possibility) + 1 == abs(y - column):
                for changing_disk in possibility: 
                    changes.append(changing_disk)

        #looks for discs in columns
        if y == column and disks[coordinate] == symbol:
            possibility = []
            for between in range(min(x, line) + 1, max(x, line)):
                possible_change = between, column
                if possible_change in disks:
                    if disks[possible_change] != symbol:
                        possibility.append(possible_change)
            if len(possibility) + 1 == abs(x - line):
                for changing_disk in possibility: 
                    changes.append(changing_disk)

        #looks for discs in diagonals
        if abs(line - x) == abs(column - y) and disks[coordinate] == symbol: 
            possibility = []
            for try_line in range(min(line,x) + 1, max(line,x)): 
                for try_column in range(min(column,y) + 1, max(column,y)): 
                    if abs(try_line - x) == abs(try_column - y): 
                        possible_change = try_line, try_column
                        if possible_change in disks:
                            if disks[possible_change] != symbol:
                                possibility.append(possible_change)
            if len(possibility) + 1 == abs(x - line):
                for changing_disk in possibility: 
                    changes.append(changing_disk)

    if not changes: 
        raise ValueError("This move is against rules")
    
    return changes

def reversal(disks, new_coordinates, symbol, changes):
    """Adds new coordinate in the dictionary and reverses discs in changes list."""
    disks[new_coordinates] = symbol
    for disk in disks.keys(): 
        if disk in changes: 
            disks[disk] = symbol
    return disks