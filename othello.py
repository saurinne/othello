from util import move, reversal
import json
import os

size = 8

def show_playing_area(disks):
    """Displays the playing area based on the size of the playing area and dict of disks.""" 
    for x in range(size):
        for y in range(size):
            coordinate = x, y
            if coordinate in disks: 
                if disks[coordinate] == "x":
                    print("x", end=" ")
                else: 
                    print("o", end=" ")
            else:
                print(".", end=" ")
        print()

def create_beginning_disks():
    """Creates start of the game and returns a dictionary of coordinates and symbols in this form: coordinates (tuple): symbol (string)."""
    disks = {
        (int((size/2) - 1), int((size/2)-1)): "x",
        (int(size/2),int(size/2)): "x",
        (int((size/2) - 1),int(size/2)): "o",
        (int(size/2),int((size/2)-1)): "o"
        }
    return disks

def ask_for_coordinates(disks, symbol):
    """Ask for the line and the column, where the player wants to play. Returns coordinates (tuple)."""
    print("Player with {}, where do you want to play?".format(symbol))
    x = int(input("Write line"))
    y = int(input("Write column"))
    coordinates = x, y
    return coordinates

def check_coordinates(disks, new):
    """Check, if the new coordinate is in the playing area and empty.""" 
    x, y = new

    if x > size or y > size or x < 0 or y < 0: 
        raise ValueError("These coordinates are out of the playing area.")
    elif new in disks: 
        raise ValueError("Here already is a disc.")
    else: 
        return new
    
def check_possible_move(disks, symbol):
    """Checks if the player has possible moves. Returns True (there is at least one possible move) or False (there is not possible move for the symbol). """
    state = False
    for x in range(size):
        for y in range(size):
            coordinate = x, y
            if coordinate not in disks:
                try: 
                    move(disks, coordinate, symbol)
                    state = True
                    break
                except ValueError:
                    pass
    return state

def check_all_moves(disks):
    """Returns True, when there is no possible move for any of the symbols."""
    return check_possible_move(disks, "x") == False and check_possible_move(disks, "o") == False

def player_move(disks, symbol):
    """Realizes a player move. 
    
    Looks up possible moves, asks for new coordinates, finds all changing discs, and reverses them. 
    If there is no possible move, then it prints a notice and skips the move.
    """

    if check_possible_move(disks, symbol):
        while True: 
            try:
                new = ask_for_coordinates(disks, symbol)
                new = check_coordinates(disks, new)
                changes = move(disks, new, symbol)
                reversal(disks, new, symbol, changes)
                break
            except ValueError as e: 
                print(e)    
    else: 
        print("You cannot play.")

def end(disks):
    """Returns True when the playing area is full or there is only one sort of symbol left. """
    return len(disks) == size*size or "x" not in disks.values() or "o" not in disks.values() 

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
        disks = create_beginning_disks()
    
    #cycle alternating moves of two players
    while not end(disks):
        show_playing_area(disks)
        player_move(disks, "x")
        
        show_playing_area(disks)
        player_move(disks, "o")

        if check_all_moves(disks):
            break

        deposit = json.dumps(code_json(disks))
        with open("othello_disks.json", "w", encoding="utf-8") as e: 
            print(deposit, file=e)

    #the end of the game - evaluation
    write_score(disks)
    show_playing_area(disks)
    os.remove("othello_disks.json")