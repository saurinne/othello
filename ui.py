import pyglet
import othello
# import util

size = othello.NUMBER_OF_LINES
c = 70
window = pyglet.window.Window(width=size * c, height=size * c)

cerna = pyglet.image.load("cerna.png")
bila = pyglet.image.load("bila.png")
pole = pyglet.image.load("pole.png")

black = pyglet.sprite.Sprite(cerna, x=c, y=c)
white = pyglet.sprite.Sprite(bila, x=c, y=c)
empty = pyglet.sprite.Sprite(pole, x=c, y=c)

disks = othello.create_beginning_disks()

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

window.push_handlers(
    on_draw = show_area
)

# for x in range(size): 
#     for y in range(size): 
#         sprite.draw

pyglet.app.run()