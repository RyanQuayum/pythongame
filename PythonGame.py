from math import gamma

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui, math, time
class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    # Returns a string representation of the vector
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    # Tests the equality of this vector and another
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # Tests the inequality of this vector and another
    def __ne__(self, other):
        return not self.__eq__(other)

    # Returns a tuple with the point corresponding to the vector
    def get_p(self):
        return (self.x, self.y)

    # Returns a copy of the vector
    def copy(self):
        return Vector(self.x, self.y)

    # Adds another vector to this vector
    def add(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __add__(self, other):
        return self.copy().add(other)

    # Negates the vector (makes it point in the opposite direction)
    def negate(self):
        return self.multiply(-1)

    def __neg__(self):
        return self.copy().negate()

    # Subtracts another vector from this vector
    def subtract(self, other):
        return self.add(-other)

    def __sub__(self, other):
        return self.copy().subtract(other)

    # Multiplies the vector by a scalar
    def multiply(self, k):
        self.x *= k
        self.y *= k
        return self

    def __mul__(self, k):
        return self.copy().multiply(k)

    def __rmul__(self, k):
        return self.copy().multiply(k)

    # Divides the vector by a scalar
    def divide(self, k):
        return self.multiply(1 / k)

    def __truediv__(self, k):
        return self.copy().divide(k)

    # Normalizes the vector
    def normalize(self):
        return self.divide(self.length())

    # Returns a normalized version of the vector
    def get_normalized(self):
        return self.copy().normalize()

    # Returns the dot product of this vector with another one
    def dot(self, other):
        return self.x * other.x + self.y * other.y

    # Returns the length of the vector
    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    # Returns the squared length of the vector
    def length_squared(self):
        return self.x ** 2 + self.y ** 2

    # Reflect this vector on a normal
    def reflect(self, normal):
        n = normal.copy()
        n.multiply(2 * self.dot(normal))
        self.subtract(n)
        return self

    # Returns the angle between this vector and another one
    def angle(self, other):
        return math.acos(self.dot(other) / (self.length() * other.length()))

    # Rotates the vector 90 degrees anticlockwise
    def rotate_anti(self):
        self.x, self.y = -self.y, self.x
        return self

    # Rotates the vector according to an angle theta given in radians
    def rotate_rad(self, theta):
        rx = self.x * math.cos(theta) - self.y * math.sin(theta)
        ry = self.x * math.sin(theta) + self.y * math.cos(theta)
        self.x, self.y = rx, ry
        return self

    # Rotates the vector according to an angle theta given in degrees
    def rotate(self, theta):
        theta_rad = theta / 180 * math.pi
        return self.rotate_rad(theta_rad)

    # project the vector onto a given vector
    def get_proj(self, vec):
        unit = vec.get_normalized()
        return unit.multiply(self.dot(unit))

class Spritesheet:
    def __init__(self, img, row, column):
        self.img = simplegui.load_image(img)
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.row = row
        self.column = column
        self.totalSprites = row * column
        self.spriteWidthHeight = (self.width/column, self.height/row)
        self.spriteCentre = (self.spriteWidthHeight[0] / 2, self.height - (self.spriteWidthHeight[1] / 2))
        self.spriteFrame = [0,0]




class Player:
    def __init__(self, pos, spritesheet):
        self.pos = pos
        self.vel = Vector()
        self.spritesheet = spritesheet
        self.playerState = "idle"
        self.centre = (290,43)
        self.dims = (580,86)
        self.frameTime = 0
        self.Interval = 6

    def draw(self, canvas, state):
        if state == "idle":
            centre = self.spritesheet.spriteCentre
            canvas.draw_image(self.spritesheet.img, centre, self.spritesheet.spriteWidthHeight, self.pos.get_p(), self.spritesheet.spriteWidthHeight)
        elif state == "walkRight":
            centrex = (self.spritesheet.spriteFrame[0] + 0.5) * self.spritesheet.spriteWidthHeight[0]
            centrey = (self.spritesheet.spriteFrame[1] + 0.5) * self.spritesheet.spriteWidthHeight[1]
            canvas.draw_image(self.spritesheet.img, (centrex, centrey), self.spritesheet.spriteWidthHeight, self.pos.get_p(), self.spritesheet.spriteWidthHeight)

    def update(self):
        self.pos.add(self.vel)
        self.vel *= 0.90
        self.frameTime += 1
        if self.frameTime >= self.Interval:
            self.frameTime = 0
            self.spritesheet.spriteFrame[0] += 1
            if self.spritesheet.spriteFrame[0] >= self.spritesheet.column:
                self.spritesheet.spriteFrame[0] = 0
                self.spritesheet.spriteFrame[1] += 1
            if self.spritesheet.spriteFrame[1] >= self.spritesheet.row:
                self.spritesheet.spriteFrame[1] = 0


class Keyboard:
    def __init__(self):
        self.right = False
        self.left = False
        self.space = False
    def keyDown(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = True
        if key == simplegui.KEY_MAP['left']:
            self.left = True
        if key == simplegui.KEY_MAP['space']:
            self.space = True
    def keyUp(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = False
        if key == simplegui.KEY_MAP['left']:
            self.left = False
        if key == simplegui.KEY_MAP['space']:
            self.space = False

class interaction:
    def __init__(self):
        pass


class Game:
    def __init__(self):
        self.frame = simplegui.create_frame('Game', 1280, 720)
        self.playersheet = Spritesheet("https://raw.githubusercontent.com/RyanQuayum/pythongame/refs/heads/main/walkSpritesheet.png",1,8)
        self.gameState = "mainMenu"
        self.kbd = Keyboard()
        self.player = Player(Vector(640,360), self.playersheet)
        self.frame.add_button("Start", self.button_handler, 200)
        self.frame.set_draw_handler(self.draw)
        self.frame.set_keydown_handler(self.kbd.keyDown)
        self.frame.set_keyup_handler(self.kbd.keyUp)

    def gamestart(self):
        self.frame.start()

    def button_handler(self): # Start Button Handler
        if self.gameState == "mainMenu":
            self.gameState = "game"

    def keyboardUpdate(self):
        if self.kbd.right:
            self.player.vel.add(Vector(0.5, 0))
            self.player.playerState = "walkRight"
        if self.kbd.left:
            self.player.vel.add(Vector(-0.5, 0))
            self.player.playerState = "walkRight"
        elif not self.kbd.left and not self.kbd.right:
            self.player.playerState = "idle"
            print("Hello")

    def draw(self, canvas):
        if self.gameState == "mainMenu":
            self.frame.set_canvas_background("lightyellow")
            canvas.draw_text('Menu', (540, 300), 50, 'Red')
            canvas.draw_text('Press Start', (540, 350), 28, 'Red')

        elif self.gameState == "game":
            self.frame.set_canvas_background("lightblue")
            self.player.draw(canvas, self.player.playerState)
            self.keyboardUpdate()
            self.player.update()



newgame = Game()
newgame.gamestart()

