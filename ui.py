from pyglet.window.key import MOD_OPTION
from util import reversal
import pyglet
import othello
import util

size = othello.size
c = 100
state = [True]
b = pyglet.window.mouse.LEFT
m = MOD_OPTION

window = pyglet.window.Window(width=size * c, height=size * c)

cerna = pyglet.image.load("cerna.png")
bila = pyglet.image.load("bila.png")
pole = pyglet.image.load("pole.png")

black = pyglet.sprite.Sprite(cerna, x=c, y=c)
white = pyglet.sprite.Sprite(bila, x=c, y=c)
empty = pyglet.sprite.Sprite(pole, x=c, y=c)

disks = othello.create_beginning_disks()

def get_symbol(): 
    if state[-1]: 
        symbol = "o"
    else: 
        symbol = "x"

    return symbol

def change_player(): 
    if state[-1]: 
        state.append(False)
    else: 
        state.append(True)

def show_area(): 
    window.clear()
    for x in range(size): 
        for y in range(size):
            coordinate = x, y
            if coordinate not in disks:  
                empty.x = x * c
                empty.y = y * c
                empty.draw()
            elif disks[coordinate] == "x": 
                black.x = x * c
                black.y = y * c
                black.draw()
            elif disks[coordinate] == "o": 
                white.x = x * c
                white.y = y * c
                white.draw()

def get_coordinates(x, y): 
    s = min(window.width, window.height)/size
    line = int(x/s)
    column = int(y/s)
    return line, column


def click_play(x, y, b, m): 
    if othello.end(disks) or othello.end(disks): 
        othello.write_score(disks)
        raise SystemExit("End")

    symbol = get_symbol()

    if othello.check_possible_move(disks, symbol):
        try:
            new_coordinate = get_coordinates(x, y)
            changes = util.move(disks, new_coordinate, symbol)
            util.reversal(disks, new_coordinate, symbol, changes)
            change_player()
        except ValueError as e: 
            print(e)    
    else: 
        print("You cannot play.")
        change_player()

def show_color(): 
    """ Idea - ukáže, zda je tah možný"""
    pass

window.push_handlers(
    on_draw = show_area,
    on_mouse_release = click_play
)


pyglet.app.run()