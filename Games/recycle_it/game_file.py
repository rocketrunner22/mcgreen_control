#!/usr/bin/python3
import pygame
from pygame import mixer
import random
import time
import math
import sys
import threading

# sys.path.append("../")
# from head_controller import Head_comm
#
# controller = Head_comm("Recycle It")
# Initialize pygame
pygame.init()

#threading trackers
active_head = 0
active_face = 0

# Screen Size (x,y)
window = (1080, 1920)
screen = pygame.display.set_mode(window)

# Background
background = pygame.image.load('gamebkg.png')
background = pygame.transform.scale(background, (window[0], window[1]//2))
game_lst = pygame.image.load('gameLostBkg.png')
game_1st = pygame.transform.scale(game_lst, (window[0], window[1]//2))
game_wn = pygame.image.load('gameWonBkg.png')
game_wn = pygame.transform.scale(game_wn, (window[0], window[1]//2))
menu = pygame.image.load('menubkg.png')
menu = pygame.transform.scale(menu, (window[0], window[1]//2))
menuForHelps = pygame.transform.scale(menu, (1080,590))
helps = pygame.image.load('helpbkg.png')
helps = pygame.transform.scale(helps, (1080, 740))

# Buttons
playb = pygame.image.load('play.png')
playb = pygame.transform.scale(playb, (700,222))
helpb = pygame.image.load('help.png')
helpb = pygame.transform.scale(helpb, (700,222))
exitb = pygame.image.load('exit.png')
exitb = pygame.transform.scale(exitb, (700,222))
lvl1 = pygame.image.load('lvl1.png')
lvl1 = pygame.transform.scale(lvl1, (700,222))
lvl2 = pygame.image.load('lvl2.png')
lvl2 = pygame.transform.scale(lvl2, (700,222))
lvl3 = pygame.image.load('lvl3.png')
lvl3 = pygame.transform.scale(lvl3, (700,222))
invplayb = pygame.image.load('invplay.png')
invplayb = pygame.transform.scale(invplayb, (700,222))
invhelpb = pygame.image.load('invhelp.png')
invhelpb = pygame.transform.scale(invhelpb, (700,222))
invexitb = pygame.image.load('invexit.png')
invexitb = pygame.transform.scale(invexitb, (700,222))
invlvl1 = pygame.image.load('invlvl1.png')
invlvl1 = pygame.transform.scale(invlvl1, (700,222))
invlvl2 = pygame.image.load('invlvl2.png')
invlvl2 = pygame.transform.scale(invlvl2, (700,222))
invlvl3 = pygame.image.load('invlvl3.png')
invlvl3 = pygame.transform.scale(invlvl3, (700,222))


# Background Music
mixer.music.load('backgroundmsc.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Recycle It or Not!")
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)

# Score
points_value = 0
largeText = pygame.font.Font('Bubblegum.ttf', 100)   #Large text, ideal for headings
mediumText = pygame.font.Font('Bubblegum.ttf', 48)   #Medium text, ideal for subheadings
mediumText2 = pygame.font.Font('Bubblegum.ttf', 24)
smallText =  pygame.font.Font('Bubblegum.ttf', 16)   #Small text, ideal for small buttons
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
darker_red = (200, 0, 0)
green = (0, 255, 0)
darker_green = (0, 200, 0)
blue = (50, 89, 250)
darker_blue = (35, 67, 250)
font = pygame.font.Font('Bubblegum.ttf', 32)
textX = 10
textY = 10

# Number of enemies and good objects at any given time
num_of_each = 3

# Player + Starting Coordinates
playerImg = pygame.image.load('character_bin.png')
playerX = window[0]/2
playerY = 3*window[1]/4
playerX_change = 0

# enemy -- non-recyclables


# timer + level
clock = pygame.time.Clock()
seconds = 0
milliseconds = 0

level = 0

class Button:
    def __init__ (self, ac, ic, rectVals):
        self.ac = ac #Active color of button
        self.ic = ic #Inactive color of button
        self.rectAttrs = rectVals #(x, y, w, h) of button

    def generate(self):
        x, y, w, h = self.rectAttrs
        mouse = pygame.mouse.get_pos()

        #Check if mouse is on button
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            screen.blit(self.ac, (self.rectAttrs[0], self.rectAttrs[1]))

        #Else just show darker button
        else:
            screen.blit(self.ic, (self.rectAttrs[0], self.rectAttrs[1]))




        pygame.display.update()



    def is_pressed(self, touch_status):
        x, y, w, h = self.rectAttrs
        mouse = pygame.mouse.get_pos()

        #Check if mouse is hovering over button or not
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            if touch_status == True:
                #print('CLICK DETECTED')
                return True

            elif touch_status == False:
                return False

        #If mouse is not hovering over button, button must obviously not be pressed
        else:
            return False

#Render text to a surface and a corresponding rectangle
def text_objects(text, font, color=(0,0,0)):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def show_score(pts, x, y):
    score = font.render("Score: " + str(pts), True, (0, 0, 0))
    screen.blit(score, (x, y))


# Checking Collision by using distance formula between objects
# parameter is named var because function can be used by enemies and good objects
def isCollision(varX, varY, playerX, playerY):
    distance = math.sqrt((math.pow(varX - playerX, 2)) + (math.pow(varY - playerY, 2)))
    if distance < 27:
        return True
    else:
        return False


def game_over(pts):
    if level == 0:
        if pts >= 1000:
            game_won(pts)
        else:
            game_lost(pts)
    if level == 1:
        if pts >= 1200:
            game_won(pts)
        else:
            game_lost(pts)
    if level == 2:
        if pts >= 1500:
            game_won(pts)
        else:
            game_lost(pts)


#threaded function
#set vertical = true for vertical movement (auto x = 90) false for opposite
def rotate_head(vertical, positions):
    global active_head
    print("---------------", flush=True)
    print("vertical: ", vertical, flush=True)
    print("positions: ", positions, flush=True)
    if active_head == 0:
        active_head +=1
        current_pos = 90
        for x in positions:
            print("x: ", x, flush=True)
            if vertical == True:
                controller.head_update([90, x])
            else:
                controller.head_update([x,90])
            print("servo update sent", flush=True)
            delay = float(abs(current_pos - x)) / 60. *.14*5
            print("delay: ", delay, flush=True)
            time.sleep(delay)
            current_pos = x
        active_head -= 1

#threaded function
#change face and then revert to normal after x time

def change_face(expression, delay):
    global active_face
    print("+++++++++++++++++++++++++++++++++=", flush=True)
    print ("expression: ", expression, flush=True)
    print("delay: ", delay, flush=True)
    #print("name: ", str(threading.current_thread().name))
    print("count: ", active_face)
    if active_face == 0:
        active_face += 1
        controller.face_update(expression)
        print("face update sent", flush=True)
        time.sleep(delay)
        controller.face_update(4)
        print("face reset sent", flush=True)
        active_face -= 1

def game_won(pts):
    # face = random.randint(1, 3)  # HEEEEEEEEEEEEEEEEEERRRRRRRRRRRRRRRRRREEEEEEEEEEEEEE
    # controller.face_update(face)
    # # These commands won't over write themselves right? like if i say these three in a row
    # # it'll hit all of the positions before going back to [90,90]?
    # # controller.head_update([90, 45])
    # # controller.head_update([90, 135])
    # # controller.head_update([90, 90])
    # rotate=threading.Thread(target=rotate_head, args=(True, [45, 135, 90]))
    # rotate.start()
    mixer.music.load('game_won.wav')
    mixer.music.play()
    pause = True
    while pause:
        screen.fill((255, 255, 255))
        screen.blit(game_wn, (50, window[1]/4))
        show_score(pts, window[0]/2 - 70, 2*window[1]/3)
        for event in pygame.event.get():
            # Quitting the Game by X-ing out Window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE or event.type == pygame.MOUSEBUTTONDOWN:
                    level_select(level)
                if event.key == pygame.K_SPACE:
                    pts = 0
                    game(playerX, points_value, playerX_change, milliseconds, seconds, level)
            if event.type == pygame.MOUSEBUTTONDOWN:
                level_select(level)
        pygame.display.update()



def game_lost(pts):
    # face = random.randint(5, 7)  # HHHHHHHHHHHHHHEEEEEEEEEEEEERRRRRRRRRRRREEEEEEEEEEEE
    # controller.face_update(face)
    #See game_won head update comments
    # controller.head_update([45, 90])
    # controller.head_update([135, 90])
    # controller.head_update([90, 90])
    # rotate=threading.Thread(target=rotate_head, args=(False, [45, 135, 90]))
    # rotate.start()


    mixer.music.load('game_lose.wav')
    mixer.music.play()
    pause = True
    while pause:
        screen.fill((255, 255, 255))
        screen.blit(game_lst, (50, window[1]/4))
        show_score(pts, window[0]/2 - 70, 2*window[1]/3)
        for event in pygame.event.get():
            # Quitting the Game by X-ing out Window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    level_select(level)
                if event.key == pygame.K_SPACE:
                    pts = 0
                    game(playerX, points_value, playerX_change, milliseconds, seconds, level)
            if event.type == pygame.MOUSEBUTTONDOWN:
                level_select(level)
        pygame.display.update()


def intro():
    bmenu = True
    screen.fill((255, 255, 255))
    screen.blit(menu, (0, 0))
    screen.blit(menu, (0,window[1]/2))
    # controller.face_update(4)  # HEEEEEEEEEEEEEERRRREEEEEEEEEEEEE
    playbutton = Button(invplayb, playb, (window[0]/2 - 750/2, window[1]/4, 750, 222))
    helpbutton = Button(invhelpb, helpb, (window[0]/2 - 750/2,  window[1]/2, 750, 222))
    quitbutton = Button(invexitb, exitb, (window[0]/2 - 750/2,  3*window[1]/4, 750, 222))
    TextSurf, TextRect = text_objects("Recycle It!", largeText, blue)
    TextRect.center = (window[0]/2,190)
    screen.blit(TextSurf,TextRect)
    while bmenu:

        playbutton.generate()
        helpbutton.generate()
        quitbutton.generate()
        for event in pygame.event.get():
            # Quitting the Game by X-ing out Window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            touch_status = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                touch_status = True
                if(playbutton.is_pressed(touch_status)):
                    level_select(level)
                if(helpbutton.is_pressed(touch_status)):
                    help_screen()
                if(quitbutton.is_pressed(touch_status)):
                    pygame.quit()
                    quit()



        # print(click)




        pygame.display.update()


def ready():
    message = ["Ready ", "Ready. ", "Ready.. ", "Ready... ", "Set ", "Set. ", "Set.. ", "Set... ", "GO! " ]
    for i in range(9):
        screen.fill((255, 255, 255))
        screen.blit(background, (-50, window[1]/4))
        ready = font.render(message[i], True, (0, 0, 0))
        screen.blit(ready, (window[0]/2 - 50, window[1]/2))
        pygame.display.update()
        pygame.time.delay(750)





def help_screen():
    bhelp = True
    while bhelp:
        screen.fill((255, 255, 255))
        screen.blit(menuForHelps, (0,0))
        screen.blit(helps, (0, 590))
        screen.blit(menuForHelps, (0,1330))
        for event in pygame.event.get():
            # Quitting the Game by X-ing out Window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # keystroke check (right/left) and changing val of playerX_change to +/- based on keypress
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    intro()
        pygame.display.update()


def level_select(lvl):
    pygame.time.delay(750)
    bmenu = True
    screen.fill((255, 255, 255))
    screen.blit(menu, (0, 0))
    screen.blit(menu, (0,window[1]/2))
    lvl1b = Button(invlvl1, lvl1, (window[0]/2 - 750/2, window[1]/4, 700, 222))
    lvl2b = Button(invlvl2, lvl2, (window[0]/2 - 750/2, window[1]/2, 700, 222))
    lvl3b = Button(invlvl3, lvl3, (window[0]/2 - 750/2, 3*window[1]/4, 700, 222))
    TextSurf, TextRect = text_objects("Select a Level", largeText, blue)
    TextRect.center = (window[0]/2,190)
    screen.blit(TextSurf,TextRect)
    while bmenu:
        lvl1b.generate()
        lvl2b.generate()
        lvl3b.generate()
        for event in pygame.event.get():
            # Quitting the Game by X-ing out Window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    intro()
            if event.type == pygame.MOUSEBUTTONDOWN:
                touch_status = True
                if(lvl1b.is_pressed(touch_status)):
                    game(playerX, points_value, playerX_change, milliseconds, seconds, 0)
                if(lvl2b.is_pressed(touch_status)):
                    game(playerX, points_value, playerX_change, milliseconds, seconds, 1)
                if(lvl3b.is_pressed(touch_status)):
                    game(playerX, points_value, playerX_change, milliseconds, seconds, 2)


        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()


        pygame.display.update()









# Game Loop
def game(playerX, pts, playerX_change, milliseconds, seconds, lvl):
    mixer.music.load('backgroundmsc.wav')
    mixer.music.play(-1)
    ready()
    if(lvl == 1):
        fallspeed = 3
    else:
        fallspeed = 2
    bgame = True
    num_of_each = 3
    if(lvl == 2):
        num_of_each = 2
    goodX = []
    goodY = []
    goodY_change = []
    goodImg = []
    neutX = []
    neutY = []
    neutY_change = []
    neutImg = []
    enemyImg = []
    enemyX = []
    enemyY = []
    enemyY_change = []
    while bgame:
        # RGB Screen Fill - Red, Green, Blue
        screen.fill((255, 255, 255))

        # setting background
        screen.blit(background, (-50, window[1]/4))

        # Checking for events (keypress)
        #for event in pygame.event.get():
            # Quitting the Game by X-ing out Window

            # keystroke check (right/left) and changing val of playerX_change to +/- based on keypress

        # changes X position of player character


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            keys_pressed = pygame.key.get_pressed()
            mousepos = pygame.mouse.get_pos()
            if keys_pressed[pygame.K_LEFT] and keys_pressed[pygame.K_RIGHT]:
                playerX_change = 0
            elif keys_pressed[pygame.K_LEFT] :
                playerX_change = -5
            elif keys_pressed[pygame.K_RIGHT]:
                playerX_change = 5
            elif event.type != pygame.MOUSEBUTTONDOWN:
                playerX_change = 0
            if event.type == pygame.MOUSEBUTTONDOWN:

        #print(mousepos[0], " ", window[0])
                if mousepos[0] < window[0]/2:
                    playerX_change = -5
                elif mousepos[0] >= window[0]/2:
                    playerX_change = 5




        if keys_pressed[pygame.K_ESCAPE]:
                level_select(level)

        playerX += playerX_change
        caphold = 76
        cap = caphold
        randol = random.randint(1, cap)
        if(len(goodImg) <= num_of_each and randol == 1):
            # choosing which good object to show
            goodSelect = random.randint(1, 4)
            if goodSelect == 1:
                goodImg.append(pygame.image.load('good_bag.png'))
            if goodSelect == 2:
                goodImg.append(pygame.image.load('good_soda.png'))
            if goodSelect == 3:
                goodImg.append(pygame.image.load('plastic1.png'))
            if goodSelect == 4:
                goodImg.append(pygame.image.load('plastic2.png'))
            # random spawn of good object
            goodX.append(random.randint(0, 862))
            goodY.append(random.randint(0, 200) - 300)
            # speed of fall
            goodY_change.append(fallspeed)
            cap = caphold

        elif(len(enemyImg) <= num_of_each and randol == 2):
            # choosing which enemy to show
            enemySelect = random.randint(1, 7)
            if enemySelect == 1:
                enemyImg.append(pygame.image.load('enemy_banana.png'))
            if enemySelect == 2:
                enemyImg.append(pygame.image.load('enemy_core.png'))
            if enemySelect == 3:
                enemyImg.append(pygame.image.load('enemy_trash.png'))
            if enemySelect == 4:
                enemyImg.append(pygame.image.load('plastic6.png'))
            if enemySelect == 5:
                enemyImg.append(pygame.image.load('plastic3.png'))
            if enemySelect == 6:
                enemyImg.append(pygame.image.load('pizza.png'))
            if enemySelect == 7:
                enemyImg.append(pygame.image.load('bag.png'))
            # random spawn location of enemy
            enemyX.append(random.randint(0, 862))
            enemyY.append(random.randint(0, 200) - 300)
            # speed of fall
            enemyY_change.append(fallspeed)
            cap = caphold
        else:
            cap -= 5


        if(lvl == 2):
            if(len(neutImg) <= num_of_each and randol == 3):
                # choosing which good object to show
                goodSelect = random.randint(1, 6)
                if goodSelect == 1:
                    neutImg.append(pygame.image.load('clothes.png'))
                if goodSelect == 2:
                    neutImg.append(pygame.image.load('computer.png'))
                if goodSelect == 3:
                    neutImg.append(pygame.image.load('medicine.png'))
                if goodSelect == 4:
                    neutImg.append(pygame.image.load('shreddedpaper.png'))
                if goodSelect == 5:
                    neutImg.append(pygame.image.load('plasticbag.png'))
                if goodSelect == 6:
                    neutImg.append(pygame.image.load('tire.png'))
                # random spawn of good object
                neutX.append(random.randint(0, 862))
                neutY.append(random.randint(0, 200) - 300)
                # speed of fall
                neutY_change.append(fallspeed)






        # Changes y position of enemies and good objects
        for i in range(len(goodImg)):
            if(i >= len(goodImg)):
                break
            goodY[i] += goodY_change[i]


            # Checking for collision

            goodCollision = isCollision(goodX[i], goodY[i], playerX, playerY)

            # Adding points to score
            if goodCollision:
                good_catch = mixer.Sound('good_catch.wav')
                #good_catch.play()
                # face = random.randint(1, 3)  # HHHHHEEEEEEEEEEEEEEERRRRRRRRRRRRREEEEEEEEEEEEE
                # good_face = threading.Thread(target=change_face, args=(face, 0.5,))
                # good_face.daemon=True
                # good_face.start()
                # controller.face_update(face)
                # # should i delay here? cuz it's gonna delay the entire program or is that on ur end?
                # # either way i'll include and u can play around
                # # time.sleep(2)
                # controller.face_update(4)
                pts += 100
                print(pts)
                # Sending good object to top of screen in a New location
                del goodX[i]
                del goodY[i]
                del goodY_change[i]
                del goodImg[i]
                i -= 1
            elif goodY[i] > 3*window[1]/4 + 50:
                del goodX[i]
                del goodY[i]
                del goodY_change[i]
                del goodImg[i]
                i -= 1
            else:
                screen.blit(goodImg[i], (goodX[i], goodY[i]))

        for i in range(len(enemyImg)):
            if(i >= len(enemyImg)):
                break
            enemyY[i] += enemyY_change[i]
            badCollision = isCollision(enemyX[i], enemyY[i], playerX, playerY)
            if badCollision:
                bad_catch = mixer.Sound('bad_catch.wav')
                # DISPLAY THE SURPRISED FACE HERE FOR 1 SECOND AND REVERT BACK TO NEUTRAL
                #bad_catch.play()
                # face = random.randint(5, 7)  # HHHHHHHEEEEEEEEEEEEEERRRRRRRRRRRRREEEEEEEEEEEE
                # controller.face_update(face)
                # # should i delay here? cuz it's gonna delay the entire program or is that on ur end?
                # # either way i'll include and u can play around
                # # time.sleep(2)
                # controller.face_update(4)
                # bad_face = threading.Thread(target=change_face, args=(face, 0.5,))
                # bad_face.start()
                pts -= 50
                print(pts)
                # Sending bad object to top of screen in a new location
                del enemyX[i]
                del enemyY[i]
                del enemyY_change[i]
                del enemyImg[i]
                i -= 1

            elif enemyY[i]> 3*window[1]/4 + 50:
                del enemyX[i]
                del enemyY[i]
                del enemyY_change[i]
                del enemyImg[i]
                i -= 1

            else:

                screen.blit(enemyImg[i], (enemyX[i], enemyY[i]))
        if(lvl == 2):
            for i in range(len(neutImg)):
                if(i >= len(neutImg)):
                    break
                neutY[i] += neutY_change[i]
                neutCollision = isCollision(neutX[i], neutY[i], playerX, playerY)
                if neutCollision:

                    # DISPLAY THE SURPRISED FACE HERE FOR 1 SECOND AND REVERT BACK TO NEUTRAL
                    #bad_catch.play()
                    # face = random.randint(5, 7)  # HHHHHHHEEEEEEEEEEEEEERRRRRRRRRRRRREEEEEEEEEEEE
                    # controller.face_update(face)
                    # # should i delay here? cuz it's gonna delay the entire program or is that on ur end?
                    # # either way i'll include and u can play around
                    # # time.sleep(2)
                    # controller.face_update(4)
                    # bad_face = threading.Thread(target=change_face, args=(face, 0.5,))
                    # bad_face.start()
                    pts -= 0
                    print(pts)
                    # Sending bad object to top of screen in a new location
                    del neutX[i]
                    del neutY[i]
                    del neutY_change[i]
                    del neutImg[i]
                    i -= 1

                elif neutY[i] > 600:
                    del neutX[i]
                    del neutY[i]
                    del neutY_change[i]
                    del neutImg[i]
                    i -= 1

                else:

                    screen.blit(neutImg[i], (neutX[i], neutY[i]))

        # Setting Boundaries for Recycle Bin --> Doesn't go out of game window
        if playerX <= 0:
            playerX = 0
        elif playerX >= 862:
            playerX = 862

        # Creating Player Object
        screen.blit(playerImg, (playerX, playerY))
        # Show Score Function
        show_score(pts, textX, textY)

        # Timer
        if milliseconds > 1000:
            seconds += 1
            milliseconds -= 1000
        if seconds == 5:
            game_over(pts)

        milliseconds += clock.tick_busy_loop(60)

        # Updating display
        pygame.display.update()


intro()
