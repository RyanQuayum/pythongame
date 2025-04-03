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

class Keyboard:
    def __init__(self):
        self.right = False
        self.left = False
        self.space = False
        self.attack = False
        self.up = False
        self.down = False
    def keyDown(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = True
        if key == simplegui.KEY_MAP['left']:
            self.left = True
        if key == simplegui.KEY_MAP['space']:
            self.space = True
        if key == simplegui.KEY_MAP['x']:
            self.attack = True
        if key == simplegui.KEY_MAP['up']:
            self.up = True
        if key == simplegui.KEY_MAP['down']:
            self.down = True
    def keyUp(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = False
        if key == simplegui.KEY_MAP['left']:
            self.left = False
        if key == simplegui.KEY_MAP['space']:
            self.space = False
        if key == simplegui.KEY_MAP['x']:
            self.attack = False
        if key == simplegui.KEY_MAP['up']:
            self.up = False
        if key == simplegui.KEY_MAP['down']:
            self.down = False

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
        self.centre = (290,32)
        self.dims = (580,64)
        self.frameTime = 0
        self.Interval = 7
        self.playerDirection = "Right"
        self.grounded = False
        self.on_ladder = False
        self.hasKey = False
        self.immunityFrames = 75
        self.Hit = False

        # self.playerLeftOffset = for scalability of character later




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
        if not self.grounded and self.vel.y < 5 and not self.on_ladder: # Gravity
            self.vel.y += 0.5





        if self.Hit: #Immunity Frame Checker, cannot be hit while less than 75
            self.immunityFrames -= 1
            if self.immunityFrames == 0:
                self.Hit = False
                self.immunityFrames = 75

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

#If statements progresses the active sprite in the spritesheet

class enemy(Player):
    def __init__(self, pos,  rightSpritesheet, leftSpriteSheet, attackRightSpriteSheet, attackLeftSpriteSheet, idleSpriteSheet, idleLeftSpriteSheet, deadRightSpriteSheet, deadLeftSpriteSheet, hitRightSpriteSheet, hitLeftSpriteSheet, attackFrames):
        super().__init__(pos, rightSpritesheet, leftSpriteSheet, attackRightSpriteSheet, attackLeftSpriteSheet)
        self.attackFrames = attackFrames
        self.vel = Vector()
        self.idleSpriteSheet = idleSpriteSheet
        self.idleLeftSpriteSheet = idleLeftSpriteSheet
        self.deadRightSpriteSheet = deadRightSpriteSheet
        self.deadLeftSpriteSheet = deadLeftSpriteSheet
        self.hitRightSpriteSheet = hitRightSpriteSheet
        self.hitLeftSpriteSheet = hitLeftSpriteSheet
        self.playerDirection = "Right"
        self.life = 2
        self.hit = False
        self.immunityFrames = 75
        self.dead = False
        self.deadTimer = 55
        self.arrowLaunched = False
        self.arrowTimer = 75

    def draw(self, canvas):

        if self.life <= 0 and self.deadTimer > 0:
            if self.playerDirection == "Right":
                centrex = (self.deadRightSpriteSheet.spriteFrame[0] + 0.5) * self.deadRightSpriteSheet.spriteWidthHeight[0]
                centrey = (self.deadRightSpriteSheet.spriteFrame[1] + 0.5) * self.deadRightSpriteSheet.spriteWidthHeight[1]
                canvas.draw_image(self.deadRightSpriteSheet.img, (centrex, centrey), self.deadRightSpriteSheet.spriteWidthHeight,
                                  self.pos.get_p(), (self.deadRightSpriteSheet.spriteWidthHeight[0] * 2,
                                                     self.deadRightSpriteSheet.spriteWidthHeight[1] * 2))


            elif self.playerDirection == "Left":
                centrex = (self.deadLeftSpriteSheet.spriteFrame[0] + 0.5) * self.deadLeftSpriteSheet.spriteWidthHeight[0]
                centrey = (self.deadLeftSpriteSheet.spriteFrame[1] + 0.5) * self.deadLeftSpriteSheet.spriteWidthHeight[1]
                canvas.draw_image(self.deadLeftSpriteSheet.img, (centrex, centrey), self.deadLeftSpriteSheet.spriteWidthHeight,
                                  self.pos.get_p(), (self.deadLeftSpriteSheet.spriteWidthHeight[0] * 2,
                                                     self.deadLeftSpriteSheet.spriteWidthHeight[1] * 2))
            return


        if self.hit:
            if self.playerDirection == "Right":
                centrex = (self.hitRightSpriteSheet.spriteFrame[0] + 0.5) * self.hitRightSpriteSheet.spriteWidthHeight[0]
                centrey = (self.hitRightSpriteSheet.spriteFrame[1] + 0.5) * self.hitRightSpriteSheet.spriteWidthHeight[1]
                canvas.draw_image(self.hitRightSpriteSheet.img, (centrex, centrey), self.hitRightSpriteSheet.spriteWidthHeight,
                                  self.pos.get_p(), (self.hitRightSpriteSheet.spriteWidthHeight[0] * 2,
                                                     self.hitRightSpriteSheet.spriteWidthHeight[1] * 2))

            elif self.playerDirection == "Left":
                centrex = (self.hitLeftSpriteSheet.spriteFrame[0] + 0.5) * self.hitLeftSpriteSheet.spriteWidthHeight[0]
                centrey = (self.hitLeftSpriteSheet.spriteFrame[1] + 0.5) * self.hitLeftSpriteSheet.spriteWidthHeight[1]
                canvas.draw_image(self.hitLeftSpriteSheet.img, (centrex, centrey), self.hitLeftSpriteSheet.spriteWidthHeight,
                                  self.pos.get_p(), (self.hitLeftSpriteSheet.spriteWidthHeight[0] * 2,
                                                     self.hitLeftSpriteSheet.spriteWidthHeight[1] * 2))
            return



        if self.playerState == "idle":
            if self.playerDirection == "Right":
                centrex = (self.idleSpriteSheet.spriteFrame[0] + 0.5) * self.idleSpriteSheet.spriteWidthHeight[0]
                centrey = (self.idleSpriteSheet.spriteFrame[1] + 0.5) * self.idleSpriteSheet.spriteWidthHeight[1]
                canvas.draw_image(self.idleSpriteSheet.img, (centrex, centrey), self.idleSpriteSheet.spriteWidthHeight, self.pos.get_p(), (self.idleSpriteSheet.spriteWidthHeight[0]*2, self.idleSpriteSheet.spriteWidthHeight[1]*2))

            elif self.playerDirection == "Left":

                centrex = (self.idleLeftSpriteSheet.column - 1 - self.idleLeftSpriteSheet.spriteFrame[0] + 0.5) * self.idleLeftSpriteSheet.spriteWidthHeight[0]
                centrey = (self.idleLeftSpriteSheet.spriteFrame[1] + 0.5) * self.idleLeftSpriteSheet.spriteWidthHeight[1]
                canvas.draw_image(self.idleLeftSpriteSheet.img, (centrex, centrey), self.idleLeftSpriteSheet.spriteWidthHeight,
                                  self.pos.get_p(), (self.idleLeftSpriteSheet.spriteWidthHeight[0] * 2,
                                                     self.idleLeftSpriteSheet.spriteWidthHeight[1] * 2))
        elif self.playerState == "attack":
            if self.playerDirection == "Right":
                centrex = (self.attackFrame + 0.5) * self.attackRightSpriteSheet.spriteWidthHeight[0]
                centrey = (self.attackRightSpriteSheet.spriteFrame[1] + 0.5) * self.attackRightSpriteSheet.spriteWidthHeight[1]
                canvas.draw_image(self.attackRightSpriteSheet.img, (centrex, centrey), self.attackRightSpriteSheet.spriteWidthHeight,
                                  self.pos.get_p(), (self.attackRightSpriteSheet.spriteWidthHeight[0] * 2,
                                                     self.attackRightSpriteSheet.spriteWidthHeight[1] * 2))
            elif self.playerDirection == "Left":
                centrex = (self.attackLeftSpriteSheet.column - 1 - self.attackFrame + 0.5) * self.attackLeftSpriteSheet.spriteWidthHeight[0]
                centrey = (self.attackLeftSpriteSheet.spriteFrame[1] + 0.5) * self.attackLeftSpriteSheet.spriteWidthHeight[1]
                canvas.draw_image(self.attackLeftSpriteSheet.img, (centrex, centrey), self.attackLeftSpriteSheet.spriteWidthHeight,
                                  self.pos.get_p(), (self.attackLeftSpriteSheet.spriteWidthHeight[0] * 2,
                                                     self.attackLeftSpriteSheet.spriteWidthHeight[1] * 2))




    def update(self):

        self.vel *= 0.90

        self.frameTime += 1

        if self.life <= 0:
            self.deadTimer -= 1
            if self.deadTimer <= 0:
                self.dead = True
                print("Enemy has passed away")

        if self.arrowLaunched:
            self.arrowTimer -= 1
            if self.arrowTimer == 0:
                self.arrowLaunched = False
                self.arrowTimer = 75



        if self.hit:
            self.playerState = "idle"
            self.immunityFrames -= 1
            if self.immunityFrames == 0:
                self.playerState = "idle"
                self.hit = False
                self.life -= 1
                self.immunityFrames = 75

# the 3 if statements above are timers to stop repeated functions


        if self.frameTime >= self.Interval:
            self.frameTime = 0
            if self.playerState == "attack":
                self.attackFrame += 1
                if self.attackFrame == self.attackFrames:
                    self.attackFrame = 0
                    self.playerState = "idle"
            self.rightSpritesheet.spriteFrame[0] += 1
            self.leftSpritesheet.spriteFrame[0] += 1
            self.idleSpriteSheet.spriteFrame[0] += 1
            self.idleLeftSpriteSheet.spriteFrame[0] += 1
            self.attackRightSpriteSheet.spriteFrame[0] += 1
            self.attackLeftSpriteSheet.spriteFrame[0] += 1
            self.hitRightSpriteSheet.spriteFrame[0] += 1
            self.hitLeftSpriteSheet.spriteFrame[0] += 1
            self.deadRightSpriteSheet.spriteFrame[0] += 1
            self.deadLeftSpriteSheet.spriteFrame[0] += 1


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

            if self.idleSpriteSheet.spriteFrame[0] >= self.idleSpriteSheet.column:
                self.idleSpriteSheet.spriteFrame[0] = 0
                self.idleSpriteSheet.spriteFrame[1] += 1
            if self.idleSpriteSheet.spriteFrame[1] >= self.idleSpriteSheet.row:
                self.idleSpriteSheet.spriteFrame[1] = 0

            if self.idleLeftSpriteSheet.spriteFrame[0] >= self.idleLeftSpriteSheet.column:
                self.idleLeftSpriteSheet.spriteFrame[0] = 0
                self.idleLeftSpriteSheet.spriteFrame[1] += 1
            if self.idleLeftSpriteSheet.spriteFrame[1] >= self.idleLeftSpriteSheet.row:
                self.idleLeftSpriteSheet.spriteFrame[1] = 0

            if self.attackRightSpriteSheet.spriteFrame[0] >= self.attackRightSpriteSheet.column:
                self.attackRightSpriteSheet.spriteFrame[0] = 0
                self.attackRightSpriteSheet.spriteFrame[1] += 1
            if self.attackRightSpriteSheet.spriteFrame[1] >= self.attackRightSpriteSheet.row:
                self.attackRightSpriteSheet.spriteFrame[1] = 0

            if self.attackLeftSpriteSheet.spriteFrame[0] >= self.attackLeftSpriteSheet.column:
                self.attackLeftSpriteSheet.spriteFrame[0] = 0
                self.attackLeftSpriteSheet.spriteFrame[1] += 1
            if self.attackLeftSpriteSheet.spriteFrame[1] >= self.attackLeftSpriteSheet.row:
                self.attackLeftSpriteSheet.spriteFrame[1] = 0

            if self.hitRightSpriteSheet.spriteFrame[0] >= self.hitRightSpriteSheet.column:
                self.hitRightSpriteSheet.spriteFrame[0] = 0
                self.hitRightSpriteSheet.spriteFrame[1] += 1
            if self.hitRightSpriteSheet.spriteFrame[1] >= self.hitRightSpriteSheet.row:
                self.hitRightSpriteSheet.spriteFrame[1] = 0

            if self.hitLeftSpriteSheet.spriteFrame[0] >= self.hitLeftSpriteSheet.column:
                self.hitLeftSpriteSheet.spriteFrame[0] = 0
                self.hitLeftSpriteSheet.spriteFrame[1] += 1
            if self.hitLeftSpriteSheet.spriteFrame[1] >= self.hitLeftSpriteSheet.row:
                self.hitLeftSpriteSheet.spriteFrame[1] = 0

            if self.deadRightSpriteSheet.spriteFrame[0] >= self.deadRightSpriteSheet.column:
                self.deadRightSpriteSheet.spriteFrame[0] = 0
                self.deadRightSpriteSheet.spriteFrame[1] += 1
            if self.deadRightSpriteSheet.spriteFrame[1] >= self.deadRightSpriteSheet.row:
                self.deadRightSpriteSheet.spriteFrame[1] = 0

            if self.deadLeftSpriteSheet.spriteFrame[0] >= self.deadLeftSpriteSheet.column:
                self.deadLeftSpriteSheet.spriteFrame[0] = 0
                self.deadLeftSpriteSheet.spriteFrame[1] += 1
            if self.deadLeftSpriteSheet.spriteFrame[1] >= self.deadLeftSpriteSheet.row:
                self.deadLeftSpriteSheet.spriteFrame[1] = 0

class rangedEnemy(enemy):
    def __init__(self, pos,  rightSpritesheet, leftSpriteSheet, attackRightSpriteSheet, attackLeftSpriteSheet, idleSpriteSheet, idleLeftSpriteSheet, deadRightSpriteSheet, deadLeftSpriteSheet, hitRightSpriteSheet, hitLeftSpriteSheet, attackFrames):
        super().__init__(pos, rightSpritesheet, leftSpriteSheet, attackRightSpriteSheet, attackLeftSpriteSheet, idleSpriteSheet, idleLeftSpriteSheet, deadRightSpriteSheet, deadLeftSpriteSheet, hitRightSpriteSheet, hitLeftSpriteSheet, attackFrames)


class inviswall:
    def __init__(self, xcorner, ycorner, width, height):
        self.xcorner = xcorner
        self.ycorner = ycorner
        self.width = width
        self.height = height
        self.left = xcorner
        self.right = xcorner + width
        self.top = ycorner
        self.bottom = ycorner + height
        self.centreX = xcorner + (width / 2)
        self.centreY = ycorner + (height / 2)
        self.halfwidth = (42 + width) / 2
        self.halfheight = (64 + height) / 2
        self.topleft = Vector(xcorner, ycorner)
        self.topright = Vector(xcorner + width, ycorner)
        self.bottomleft = Vector(xcorner, ycorner + height)
        self.bottomright = Vector(xcorner + width, ycorner + height)

    def draw(self, canvas):
        canvas.draw_polygon([(self.xcorner, self.ycorner),
                             (self.xcorner + self.width, self.ycorner),
                             (self.xcorner + self.width, self.ycorner + self.height),
                             (self.xcorner, self.ycorner + self.height)],
                              1, 'Red')



class interaction:
    def __init__(self, polygons, player, kbd, lifesystem, interactables, enemies, scoresystem, projectiles, arrow):
        self.polygons = polygons
        self.player = player
        self.kbd = kbd
        self.lifesystem = lifesystem
        self.scoresystem = scoresystem
        self.interactables = interactables
        self.ladderTimer = 0
        self.enemies = enemies
        self.projectiles = projectiles
        self.arrow = arrow

    def draw(self, canvas):
        self.update()
        for polygon in self.polygons: #Polygon dimensions here smth like that
            polygon.draw(canvas)
        for interact in self.interactables:
            interact.draw(canvas)






############## Enemy React for distance reaction, enemy hit for attack animation/type (fireball or arrow...)

    def enemyReact(self, enemy):
        if enemy.playerState == "attack":
            return None
        if str(type(enemy)) == "<class '__main__.rangedEnemy'>":
            if abs(enemy.pos.x - self.player.pos.x) < 250 and abs(enemy.pos.y - self.player.pos.y) < 5:
                if enemy.pos.x  < self.player.pos.x:
                  enemy.playerDirection = "Right"
                elif enemy.pos.x > self.player.pos.x:
                  enemy.playerDirection = "Left"
                enemy.playerState = "attack"
            elif abs(enemy.pos.x - self.player.pos.x) > 250 and abs(enemy.pos.y - self.player.pos.y) > 5:
                enemy.playerState = "idle"
        else:
            if abs(enemy.pos.x - self.player.pos.x) < 80 and abs(enemy.pos.y - self.player.pos.y) < 5:
                if enemy.pos.x  < self.player.pos.x:
                  enemy.playerDirection = "Right"
                elif enemy.pos.x > self.player.pos.x:
                  enemy.playerDirection = "Left"
                enemy.playerState = "attack"
            elif abs(enemy.pos.x - self.player.pos.x) > 20 and abs(enemy.pos.y - self.player.pos.y) > 5:
                enemy.playerState = "idle"
            else:
                return None




    def playerGroundCollide(self, poly, player):
        playerBottomOffset = player.pos.y + 32
        playerLeftOffset = player.pos.x - 21
        playerRightOffset = player.pos.x + 21

        if (playerRightOffset > poly.xcorner and playerLeftOffset < poly.right) and (
                playerBottomOffset <= poly.top+5 and playerBottomOffset >= poly.top-5):
            self.player.grounded = True
            # Place player on top of the platform and stop downward movement (vel.y = 0)
            player.pos.y = poly.top - 32  # Adjust position to rest on platform (centre + offset above platform top)
            player.vel.y = 0  # Stop downward movement
            return True  # Collision detected
        else:
            return False  # Nada collision



    def playerLeftWallCollide(self, poly, player):
        playerBottomOffset = player.pos.y + 32
        playerTopOffset = player.pos.y - 32
        playerRightOffset = player.pos.x + 21
        if (playerBottomOffset > poly.ycorner or playerTopOffset < poly.bottom) and (
                playerRightOffset <= poly.left + 2 and playerRightOffset >= poly.left - 2):

            player.pos.x = poly.left - 24  # Adjust position to rest on platform
            player.vel.x = 0  # Stop downward velocity (gravity)
            return True  # Collision detected
        else:
            return False  # No collision

    def playerRightWallCollide(self, poly, player):
        playerBottomOffset = player.pos.y + 32
        playerTopOffset = player.pos.y - 32
        playerLeftOffset = player.pos.x - 21
        if (playerBottomOffset > poly.ycorner or playerTopOffset < poly.bottom) and (
                playerLeftOffset <= poly.right + 2 and playerLeftOffset >= poly.right - 2):

            player.pos.x = poly.right + 24  # Adjust position to rest on platform
            player.vel.x = 0  # Stop downward velocity (gravity)
            return True  # Collision detected
        else:
            return False  # No collision


    def playerRoofCollide(self, poly, player):
        playerLeftOffset = player.pos.x - 21
        playerRightOffset = player.pos.x + 21
        playerTopoffset = player.pos.y - 32


        if (playerRightOffset > poly.xcorner and playerLeftOffset < poly.right) and (
                playerTopoffset <= poly.bottom+5 and playerTopoffset >= poly.bottom-5):
            # Place player on top of the platform and stop downward movement (y velocity)
            player.pos.y = poly.bottom + 38  # Adjust position to rest on platform
            player.vel.y = 0  # Stop downward velocity (gravity)
            return True  # Collision detected
        else:
            return False  # No collision



    def wallOrGround(self, poly):

        distanceX = self.player.pos.get_p()[0] - poly.centreX
        distanceY = self.player.pos.get_p()[1] - poly.centreY

        overlapX = poly.halfwidth - abs(distanceX)
        overlapY = poly.halfheight - abs(distanceY)

        if overlapX < overlapY:
            if distanceX > 0:
                return "right"
            else:
                return "left"
        else:
            if distanceY > 0:
                return "bottom"
            else:
                return "top"


    def is_colliding(self, poly):
        # Get the player and platform bounding boxes
        player_left = self.player.pos.x - 21
        player_right = self.player.pos.x + 21
        player_top = self.player.pos.y - 32
        player_bottom = self.player.pos.y + 32


        # Check for overlap in both X and Y axes

        return (player_right > poly.left and player_left < poly.right) or (player_bottom > poly.top and player_top < poly.bottom)

    def update(self): #Checks for gravity # Initially assume the player is not grounded

        self.player.grounded = False
        for poly in self.polygons:
            if self.is_colliding(poly):
                if self.wallOrGround(poly) == "top":
                    self.playerGroundCollide(poly, self.player)
                elif self.wallOrGround(poly) == "left":
                    self.playerLeftWallCollide(poly, self.player)
                elif self.wallOrGround(poly) == "right":
                    self.playerRightWallCollide(poly, self.player)
                elif self.wallOrGround(poly) == "bottom":
                    self.playerRoofCollide(poly, self.player)
        self.player.on_ladder = False
        for interact in self.interactables:
            if self.is_colliding(interact):
                self.interactableCollision(interact, self.player, self.lifesystem, self.scoresystem)
                if self.interactableCollision(interact, self.player, self.lifesystem, self.scoresystem) == "levelFinish":
                    return "levelFinish"


 # Gravity effect (pull down)
        if self.kbd.space:
            if self.player.on_ladder:
                self.player.vel.y = -15
                self.player.on_ladder = False
                self.ladderTimer = 100

        # Jumping:
            elif self.player.grounded:
                self.player.vel.y = -20  # Jump velocity (negative = upwards)
                self.player.grounded = False  # Prevent double jumping after initial jump
            else:
                pass
        # Update player position with velocity
        if self.ladderTimer > 0:
            self.ladderTimer -= 1


        if self.player.on_ladder:
            if self.kbd.up:
                self.player.vel.y = -5
            elif self.kbd.down:
                self.player.vel.y = 5



    def enemyHit(self, player, enemy):
        playerBottomOffset = player.pos.y + 32
        playerLeftOffset = player.pos.x - 21
        playerRightOffset = player.pos.x + 18
        playerTopOffset = player.pos.y - 32
        enemyRightOffset = enemy.pos.x + 10
        enemyLeftOffset = enemy.pos.x - 10
        if str(type(enemy)) == "<class '__main__.rangedEnemy'>":
            if enemy.playerState == "attack":
                enemyposx = enemy.pos.x
                enemyposy = enemy.pos.y
                if enemy.playerDirection == "Right":
                    if enemy.attackFrame == 8 and enemy.arrowTimer == 75:
                        self.projectiles.append(projectile(Vector(enemyposx, enemyposy), "arrow",self.arrow, 1, self.player, (14,3.5), (28,7)))
                        enemy.arrowLaunched = True
                if enemy.playerDirection == "Left" and enemy.arrowTimer == 75:
                    if enemy.attackFrame == 8:
                        self.projectiles.append(projectile(Vector(enemyposx, enemyposy), "arrow",self.arrow, -1, self.player, (14,3.5), (28,7)))
                        enemy.arrowLaunched = True
        else:
            if enemy.playerState != "attack" or player.immunityFrames < 75:
                return False
            elif enemy.playerState == "attack":
                if enemy.playerDirection == "Right":
                    if enemy.attackFrame == 8:
                        if (playerLeftOffset >= enemyRightOffset and playerLeftOffset <= enemyRightOffset + 35) or (playerRightOffset >= enemyRightOffset and playerRightOffset <= enemyRightOffset + 35):
                            player.Hit = True
                            self.lifesystem.damage()
                            player.vel.y += 0.75
                            player.vel.x += 1
                elif enemy.playerDirection == "Left":
                    if enemy.attackFrame == 8:
                        if (playerLeftOffset <= enemyLeftOffset and playerLeftOffset <= enemyLeftOffset + 35) or (playerRightOffset <= enemyLeftOffset and playerRightOffset <= enemyLeftOffset - 35):
                            player.Hit = True
                            self.lifesystem.damage()
                            player.vel.y += 0.75
                            player.vel.x += -1

    def playerAttack(self, player, enemy):
        playerLeftOffset = player.pos.x - 43
        playerRightOffset = player.pos.x + 43
        enemyRightOffset = enemy.pos.x + 30
        enemyLeftOffset = enemy.pos.x - 30

        if player.playerState == "attack":
            if player.playerDirection == "Right":

                if player.attackFrame == 2:
                    if (enemyLeftOffset <= playerRightOffset and playerRightOffset <= enemyLeftOffset + 35) or \
                            (enemyLeftOffset >= playerLeftOffset and enemyLeftOffset <= playerLeftOffset + 35):
                        enemy.hit = True

            elif player.playerDirection == "Left":
                if player.attackFrame == 2:
                    if (enemyLeftOffset <= playerLeftOffset and playerLeftOffset <= enemyLeftOffset + 35) or (enemyLeftOffset >= playerRightOffset and enemyLeftOffset <= playerRightOffset + 35):
                        enemy.hit = True





    def interactableCollision(self, interact, player, lifesystem, scoresystem):
        playerBottomOffset = player.pos.y + 32
        playerLeftOffset = player.pos.x - 21
        playerRightOffset = player.pos.x + 21
        playerTopOffset = player.pos.y - 32

        if ((playerRightOffset > interact.xcorner and playerLeftOffset < interact.right) and
                (playerBottomOffset > interact.ycorner and playerTopOffset < interact.bottom)):
            if interact.name == "ladder" and self.ladderTimer == 0:
                self.player.on_ladder = True

            elif interact.name == "saw":
                player.pos.y -= player.vel.y *2
                player.pos.x -= player.vel.x *2
                player.vel.y = (-player.vel.y * 1.5)
                player.vel.x = (-player.vel.x * 1.5)
                print("on saw")
                lifesystem.damage()
            elif interact.name == "spike":
                player.pos.y -= player.vel.y *2
                player.pos.x -= player.vel.x *2
                player.vel.y = (-player.vel.y * 1.5)
                player.vel.x = (-player.vel.x * 1.5)
                print("on spike")
                lifesystem.damage() # Add spritesheet for spikes appearing

            elif interact.name == "finishLevelDoor":
                if self.player.hasKey:
                    return "levelFinish"
            return True  # Collision detected
        else:
            return False  # No collision

    def projectileCollision(self, projectile, player, lifesystem, poly, scoresystem):
        playerBottomOffset = player.pos.y + 32
        playerLeftOffset = player.pos.x - 21
        playerRightOffset = player.pos.x + 21
        playerTopOffset = player.pos.y - 32
        projectileBottomOffset = projectile.pos.y + (projectile.dims[1] - projectile.centre[1])
        projectileLeftOffset = projectile.pos.x - (projectile.dims[0] - projectile.centre[0])
        projectileRightOffset = projectile.pos.x + (projectile.dims[0] - projectile.centre[0])
        projectileTopOffset = projectile.pos.y - (projectile.dims[1] - projectile.centre[1])
        if str(type(projectile)) == "<class '__main__.saw'>":
            if math.degrees(projectile.angle) == 0:
                projectileBottomOffset = projectile.pos.y
                projectileLeftOffset = projectile.pos.x - (projectile.dims[0] - projectile.centre[0])
                projectileRightOffset = projectile.pos.x + (projectile.dims[0] - projectile.centre[0])
                projectileTopOffset = projectile.pos.y - (projectile.dims[1])
            elif math.degrees(projectile.angle) == 90:
                projectileBottomOffset = projectile.pos.y + (projectile.dims[0] - projectile.centre[0])
                projectileTopOffset = projectile.pos.y - (projectile.dims[0] - projectile.centre[0])
                projectileLeftOffset = projectile.pos.x - 27
                projectileRightOffset = projectile.pos.x - 9
            elif math.degrees(projectile.angle) == 180:
                projectileBottomOffset = projectile.pos.y + 18
                projectileTopOffset = projectile.pos.y
                projectileLeftOffset = projectile.pos.x - 15
                projectileRightOffset = projectile.pos.x + 15
            elif math.degrees(projectile.angle) == -90:
                projectileBottomOffset = projectile.pos.y + (projectile.dims[0] - projectile.centre[0])
                projectileTopOffset = projectile.pos.y - (projectile.dims[0] - projectile.centre[0])
                projectileLeftOffset = projectile.pos.x-18
                projectileRightOffset = projectile.pos.x
        if projectile.name == "coin" or projectile.name == "key":
            if ((playerRightOffset > projectileLeftOffset and playerLeftOffset < projectileRightOffset) and
                (playerBottomOffset > projectileTopOffset and playerTopOffset < projectileBottomOffset)):
                if projectile.name == "coin" and not projectile.collected:
                    scoresystem.increase() # increases score (money)
                    projectile.collected = True # sets to invis and stops any more score
                    projectile.finished = True
                elif projectile.name == "key":
                    player.hasKey = True # Set to false when new scene
                    print("collected key")
                    projectile.finished = True

        elif player.immunityFrames == 75:
            if ((playerRightOffset > projectileLeftOffset and playerLeftOffset < projectileRightOffset) and
                (playerBottomOffset > projectileTopOffset and playerTopOffset < projectileBottomOffset)):

                    player.Hit = True
                    player.immunityFrames = 74
                    if str(type(projectile)) == "<class '__main__.saw'>":
                        player.pos.y += projectile.vel.y * 2
                        player.pos.x += projectile.vel.x * 2
                        player.vel.y = (projectile.vel.y * 1.5)
                        player.vel.x = (projectile.vel.x * 1.5)

                        print("on saw")
                    else:
                        print("arrowHit")
                        projectile.finished = True

                    lifesystem.damage()
        if not str(type(projectile)) == "<class '__main__.saw'>":
            if ((projectileRightOffset > poly.xcorner and projectileLeftOffset < poly.right) and
                (projectileBottomOffset > poly.ycorner and projectileTopOffset < poly.bottom)):
                projectile.finished = True
        else:
            if ((projectileRightOffset > poly.xcorner and projectileLeftOffset < poly.right) and
                (projectileBottomOffset > poly.ycorner and projectileTopOffset < poly.bottom)):
                #projectile.pos.x -= projectile.vel.x
                if not projectile.reversed:
                    projectile.reversed = True
                else:
                    projectile.reversed = False
                projectile.surfaceflipped = False





class interactable(inviswall):
    def __init__(self, xcorner, ycorner, width, height, name):
        super().__init__(xcorner, ycorner, width, height)
        self.name = name
        self.collected = False


class projectile(Player):
    def __init__(self, pos, name, Spritesheet, direction, player, centre, dims):

        self.pos = pos
        self.vel = Vector()
        self.Spritesheet = Spritesheet
        self.direction = direction
        self.angle = self.calculateAngle(player)
        self.name = name
        self.centre = centre
        self.dims = dims
        self.vel.x = 5*math.cos(self.angle)*self.direction
        self.vel.y = -5* math.sin(self.angle)
        self.finished = False
        self.collected = False

    def draw(self, canvas):
        if self.name == "arrow":

            self.angle = math.atan(self.vel.y / self.vel.x) - math.radians(180)
        canvas.draw_image(self.Spritesheet, self.centre, self.dims,
                          self.pos.get_p(), self.dims, self.angle)

    def calculateAngle(self, player):
        v0 = 5
        g = Vector(0,-0.1)
        R = player.pos.__sub__(self.pos)
        R.y *= -1
        a = (Vector.dot(g, g)) / 4
        b = -(Vector.dot(R, g)) - (v0**2)
        c = (Vector.dot(R, R))
        if (b ** 2 - (4 * a * c)) >= 0:

            tsq1 = (-b + math.sqrt(b ** 2 - (4 * a * c))) / (2 * a)
            tsq2 = (-b - math.sqrt(b ** 2 - (4 * a * c))) / (2 * a)
            t1 = math.sqrt(tsq1)
            t2 = math.sqrt(tsq2)
            N1 = (R - (Vector.__mul__(g, t1 ** 2)) / 2) / (v0 * t1)
            N2 = (R - (Vector.__mul__(g, t2 ** 2)) / 2) / (v0 * t2)
            angle1 = math.atan(N1.y / N1.x)
            angle2 = math.atan(N2.y / N2.x)
            return -(max(angle1, angle2))
        return 0


    def updateProjectile(self):

        self.pos.add(self.vel)
        if self.name == "coin":
            self.vel = Vector(0,0)
        if self.name == "fireball":
            self.vel.x = (0.5 * self.direction)
            self.vel.y = 0
        if self.name == "arrow":
            self.vel.y += 0.1
        if self.name == "key":
            self.vel = Vector(0,0)

class saw:
    def __init__(self, pos, surface, sprite):
        self.reversed = False
        self.pos = pos  # Current position
        self.speed = 1  # Movement speed
        self.surface = surface  # The current polygon surface it's moving on
        self.flippedsurface = (Vector(0,0), Vector(1,1))
        self.angle = self.get_surface_angle(surface)  # Rotation angle
        self.vel = self.get_surface_velocity(surface)  # Velocity along surface
        self.sawSprite = sprite
        self.centre = (15, 9)
        self.dims = (30, 18)
        self.surfaceflipped = False
        self.name = "saw"


    def get_surface_angle(self, surface):
        dx = surface[1].x - surface[0].x
        dy = surface[1].y - surface[0].y
        return math.atan2(dy, dx)  # Angle of the surface

    def get_surface_velocity(self, surface):
        dx = surface[1].x - surface[0].x
        dy = surface[1].y - surface[0].y
        length = math.sqrt(dx**2 + dy**2)
        return Vector((dx / length) * self.speed, (dy / length) * self.speed)

    def update(self, polygons):

        if self.reversed:
            if not self.surfaceflipped:
                temp1 = self.surface[0].x
                self.flippedsurface[0].x = self.surface[1].x
                self.flippedsurface[1].x = temp1
                temp2 = self.surface[0].y
                self.flippedsurface[0].y = self.surface[1].y
                self.flippedsurface[1].y = temp2
                self.surfaceflipped = True

            self.angle = self.get_surface_angle(self.surface)
            self.vel = self.get_surface_velocity(self.flippedsurface)
            self.pos.x += self.vel.x
            self.pos.y += self.vel.y


            if self.reached_surface_end():

                next_surface = self.find_next_surface(polygons)

                self.surfaceflipped = False

#error checking?

                if next_surface:
                    self.pos.x = self.flippedsurface[1].x
                    self.pos.y = self.flippedsurface[1].y

                    self.surface = next_surface
        else:
            self.angle = self.get_surface_angle(self.surface)
            self.vel = self.get_surface_velocity(self.surface)
            self.pos.x += self.vel.x
            self.pos.y += self.vel.y
            # Check if the saw reaches the end of the current surface
            if self.reached_surface_end():

                next_surface = self.find_next_surface(polygons)

                if next_surface:
                    self.pos.x = self.surface[1].x
                    self.pos.y = self.surface[1].y
                    self.surface = next_surface



    def reached_surface_end(self):
        return (self.pos.x > max(self.surface[0].x, self.surface[1].x) or
                self.pos.x < min(self.surface[0].x, self.surface[1].x) or
                self.pos.y > max(self.surface[0].y, self.surface[1].y) or
                self.pos.y < min(self.surface[0].y, self.surface[1].y)
                )

    def find_next_surface(self, edges):
        for edge in edges:
            if self.reversed:
                if edge[1] == self.surface[0]:
                    return edge
            else:
                if edge[0] == self.surface[1]:  # Check if a polygon connects to the current end
                    return edge  # Return the next edge

        return None  # No next surface found


    def draw(self, canvas):
        if math.degrees(self.angle) == 0:
            canvas.draw_image(self.sawSprite, (15,9), (30,18), (self.pos.x, self.pos.y - 9), (30,18), self.angle)
        elif math.degrees(self.angle) == 90:
            canvas.draw_image(self.sawSprite, (15, 9), (30, 18), (self.pos.x + 9, self.pos.y), (30, 18), self.angle)
        elif math.degrees(self.angle) == 180:
            canvas.draw_image(self.sawSprite, (15,9), (30,18), (self.pos.x, self.pos.y + 9), (30,18), self.angle)
        elif math.degrees(self.angle) == -90:
            canvas.draw_image(self.sawSprite, (15, 9), (30, 18), (self.pos.x - 9, self.pos.y), (30, 18), self.angle)


class lives:
    def __init__(self, img):
        self.img = img
        self.imgwidth = img.get_width()
        self.imgheight = img.get_height()
        self.max = 5
        self.currentlives = 5
    def damage(self):
        self.currentlives -= 1
    def draw(self, canvas):
        for i in range(self.currentlives):
            canvas.draw_image(self.img, ((self.imgwidth/2), (self.imgheight/2)), (16,16), (1150 + (i*25), 20), (32,30))

class score:
    def __init__(self, img):
        self.img = img
        self.imgwidth = img.get_width()
        self.imgheight = img.get_height()
        self.currentscore = 0
    def increase(self):
        self.currentscore += 1
    def draw(self, canvas):
        canvas.draw_image(self.img, ((self.imgwidth/2), (self.imgheight/2)), (16,16), (1150, 60), (32,30))
        canvas.draw_text(str(self.currentscore), (1180, 60), 12, 'Yellow')





class Game:
    def __init__(self, firstStart=True):
        if firstStart:
            self.frame = simplegui.create_frame('Game', 1280, 720)
            self.button = self.frame.add_button("Start", self.button_handler, 200)
        self.rightPlayersheet = Spritesheet("https://raw.githubusercontent.com/RyanQuayum/pythongame/refs/heads/main/walkSpritesheet.png",1,8)
        self.heartimg = simplegui.load_image("https://raw.githubusercontent.com/RyanQuayum/pythongame/refs/heads/main/heart.png")
        self.leftPlayersheet = Spritesheet("https://raw.githubusercontent.com/RyanQuayum/pythongame/refs/heads/main/newLeftSpritewalksheet.png", 1, 8)
        self.attack1RightPlayersheet = attackSpritesheet("https://raw.githubusercontent.com/RyanQuayum/pythongame/refs/heads/main/attack1RightSpritesheet.png", 1, 4, [48,49,85,80])
        self.attack1LeftPlayersheet = attackSpritesheet("https://raw.githubusercontent.com/RyanQuayum/pythongame/refs/heads/main/leftAttackSpritesheet.png", 1, 4, [48, 48, 84, 80])
        self.lvl1image = simplegui.load_image("https://raw.githubusercontent.com/RyanQuayum/pythongame/refs/heads/main/lvl1.png")
        self.skeletonIdleRight = Spritesheet("https://raw.githubusercontent.com/RyanQuayum/pythongame/refs/heads/main/Skeleton%20Idle.png", 1, 11)
        self.skeletonLeftIdle = Spritesheet("https://raw.githubusercontent.com/RyanQuayum/pythongame/refs/heads/main/skeletonIdleLeft.png", 1, 11)
        self.skeletonWalkLeft = Spritesheet("https://raw.githubusercontent.com/RyanQuayum/pythongame/refs/heads/main/skeletonWalkLeft.png", 1, 13)
        self.skeletonWalkRight = Spritesheet("https://raw.githubusercontent.com/RyanQuayum/pythongame/refs/heads/main/Skeleton%20Walk.png", 1, 13)
        self.skeletonDeadRight = Spritesheet("https://raw.githubusercontent.com/RyanQuayum/pythongame/refs/heads/main/Skeleton%20Dead.png", 1, 15)
        self.skeletonDeadLeft = Spritesheet("https://raw.githubusercontent.com/RyanQuayum/pythongame/refs/heads/main/skeletonDeadLeft.png", 1, 15)
        self.skeletonHitRight = Spritesheet("https://raw.githubusercontent.com/RyanQuayum/pythongame/refs/heads/main/Skeleton%20Hit.png ", 1, 8)
        self.skeletonHitLeft = Spritesheet("https://raw.githubusercontent.com/RyanQuayum/pythongame/refs/heads/main/skeletonHitLeft.png", 1, 8)
        self.skeletonAttackRight = attackSpritesheet("https://raw.githubusercontent.com/RyanQuayum/pythongame/refs/heads/main/Skeleton%20Attack.png", 1, 18, [43]*18)
        self.skeletonAttackLeft = attackSpritesheet("https://raw.githubusercontent.com/RyanQuayum/pythongame/refs/heads/main/skeletonAttackLeft.png", 1, 18, [43]*18)
        self.singleCoin = simplegui.load_image("https://raw.githubusercontent.com/RyanQuayum/pythongame/refs/heads/main/singlecoin.png")
        self.sawSprite = simplegui.load_image("https://raw.githubusercontent.com/RyanQuayum/pythongame/refs/heads/main/saw.png")
        self.keySprite = simplegui.load_image("https://raw.githubusercontent.com/RyanQuayum/pythongame/refs/heads/main/Hallowed_Key.png")
        self.arrow = simplegui.load_image("https://raw.githubusercontent.com/RyanQuayum/pythongame/refs/heads/main/ARROWTHATACTUALLYISTRANSPARENT.png")
        self.gameState = "mainMenu"
        self.kbd = Keyboard()
        self.lifesystem = lives(self.heartimg)
        self.scoresystem = score(self.singleCoin)
        self.player = Player(Vector(100, 20), self.rightPlayersheet, self.leftPlayersheet, self.attack1RightPlayersheet, self.attack1LeftPlayersheet)
        self.frame.set_draw_handler(self.draw)
        self.frame.set_keydown_handler(self.kbd.keyDown)
        self.frame.set_keyup_handler(self.kbd.keyUp)
        self.terrain_spritesheet = Spritesheet("https://raw.githubusercontent.com/RyanQuayum/pythongame/main/forest-2.png",10,40)
        self.level = 1

        self.enemies = [
            enemy(Vector(70, 172), self.skeletonWalkRight, self.skeletonWalkLeft, self.skeletonAttackRight, self.skeletonAttackLeft, self.skeletonIdleRight, self.skeletonLeftIdle, self.skeletonDeadRight, self.skeletonDeadLeft, self.skeletonHitRight, self.skeletonHitLeft, 18),
            rangedEnemy(Vector(900, 130), self.skeletonWalkRight, self.skeletonWalkLeft, self.skeletonAttackRight, self.skeletonAttackLeft, self.skeletonIdleRight, self.skeletonLeftIdle, self.skeletonDeadRight, self.skeletonDeadLeft, self.skeletonHitRight, self.skeletonHitLeft, 18)
        ]

        self.projectiles = [
            # projectile(Vector(300, 50), "arrow",self.arrow, -1, self.player, (14,3.5), (28,7)),
            projectile(Vector(300, 530), "coin", self.singleCoin, 1, self.player, (8,8), (16,16)),
            projectile(Vector(350, 510), "key", self.keySprite, 1, self.player, (8, 14), (16, 28))

        ]

        self.deleted_projectiles = []
        self.deleted_enemies = []

        self.saws = [

        ]
        self.lvl1polys = [
            (0, 80, 125, 30),
            (225, 80, 180, 30),
            (405, 0, 30, 240),
            (0, 207, 190, 30),
            (250, 308, 315, 155),
            (200, 550, 400, 30),
            (0, 720, 1280, 10),
            (595, 162, 380, 30),
            (568, 0, 28, 75),
            (568, 162, 28, 380),
            (530, 162, 35, 15),
            (405, 225, 70, 15),
            (965, 310, 315, 30),
            (917, 468, 370, 30),
            (225, 695, 650, 30)
        ]

        self.lvl2polys = [(0, 360, 1280, 100)
        ]

        self.polygon_positions = [
            (0, 80, 125, 30),
            (225, 80, 180, 30),
            (405, 0, 30, 240),
            (0, 207, 190, 30),
            (250, 308, 315, 155),
            (200, 550, 400, 30),
            (0, 720, 1280, 10),
            (595, 162, 380, 30),
            (568, 0, 28, 75),
            (568, 162, 28, 380),
            (530, 162, 35, 15),
            (405, 225, 70, 15),
            (965, 310, 315, 30),
            (917, 468, 370, 30),
            (225, 695, 650, 30)

        ]

        self.polygon_edges = []

        self.interactable_positions = [
            (700, 665, 50, 30, "spike"),
            (217, 310, 30, 220, "ladder"),
            (233, 630, 67, 62, "finishLevelDoor"),


        ]

        self.polygons = [inviswall(xcorner, ycorner, width, height) for xcorner, ycorner, width, height in self.polygon_positions]
        self.interactables = [interactable(xcorner, ycorner, width, height, name) for xcorner, ycorner, width, height, name in self.interactable_positions]

        self.interaction = interaction(self.polygons, self.player, self.kbd, self.lifesystem, self.interactables, self.enemies, self.scoresystem, self.projectiles, self.arrow)

        for poly in self.polygons:
            edges = ((poly.topleft, poly.topright), (poly.topright, poly.bottomright),
                     (poly.bottomright, poly.bottomleft), (poly.bottomleft, poly.topleft))
            self.polygon_edges.extend(edges)


        self.saws.append(saw(Vector(250,80), self.polygon_edges[4], self.sawSprite))
        '''HERE'''

    def restart(self):
        self.__init__(firstStart=False)
        self.gamestart()
        return

    def levelChange(self):
        print("Level Change")
        #reinitalise class
        # self.level += 1
        # self.polygon_positions.clear()
        #
        # if self.level == 2:
        #     self.polygon_positions = self.lvl2polys
        pass



    def gamestart(self):
        self.frame.start()

    def button_handler(self): # Start Button Handler
        if self.gameState == "mainMenu":
            self.gameState = "game"
            self.button.set_text("Menu")
        elif self.gameState == "game":
            self.gameState = "mainMenu"
            self.button.set_text("Start")
        elif self.gameState == "dead":
            self.button.set_text("Start")
            self.restart()

    def keyboardUpdate(self):
        if self.kbd.right:
            # if self.player.on_ladder:
            #     pass # on ladder so no move
            if self.kbd.right and self.kbd.attack:
                self.player.vel.add(Vector(0.1, 0))
                self.player.playerState = "attack"
                self.player.playerDirection = "Right"
            else:
                self.player.vel.add(Vector(0.5, 0))
                self.player.playerState = "walkRight"
                self.player.playerDirection = "Right"

        elif self.kbd.left:
            # if self.player.on_ladder:
            #     pass # on ladder so no move (add climbing state)
            if self.kbd.left and self.kbd.attack:
                self.player.vel.add(Vector(-0.1, 0))
                self.player.playerState = "attack"
                self.player.playerDirection = "Left"
            else:
                self.player.vel.add(Vector(-0.5, 0))
                self.player.playerState = "walkLeft"
                self.player.playerDirection = "Left"
        elif self.kbd.attack:
            self.player.playerState = "attack"
        elif not self.kbd.left and not self.kbd.right and not self.player.attackFrame == 0:
            self.player.playerState = "idle"
        else:
            self.player.playerState = "idle"

    def draw(self, canvas):
        if self.gameState == "mainMenu":
            self.frame.set_canvas_background("lightyellow")
            canvas.draw_text('Mystic Flare', (470, 300), 50, 'Red')
            canvas.draw_text('Press Start', (540, 350), 28, 'Red')

        elif self.gameState == "dead":
            self.frame.set_canvas_background("black")
            canvas.draw_text('You Died', (470, 300), 50, 'Red')
            canvas.draw_text('Press Menu to go back to main menu', (540, 350), 28, 'Red')
        elif self.gameState == "game":
            canvas.draw_image(self.lvl1image, (640, 360), (1280, 720), (640, 360), (1280, 720))
            self.interaction.draw(canvas)
            self.interaction.update()
            if self.interaction.update() == "levelFinish":
                self.levelChange()

            for polygon in self.polygons:
                polygon.draw(canvas)
            self.player.draw(canvas, self.player.playerState)
            self.keyboardUpdate()
            self.player.update()
            self.lifesystem.draw(canvas)
            self.scoresystem.draw(canvas)

            for enemy in self.enemies:
                self.interaction.playerAttack(self.player, enemy)
                enemy.update()
                self.interaction.enemyHit(self.player, enemy)
                self.interaction.enemyReact(enemy)
                enemy.draw(canvas)
                if enemy.dead:
                    self.deleted_enemies.append(enemy)
            for enemy in self.deleted_enemies:
                if enemy in self.enemies:
                    self.enemies.remove(enemy)


            for projectile in self.projectiles:
                projectile.updateProjectile()
                for polygon in self.polygons:
                    self.interaction.projectileCollision(projectile, self.player, self.lifesystem, polygon, self.scoresystem)
                projectile.draw(canvas)
                if projectile.finished == True:

                    self.deleted_projectiles.append(projectile)
            for projectile in self.deleted_projectiles:
                if projectile in self.projectiles:
                    self.projectiles.remove(projectile)

            for saw in self.saws:
                for polygon in self.polygons:
                    self.interaction.projectileCollision(saw, self.player, self.lifesystem, polygon, self.scoresystem)
                saw.update(self.polygon_edges)
                saw.draw(canvas)

            if self.lifesystem.currentlives <= 0:
                self.gameState = "dead"

                                                            ####HERE########




newgame = Game()
newgame.gamestart()

