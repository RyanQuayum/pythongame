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




class Player:
    def __init__(self, pos):
        self.pos = pos
        self.vel = Vector()
        self.img = simplegui.load_image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/Solid_red.svg/1024px-Solid_red.svg.png")
        self.centre = (512,512)
        self.dims = (1024,1024)

    def draw(self, canvas):
        canvas.draw_image(self.img, self.centre, self.dims, self.pos.get_p(), (64,64))

    def update(self):
        self.pos.add(self.vel)
        self.vel *= 0.90



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
    def __init__(self, player, keyboard):
        self.player = player
        self.keyboard = keyboard
        self.state = "mainMenu"
    def update(self):
        if self.keyboard.right:
            self.player.vel.add(Vector(1, 0))
        if self.keyboard.left:
            self.player.vel.add(Vector(-1, 0))

    def button_handler(self): # Start Button Handler
        if self.state == "mainMenu":
            self.state = "game"


kbd = Keyboard()
frame = simplegui.create_frame('Game', 1280, 720)
player = Player(Vector(640,360))
interact = interaction(player, kbd)

def draw(canvas):
    if interact.state == "mainMenu":
        frame.set_canvas_background("lightyellow")
        canvas.draw_text('Menu', (540, 300), 50, 'Red')
        canvas.draw_text('Press Start', (540, 350), 28, 'Red')
    elif interact.state == "game":
        frame.set_canvas_background("lightblue")
        player.draw(canvas)
        interact.update()
        player.update()


frame.add_button("Start", interact.button_handler, 200)
frame.set_draw_handler(draw)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)
frame.start()

