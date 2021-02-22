from util import move, reversal
import json
import os

NUMBER_OF_LINES = 8
NUMBER_OF_COLUMNS = 8

def show_playing_area(disks, NUMBER_OF_LINES, NUMBER_OF_COLUMNS):
    """Displays the playing area based on the size of the playing area (number_of_lines, number_of_columns) and dict of disks.""" 
    for x in range(NUMBER_OF_LINES):
        for y in range(NUMBER_OF_COLUMNS):
            coordinate = x, y
            if coordinate in disks: 
                if disks[coordinate] == "x":
                    print("x", end=" ")
                else: 
                    print("o", end=" ")
            else:
                print(".", end=" ")
        print()

def create_beginning_disks(NUMBER_OF_LINES, NUMBER_OF_COLUMNS):
    """Creates start of the game and returns a dictionary of coordinates and symbols in this form: coordinates (tuple): symbol (string)."""
    disks = {
        (int((NUMBER_OF_LINES/2) - 1), int((NUMBER_OF_COLUMNS/2)-1)): "x",
        (int(NUMBER_OF_LINES/2),int(NUMBER_OF_COLUMNS/2)): "x",
        (int((NUMBER_OF_LINES/2) - 1),int(NUMBER_OF_COLUMNS/2)): "o",
        (int(NUMBER_OF_LINES/2),int((NUMBER_OF_COLUMNS/2)-1)): "o"
        }
    return disks

def ask_for_coordinates(disks, NUMBER_OF_LINES, NUMBER_OF_COLUMNS, symbol):
    """Ask for the line and the column, where the player wants to play. Returns coordinates (tuple)."""
    print("Player with {}, where do you want to play?".format(symbol))
    x = int(input("Write line"))
    y = int(input("Write column"))
    coordinates = x, y
    return coordinates

def check_coordinates(disks, new, NUMBER_OF_LINES, NUMBER_OF_COLUMNS):
    """Check, if the new coordinate is in the playing area and empty.""" 
    x, y = new

    #mé pracovní ukončení
    if x == 999: 
        raise SystemExit

    if x > NUMBER_OF_LINES or y > NUMBER_OF_COLUMNS or x < 0 or y < 0: 
        raise ValueError("These coordinates are out of the playing area.")
    elif new in disks: 
        raise ValueError("Here already is a disc.")
    else: 
        return new
    
def check_possible_move(disks, symbol, NUMBER_OF_LINES, NUMBER_OF_COLUMNS):
    """Checks if the player has possible moves. Returns True (there is at least one possible move) or False (there is not possible move for the symbol). """
    state = False
    for x in range(NUMBER_OF_LINES):
        for y in range(NUMBER_OF_COLUMNS):
            coordinate = x, y
            if coordinate not in disks:
                try: 
                    move(disks, coordinate, symbol)
                    state = True
                    break
                except ValueError:
                    pass
    return state

def check_all_moves(disks, NUMBER_OF_LINES, NUMBER_OF_COLUMNS):
    """Returns True, when there is no possible move for any of the symbols."""
    return check_possible_move(disks, "x", NUMBER_OF_LINES, NUMBER_OF_COLUMNS) == False and check_possible_move(disks, "o", NUMBER_OF_LINES, NUMBER_OF_COLUMNS) == False

def player_move(disks, symbol):
    """Realizes a player move. 
    
    Looks up possible moves, asks for new coordinates, finds all changing discs, and reverses them. 
    If there is no possible move, then it prints a notice and skips the move.
    """

    if check_possible_move(disks, symbol, NUMBER_OF_LINES, NUMBER_OF_COLUMNS):
        while True: 
            try:
                new = ask_for_coordinates(disks, NUMBER_OF_LINES, NUMBER_OF_COLUMNS, symbol)
                new = check_coordinates(disks, new, NUMBER_OF_LINES, NUMBER_OF_COLUMNS)
                changes = move(disks, new, symbol)
                reversal(disks, new, symbol, changes)
                break
            except ValueError as e: 
                print(e)    
    else: 
        print("You cannot play.")

def end(disks, NUMBER_OF_COLUMNS, NUMBER_OF_LINES):
    """Returns True when the playing area is full or there is only one sort of symbol left. """
    return len(disks) == NUMBER_OF_COLUMNS*NUMBER_OF_LINES or "x" not in disks.values() or "o" not in disks.values() 

def who_wins(disks):
    """Calculates score and prints the results of the game. """
    player_x = 0
    player_o = 0
    for disk in disks.values(): 
        if disk == "x":
            player_x += 1
        elif disk == "o":
            player_o += 1
    return player_x, player_o

def write_score(disks):
    """Prints the result of the game."""
    player_x, player_o = who_wins(disks)
    if player_x > player_o: 
        print("Game over! \nIt is {}:{}. The player with {} wins!".format(player_x, player_o, "x"))
    elif player_x < player_o: 
        print("Game over! \nIt is {}:{}. The player with {} wins!".format(player_x, player_o, "o"))
    else: 
        print("Game over! \nIt is {}:{}".format(player_x, player_o))

def code_json(disks):
    """Changes the discs dictionary to write to JSON.
    Returns dictionary in the format: symbol (string): coordinates (list of tuples)."""
    disks_code = {
        "x": [k for k,v in disks.items() if v == "x"],
        "o": [k for k,v in disks.items() if v == "o"]
    }

    return disks_code

def decode_json(decode):
    """Changes the dictionary from JSON back to the format: coordinate(tuple): symbol(string)."""
    disks = {}
    for key, list_of_coordinates in decode.items():
        for coordinate in list_of_coordinates: 
            disks[tuple(coordinate)] = key

    return disks

def play():
    """The mechanism of the game."""

    #beginning of the game, creating the playing area
    try: 
        with open("othello_disks.json", encoding="utf-8") as e: 
            disks = decode_json(json.loads(e.read()))
    except FileNotFoundError:
        disks = create_beginning_disks(NUMBER_OF_LINES, NUMBER_OF_COLUMNS)
    
    #cycle alternating moves of two players
    while not end(disks, NUMBER_OF_COLUMNS, NUMBER_OF_LINES):
        show_playing_area(disks, NUMBER_OF_LINES, NUMBER_OF_COLUMNS)
        player_move(disks, "x")
        
        show_playing_area(disks, NUMBER_OF_LINES, NUMBER_OF_COLUMNS)
        player_move(disks, "o")

        if check_all_moves(disks, NUMBER_OF_LINES, NUMBER_OF_COLUMNS):
            break

        deposit = json.dumps(code_json(disks))
        with open("othello_disks.json", "w", encoding="utf-8") as e: 
            print(deposit, file=e)

    #the end of the game - evaluation
    write_score(disks)
    show_playing_area(disks, NUMBER_OF_LINES, NUMBER_OF_COLUMNS)
    os.remove("othello_disks.json")