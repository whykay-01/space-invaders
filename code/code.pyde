from ddf.minim import Minim
import os
import random
import time

path = os.getcwd()
player_1 = Minim(this)

# general class that creates the basic characteristics for all the creatures we have in a game (we will inherit from # this class after)

class Creatures():
    def __init__(self, x, y, r, g, img, img_w, img_h):
        self.x = x
        self.y = y
        self.r = r
        self.g = 800
        self.img = loadImage(path + "/images/" + img)
        self.img_w = img_w
        self.img_h = img_h

# class for the boss

class Boss():
    def __init__(self, x, y, r, g, img, img_w, img_h):
        self.vx = 0.3
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.vy = 0.1
        self.img = loadImage(path + "/images/" + img)
        self.img_w = img_w
        self.img_h = img_h

# boss movement function
  
    def update(self):
        image(self.img, self.x - self.img_w // 2, self.y - self.img_h // 2,
              self.img_w, self.img_h)
        self.x = self.x + self.vx
        self.y = self.y + self.vy
        if self.x - self.r / 2 < 0:
            self.x = self.r / 2
            self.vx = 0.3
        elif self.x + self.r / 2 > game.w:
            self.x = game.w - self.r / 2
            self.vx = -0.3

    def display(self):
        self.update()
        
# class that defined the ship of the game

class Player(Creatures):
    def __init__(self, x, y, r, g, img, img_w, img_h):
        Creatures.__init__(self, x, y, r, g, img, img_w, img_h)
        self.key_handler = {LEFT: False, RIGHT: False}
# updates the position of the player 
    def update(self):
        image(self.img, self.x - self.img_w // 2, self.y - self.img_h // 2,
              self.img_w, self.img_h)
        if self.key_handler[LEFT] == True:
            self.vx = -8
            self.dir = LEFT

        elif self.key_handler[RIGHT] == True:
            self.vx = 8
            self.dir = RIGHT

        else:
            self.vx = 0
        self.x = self.x + self.vx

        if self.x - self.r / 2 < 0:
            self.x = self.r / 2
        elif self.x + self.r / 2 > game.w:
            self.x = game.w - self.r / 2
# displays the player
    def display(self):
        self.update()

# creates the enemy class

class Enemies(Creatures):
    def __init__(self, x, y, r, g, img, img_w, img_h):
        Creatures.__init__(self, x, y, r, g, img, img_w, img_h)
        self.vy = 0.1
        self.update()
        self.state = False
#updates the position of the enemies (they can only move down)
    def update(self):
        self.y = self.y + self.vy
        if self.y + self.r / 2 < self.g:
            return False
        else:
            return True
#displays the enemy and if update is True it returns True
    def display(self):
        image(self.img, self.x - self.img_w // 2, self.y - self.img_h // 2,
              self.img_w, self.img_h)
        self.update()
        if self.update() == True:
            return True
# checks whether there is a collision between the enemy and the other creature (player)
    def collision(self, other):
        if ((self.x - other.x)**2 + (self.y - other.y)**2)**(1 / 2) < self.r:
            return True
            other.collision = True

#class for enemy bullets 
class Bullets_player(Player):
    def __init__(self, x, y, r, g, img, img_w, img_h):
        Player.__init__(self, x, y, r, g, img, img_w, img_h)
        self.y = y
        self.x = x
        self.vy = -3
        self.radius = 5
        self.bullet_sound = player_1.loadFile(path +
                                              "/sounds/player_bullet.mp3")
#displays the enemy bullet
    def display(self):
        image(self.img, self.x - self.img_w // 2, self.y - self.img_h // 2,
              self.img_w, self.img_h)
        self.update()
# it updates the position of the bullet- can only move in the y-direction- and if it goes beyond y=0, it returns True which will ultimately lead to the bullet getting erased
    def update(self):
        self.y = self.y + self.vy
        if self.y < 0:
            return True

#a similar class just for enemy bullets 
class Bullets_enemies(Player):
    def __init__(self, x, y, r, g, img, img_w, img_h):
        Player.__init__(self, x, y, r, g, img, img_w, img_h)
        self.y = y
        self.x = x
        self.vy = 3
        self.radius = 5
# displays the enemy bullet 
    def display(self):
        image(self.img, self.x - self.img_w // 2, self.y - self.img_h // 2,
              self.img_w, self.img_h)
        self.update()
# updates the position of the enemy bullet and returns True if it goes below self.g in which case it deletes the bullet from the list of enemy bullets in the game class
    def update(self):
        self.y = self.y + self.vy
        if self.y > self.g:
            return True

# game class which handles the whole game
class Game():
    def __init__(self, w, h, g):
        self.w = w
        self.h = h
        self.g = g
        self.game = False #if self.game is equal to True a new game object is instantiated
        self.game_not_initiated = True
        self.player = Player(random.randint(0, self.w), self.h - 30, 60, 0,
                             "ship.png", 60, 60)
        self.number_of_enemies = 3
        self.enemies = []
        self.key_handler = False
        self.positions = []
        self.bullets = []
        self.enemy_bullets = []
        self.counter = 0
        self.live = False
        self.num_lives = 5
        self.time = 0
        self.k=0 # this is the variable that needed for the destruction of the first bullet which should not appear
        self.game_over_screen = loadImage(path + "/images/" + "game_over.png")
        self.img_background = loadImage(path + "/images/" + "background.png")
        self.game_won = loadImage(path + "/images/" + "game_won.png")
        self.heart = loadImage(path + "/images/" + "heart.png")
        # self.bg_sound = player_1.loadFile(path + "/sounds/unused.mp3")
        self.game_over_sound = player_1.loadFile(path +
                                                 "/sounds/game_over.mp3")
        # self.bg_sound.loop()
        self.score = 0
        self.player_shoots = player_1.loadFile(path +
                                               "/sounds/player_bullet.mp3")
        self.enemy_destroyed = player_1.loadFile(path +
                                                 "/sounds/enemy_dies.mp3")
        self.live_taken = player_1.loadFile(path + "/sounds/new_level.mp3")
        self.winner = player_1.loadFile(path + "/sounds/winner.mp3")
        self.timer = 0
        self.opening_screen = loadImage(path + "/images/" + "opening.png")
        self.boss = Boss(random.randint(0, self.w), 0 + 103, 125, 800,
                         "boss.png", 125, 125)
        self.boss_lives = 5
        self.game_over = False
        self.timez = 0 # will track the amount of time a player spends playing the game, it is set to an actual time when player command the game to start (by either pressing enter or return)
# displays the opening screen which gives the instructions
    def display_opening_screen(self):
        image(self.opening_screen, 0, 0, self.w, self.h)
# displays screen at the top of the game which informs the player about the amount of lives, time and level
    def display_screen(self):
        image(self.img_background, 0, 0, self.w, self.h)
        textSize(20)
        fill(255, 255, 255)
        if self.counter == 3 and len(self.enemies)==0 and self.game_over!=True:
            text("Boss level",350,28)
        else:
            text("Level:"+str(self.counter),350,28)
        textSize(20)
        fill(255, 255, 255)
        text("Lives: ", 580, 28)
        for x in range(self.num_lives):
            image(self.heart, 670 + x * 22, 10, 20, 20)
        textSize(20)
        fill(255, 255, 255)
        self.time = time.time() - self.timer
        text("Time:  " + str(round(self.time, 1)) + " sec", 50, 28)
# when this function is called (player kills all the enemies in a certain level) it spawns new enemies
    def enemy_spawn(self):
        for row in range(self.w / 80):
            list1 = []
            for column in range(self.h / 80):
                list1.append(0)
            self.positions.append(list1)
        for enemy in range(self.number_of_enemies):
            y = 0
            position = random.randint(0, self.w / 80 - 1)
            while self.positions[y][position] != 0:
                y += 1
            self.positions[y][position] = 1
            self.enemies.append(
                Enemies(position * self.w / 10 + self.w / 10 / 2,
                        y * self.h / 10 + self.h / 10 / 2 + 40, self.w / 10,
                        self.g,
                        str(random.randint(1, 5)) + ".png", self.w / 10,
                        self.w / 10))
        for row in range(self.w / 80): #clears the previous list and makes it possible to add new players at relatively the same positions (if this wasn't cleared enemies could not be spawned in the same positions)
            list1 = []
            for column in range(self.h / 80):
                self.positions[row][column] = 0
# when player presses the control button this causes the bullet to be generated 
    def shoot(self):
        if self.key_handler == True and self.timer!=0:
            self.player_shoots.rewind()
            self.player_shoots.play()
            self.bullet = Bullets_player(self.player.x, self.player.y,
                                         self.player.r, self.player.g,
                                         "laser1.png", 8, 22)
            self.bullets.append(self.bullet)
#this method ensures that the enemies shoot bullets at a constant pace (bullets are generated based on the proximity of the enemy to the player from the x axis)
    def enemy_shoots(self):
        list1 = []
        if len(self.enemies) == 0:
            self.next_level = True 
        else:
            for enemy in self.enemies:
                list1.append(abs(enemy.x - self.player.x)) #this appends all the absolute differences between the player and the enemies
            output = [
                idx for idx, element in enumerate(list1)
                if element == min(list1)
            ] #list comprehension for finding the index of the enemy whose absolute distance viewed from the x axis is the smallest
            shooter = self.enemies[output[-1]] #if there are multiple enemies in a column this makes sure the closest one to the player shoots the bullet
            self.enemy_bullet = Bullets_enemies(shooter.x, shooter.y,
                                                shooter.r, shooter.g,
                                                "laser2.png", 8, 22)
            self.enemy_bullets.append(self.enemy_bullet)
          # condition of where we do define the boss appearence 
        if self.counter == 3 and len(
                self.enemies) == 0 and self.game_over != True and time.time(
                ) - self.timez > 1: 
            self.timez = time.time()
            shooter = self.boss

            # boss' bullets are instantiated here
                  
            self.enemy_bullet = Bullets_enemies(shooter.x, shooter.y,
                                                shooter.r, shooter.g,
                                                "laser2.png", 8, 22)
            self.enemy_bullets.append(self.enemy_bullet)
            self.enemy_bullet = Bullets_enemies(shooter.x - 20, shooter.y,
                                                shooter.r, shooter.g,
                                                "laser2.png", 8, 22)
            self.enemy_bullets.append(self.enemy_bullet)
            self.enemy_bullet = Bullets_enemies(shooter.x + 20, shooter.y,
                                                shooter.r, shooter.g,
                                                "laser2.png", 8, 22)
            self.enemy_bullets.append(self.enemy_bullet)
            self.enemy_bullet = Bullets_enemies(shooter.x - 40, shooter.y,
                                                shooter.r, shooter.g,
                                                "laser2.png", 8, 22)
            self.enemy_bullets.append(self.enemy_bullet)
            self.enemy_bullet = Bullets_enemies(shooter.x + 40, shooter.y,
                                                shooter.r, shooter.g,
                                                "laser2.png", 8, 22)
            self.enemy_bullets.append(self.enemy_bullet)

# function that checks for the collision between the bullet of the player and the enemy. is detected, enemy is removed
                  
    def collision(self):
        for enemy in self.enemies:
            for bullet in self.bullets:
                if dist(enemy.x, enemy.y, bullet.x,
                        bullet.y) <= enemy.r / 2 or dist(
                            enemy.x, enemy.y, bullet.x,
                            bullet.y) <= enemy.r / 2 + 1 or dist(
                                enemy.x, enemy.y, bullet.x,
                                bullet.y) <= enemy.r / 2 - 1:
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 10
                                  
# the place where if the collision between the bullet and the and the ship is detected -- the live of the player is taken
                                  
        for bullet in self.enemy_bullets:
            if dist(self.player.x, self.player.y, bullet.x,
                    bullet.y) <= self.player.r / 2:

                self.enemy_bullets.remove(bullet)
                self.num_lives -= 1

                self.live_taken.rewind()
                self.live_taken.play()

                if self.num_lives == 0:
                    self.live = True

        for bullet in self.bullets:
            if dist(self.boss.x, self.boss.y, bullet.x,
                    bullet.y) <= self.boss.r / 2:
                self.bullets.remove(bullet)
                self.boss_lives -= 1

# condition for defeating the boss
      
        if self.boss_lives <= 0:
            self.score += 100
            self.game_over = True
            for bullet in self.bullets:
                self.bullets.remove(bullet)
            self.enemy_bullets = []

    def display(self):
        if self.game_not_initiated == True:
            self.display_opening_screen()
            self.timer = time.time()
            self.k=1

        else:
            if self.k==1:
                self.bullets=[]
                self.k=0
            self.display_screen()
            self.player.display()
            self.collision()
            for bullet in self.enemy_bullets:
                bullet.display()
                if bullet.update() == True:
                    self.enemy_bullets.remove(bullet)
     
            for bullet in self.bullets:
                bullet.display()
                if bullet.update() == True:
                    self.bullets.remove(bullet)
            

# place that controls whether how many new conditions we have to overwrite in the case u pass to the next level
          
            if len(self.enemies) == 0 and self.counter < 3:
                self.enemy_spawn()
                self.number_of_enemies += 2
                self.counter += 1

            elif self.counter == 3 and len(
                    self.enemies) == 0 and self.game_over != True:
                self.boss.display()

# displaying the game winning display
                      
            if self.game_over == True:
                # self.bg_sound.close()
                self.winner.rewind()
                self.winner.play()
                self.game = True
                image(self.game_won, 0, 0, self.w, self.h)

                textSize(35)
                fill(0, 174, 239)
                text(str(round(self.time, 0)), 498.6474, 468.0663)

                fill(127, 135, 194)
                text(str(round(self.time, 0) + self.score), 528.5699, 400)

                fill(237, 28, 36)
                text(str(self.score), 563.5154, 532.15)
                
# checks whether the boss has reached the ground or collapsed with the player, so the game is lost
              
            if self.live == True or self.boss.y - self.boss.r - 30 >= self.g or dist(
                    self.player.x, self.player.y, self.boss.x,
                    self.boss.y) < self.boss.r - 32: 
                self.game = True
                self.time_spent = time.time()

                # displaying the game over screen
                image(self.game_over_screen, 0, 0, self.w, self.h)
                textSize(35)
                fill(0, 174, 239)
                text(str(round(self.time, 0)), 498.6474, 468.0663)

                fill(127, 135, 194)
                text(str(round(self.time, 0) + self.score), 528.5699, 400)

                fill(237, 28, 36)
                text(str(self.score), 563.5154, 532.15)
            

            for enemy in self.enemies:
                if enemy.display() or dist(
                        enemy.x, enemy.y, self.player.x, self.player.y
                ) <= self.player.r + 10 or self.live == True:
                    self.game = True
                    # self.bg_sound.close()

                    self.game_over_sound.rewind()
                    self.game_over_sound.play()

                    self.time_spent = time.time()
                    image(self.game_over_screen, 0, 0, self.w, self.h)
                    textSize(35)
                    fill(0, 174, 239)
                    text(str(round(self.time, 0)), 498.6474, 468.0663)

                    fill(127, 135, 194)
                    text(str(round(self.time, 0) + self.score), 528.5699, 400)

                    fill(237, 28, 36)
                    text(str(self.score), 563.5154, 532.15)

                    break
                else:
                    self.game = False
                    enemy.display()
                    enemy.update()

# the variable that controls that player will not be able to shoot every other time he/she presses the cntrl button 
# for more information please see the function that defines the pressing of the control button
                  
timez = 0
game = Game(800, 800, 585)


def setup():
    # we loaded the font here and established the environment for the future
    font = loadFont("KenVector-Future-42.vlw")
    textFont(font)
    size(game.w, game.h)
    background(255, 255, 255)
    frameRate(60)


def draw():
    global game
    global game_initiated

    if game.game == False:
        background(255, 255, 255)
        game.display()
# re-instantiatin of the game (in case the game is over (game.game == True) part of the code)
    elif game.game == True and mousePressed:
        game.player_shoots.close()
        game.enemy_destroyed.close()
        game.live_taken.close()
        game.winner.close()
        game.winner.close()
        # game.bg_sound.close()
        game = Game(800, 800, 585)
        game.display()

    if frameCount % 100 == 0:
        game.enemy_shoots()

# functions that control the pressing of the keys

def keyPressed():
    global timez
  # the place where the game is initiated for the first time
    if keyCode == RETURN or ENTER:
        game.game_not_initiated = False

    pressing = True
    if keyCode == LEFT:
        game.player.key_handler[LEFT] = True
    elif keyCode == RIGHT:
        game.player.key_handler[RIGHT] = True
    elif keyCode == CONTROL and pressing == True and time.time(
    ) - timez > 1 or timez == 0:
        timez = time.time()
        game.key_handler = True
        game.shoot()
        pressing = False


def keyReleased():
    pressing = True
    if keyCode == LEFT:
        game.player.key_handler[LEFT] = False
    elif keyCode == RIGHT:
        game.player.key_handler[RIGHT] = False
    elif keyCode == CONTROL:
        game.key_handler = False
        pressing = True
