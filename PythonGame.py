
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui, math, time
# from SimpleGUICS2Pygame.example.Mandelbrot_Set import frame


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

class attackSpritesheet(Spritesheet):
    def __init__(self, img, row, column, frameWidths):
        super().__init__(img, row, column)
        self.frameWidths = frameWidths

class Player:
    def __init__(self, pos, rightSpritesheet, leftSpriteSheet, attackRightSpriteSheet, attackLeftSpriteSheet):
        self.pos = pos
        self.vel = Vector()
        self.rightSpritesheet = rightSpritesheet
        self.leftSpritesheet = leftSpriteSheet
        self.attackRightSpriteSheet = attackRightSpriteSheet
        self.attackLeftSpriteSheet = attackLeftSpriteSheet
        self.playerState = "idle"
        self.attackFrame = 0
        self.centre = (290,43)
        self.dims = (580,86)
        self.frameTime = 0
        self.Interval = 7
        self.playerDirection = "Right"

    def draw(self, canvas, state):

        if state == "idle":
            if self.playerDirection == "Right":
                centre = (self.rightSpritesheet.spriteCentre[0] + self.rightSpritesheet.spriteWidthHeight[0], self.rightSpritesheet.spriteCentre[1])
                canvas.draw_image(self.rightSpritesheet.img, centre, self.rightSpritesheet.spriteWidthHeight, self.pos.get_p(), self.rightSpritesheet.spriteWidthHeight)
            elif self.playerDirection == "Left":
                centre = (self.leftSpritesheet.spriteCentre[0] + self.leftSpritesheet.spriteWidthHeight[0], self.leftSpritesheet.spriteCentre[1])
                canvas.draw_image(self.leftSpritesheet.img, centre, self.leftSpritesheet.spriteWidthHeight, self.pos.get_p(), self.leftSpritesheet.spriteWidthHeight)

        if state == "attack":
            if self.playerDirection == "Right":
                total_width = sum(self.attackRightSpriteSheet.frameWidths[0:self.attackFrame])
                centrex = total_width + (self.attackRightSpriteSheet.frameWidths[self.attackFrame] / 2)
                centrey = self.attackRightSpriteSheet.spriteWidthHeight[1] / 2
                width_height_dest = (self.attackRightSpriteSheet.frameWidths[self.attackFrame],
                                     self.attackRightSpriteSheet.spriteWidthHeight[1])
                canvas.draw_image(self.attackRightSpriteSheet.img, (centrex, centrey), width_height_dest, self.pos.get_p(), width_height_dest)
            elif self.playerDirection == "Left":
                total_width = sum(self.attackRightSpriteSheet.frameWidths[0:self.attackFrame])
                centrex = total_width + (self.attackRightSpriteSheet.frameWidths[self.attackFrame] / 2)
                centrey = self.attackRightSpriteSheet.spriteWidthHeight[1] / 2
                width_height_dest = (self.attackRightSpriteSheet.frameWidths[self.attackFrame],
                                     self.attackRightSpriteSheet.spriteWidthHeight[1])
                canvas.draw_image(self.attackLeftSpriteSheet.img, (centrex, centrey), width_height_dest, self.pos.get_p(), width_height_dest)



        elif state == "walkRight":
            centrex = (self.rightSpritesheet.spriteFrame[0] + 0.5) * self.rightSpritesheet.spriteWidthHeight[0]
            centrey = (self.rightSpritesheet.spriteFrame[1] + 0.5) * self.rightSpritesheet.spriteWidthHeight[1]
            canvas.draw_image(self.rightSpritesheet.img, (centrex, centrey), self.rightSpritesheet.spriteWidthHeight, self.pos.get_p(), self.rightSpritesheet.spriteWidthHeight)
        elif state == "walkLeft":
            centrex = (self.leftSpritesheet.spriteFrame[0] + 0.5) * self.leftSpritesheet.spriteWidthHeight[0]
            centrey = (self.leftSpritesheet.spriteFrame[1] + 0.5) * self.leftSpritesheet.spriteWidthHeight[1]
            canvas.draw_image(self.leftSpritesheet.img, (centrex, centrey), self.leftSpritesheet.spriteWidthHeight, self.pos.get_p(), self.leftSpritesheet.spriteWidthHeight)



    def update(self):
        self.pos.add(self.vel)

        self.vel *= 0.90
        self.frameTime += 1
        if self.frameTime >= self.Interval:
            self.frameTime = 0
            if self.playerState == "attack":
                self.attackFrame += 1
                if self.attackFrame == 4:
                    self.attackFrame = 0
                    self.playerState = "idle"
            self.rightSpritesheet.spriteFrame[0] += 1
            self.leftSpritesheet.spriteFrame[0] += 1
            if self.rightSpritesheet.spriteFrame[0] >= self.rightSpritesheet.column:
                self.rightSpritesheet.spriteFrame[0] = 0
                self.rightSpritesheet.spriteFrame[1] += 1
            if self.rightSpritesheet.spriteFrame[1] >= self.rightSpritesheet.row:
                self.rightSpritesheet.spriteFrame[1] = 0
            if self.leftSpritesheet.spriteFrame[0] >= self.leftSpritesheet.column:
                self.leftSpritesheet.spriteFrame[0] = 0
                self.leftSpritesheet.spriteFrame[1] += 1
            if self.leftSpritesheet.spriteFrame[1] >= self.leftSpritesheet.row:
                self.leftSpritesheet.spriteFrame[1] = 0



class Keyboard:
    def __init__(self):
        self.right = False
        self.left = False
        self.space = False
        self.attack = False
    def keyDown(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = True
        if key == simplegui.KEY_MAP['left']:
            self.left = True
        if key == simplegui.KEY_MAP['space']:
            self.space = True
        if key == simplegui.KEY_MAP['x']:
            self.attack = True
    def keyUp(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = False
        if key == simplegui.KEY_MAP['left']:
            self.left = False
        if key == simplegui.KEY_MAP['space']:
            self.space = False
        if key == simplegui.KEY_MAP['x']:
            self.attack = False

class interaction:
    def __init__(self):
        pass



class Game:
    def __init__(self):
        self.frame = simplegui.create_frame('Game', 1280, 720)
        self.rightPlayersheet = Spritesheet("https://raw.githubusercontent.com/RyanQuayum/pythongame/refs/heads/main/walkSpritesheet.png",1,8)
        self.leftPlayersheet = Spritesheet("https://raw.githubusercontent.com/RyanQuayum/pythongame/refs/heads/main/newLeftSpritewalksheet.png", 1, 8)
        self.attack1RightPlayersheet = attackSpritesheet("https://raw.githubusercontent.com/RyanQuayum/pythongame/refs/heads/main/attack1RightSpritesheet.png", 1, 4, [48,49,85,80])
        self.attack1LeftPlayersheet = attackSpritesheet("https://raw.githubusercontent.com/RyanQuayum/pythongame/refs/heads/main/leftAttackSpritesheet.png", 1, 4, [48, 48, 84, 80])
        self.gameState = "mainMenu"
        self.kbd = Keyboard()
        self.player = Player(Vector(640,360), self.rightPlayersheet, self.leftPlayersheet, self.attack1RightPlayersheet, self.attack1LeftPlayersheet)
        self.button = self.frame.add_button("Start", self.button_handler, 200)
        self.frame.set_draw_handler(self.draw)
        self.frame.set_keydown_handler(self.kbd.keyDown)
        self.frame.set_keyup_handler(self.kbd.keyUp)

    def gamestart(self):
        self.frame.start()

    def button_handler(self): # Start Button Handler
        if self.gameState == "mainMenu":
            self.gameState = "game"
            self.button.set_text("Menu")
        elif self.gameState == "game":
            self.gameState = "mainMenu"
            self.button.set_text("Start")

    def keyboardUpdate(self):
        if self.kbd.right:
            self.player.vel.add(Vector(0.5, 0))
            self.player.playerState = "walkRight"
            self.player.playerDirection = "Right"
        elif self.kbd.left:
            self.player.vel.add(Vector(-0.5, 0))
            self.player.playerState = "walkLeft"
            self.player.playerDirection = "Left"
        elif self.kbd.attack:
            self.player.playerState = "attack"
        elif not self.kbd.left and not self.kbd.right and not self.player.attackFrame == 0:
            self.player.playerState = "idle"

    def draw(self, canvas):
        if self.gameState == "mainMenu":
            self.frame.set_canvas_background("lightyellow")
            canvas.draw_text('Mystic Flare', (470, 300), 50, 'Red')
            canvas.draw_text('Press Start', (540, 350), 28, 'Red')

        elif self.gameState == "game":
            self.frame.set_canvas_background("lightblue")
            self.player.draw(canvas, self.player.playerState)
            self.keyboardUpdate()
            self.player.update()
            print(self.player.playerState)




newgame = Game()
newgame.gamestart()

