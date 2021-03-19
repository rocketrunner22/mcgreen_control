import pygame
from pygame import mixer
import time
import sys
import random
import threading

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

class Level:
    def __init__(self):
        self.game_screen_vshift = (window_size[1]-634)/2
        self.game_screen_hshift = (window_size[0]-926)/2
        self.background = None
        self.objs = []
        self.flipped = []
        self.hints = []
        self.isTimer = False
        self.timer = 0

    def setBackground(self, bg):
        self.background = bg

    def setTimer(self, timer):
        self.isTimer = True
        self.timer = timer

    def addObj(self, obj, flippedobj, x_pos, y_pos, x_off, y_off, hint):
        x_pos += self.game_screen_hshift
        y_pos += self.game_screen_vshift
        xuplimit = x_pos + x_off
        xlowlimit = x_pos - 10
        yuplimit = y_pos + y_off
        ylowlimit = y_pos - 10

        self.objs.append([obj,flippedobj, x_pos, y_pos, xuplimit, xlowlimit, yuplimit, ylowlimit])
        self.hints.append(hint)
        self.flipped.append(0)

    def run(self):

        start_tick = pygame.time.get_ticks()
        self.flipped = [0 for _ in self.objs]
        hint = font.render(" ", True, (0, 0, 0))
        mixer.music.load('backgroundmsc.wav')
        mixer.music.play(-1)
        screen.fill((255, 255, 255))
        screen.blit(menu, (0, 0))
        screen.blit(menu, (0,window_size[1]/2))
        back = Button(Back_Arrow, Back_Arrow, (10, 10, 100, 80))

        back.generate()

        pygame.display.update()

        while True:


            screen.blit(self.background, (self.game_screen_hshift, self.game_screen_vshift))
            screen.blit(Back_Arrow, (10, 10))
            screen.blit(hint, (50+self.game_screen_hshift,85+self.game_screen_vshift))
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            print(mouse)

            for event in pygame.event.get():
                # Quitting the Game by X-ing out Window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                # keystroke check (right/left) and changing val of playerX_change to +/- based on keypress
                #if event.type == pygame.KEYDOWN:
                #    if event.key == pygame.K_ESCAPE:
                #        level_select()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back.is_pressed(True):
                        level_select()

            for num, object in enumerate(self.objs):
                screen.blit(object[0 + self.flipped[num]], (object[2], object[3]))
                if object[-4] > mouse[0] > object[-3] and object[-2] > mouse[1] > object[-1] and click[0] == 1:
                    #screen.blit(self.background, (0, 0))
                    #back.generate()
                    pygame.display.update(pygame.Rect(object[-3], object[-1], object[-4]-object[-3], object[-2]-object[-1]))
                    self.flipped[num] = 1

            else:
                screen.blit(hintp, (815+self.game_screen_hshift, 25+self.game_screen_vshift))
                if 900+self.game_screen_hshift > mouse[0] > 815+self.game_screen_hshift and 100+self.game_screen_vshift > mouse[1] > 25+self.game_screen_vshift:
                    screen.blit(hintp, (815+self.game_screen_hshift, 25+self.game_screen_vshift))
                    if click[0] == 1:
                        for objnum, flip in enumerate(self.flipped):
                            if not flip:
                                hint = font.render(self.hints[objnum], True, (0, 0, 0))
                                break
                else:
                    screen.blit(hintp, (815+self.game_screen_hshift, 25+self.game_screen_vshift))


            if self.isTimer:
                    time = self.timer
                    seconds_elapsed = (pygame.time.get_ticks()-start_tick)//1000
                    time_left = time-seconds_elapsed
                    time_text = font.render(str(time_left), True, (0, 0, 0))
                    screen.blit(time_text, (5+self.game_screen_hshift, 85+self.game_screen_vshift))
                    if time_left <= 0:
                        gamelose()

            if all(flip == 1 for flip in self.flipped):
                gamewin()
            pygame.display.update()

pygame.init()
window_size = (1080, 1920)
screen = pygame.display.set_mode(window_size)

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
darker_red = (200, 0, 0)
green = (0, 255, 0)
darker_green = (0, 200, 0)
blue = (50, 89, 250)
darker_blue = (35, 67, 250)
yellow = (255, 255, 0)
darker_yellow = (200, 200, 0)

largeText = pygame.font.Font('FreeSansBold.ttf', 70)   #Large text, ideal for headings (normally 64)
mediumText = pygame.font.Font('FreeSansBold.ttf', 48)   #Medium text, ideal for subheadings
smallText =  pygame.font.Font('FreeSansBold.ttf', 14)   #Small text, ideal for small buttons

# backgrounds
Back_Arrow = pygame.image.load('Back_Arrow.png')
Back_Arrow = pygame.transform.scale(Back_Arrow, (100,70))
classroomlvl = pygame.image.load('classroomlvl.png')
kitchenlvl = pygame.image.load('kitchenlvl.png')
bedroomlvl = pygame.image.load('bedroomlvl.png')
menu = pygame.image.load('menubkg.png')
menu = pygame.transform.scale(menu, (window_size[0], window_size[1]//2))
helps = pygame.image.load('helpback.png')
helpbkg = pygame.image.load('helpbkglegit.png')
helpbkg = pygame.transform.scale(helpbkg, window_size)
helps = pygame.transform.scale(helps, (926, 634))
gamewon = pygame.image.load('winner.png')
gamelost = pygame.image.load('loser.png')

# Background Music
mixer.music.load('backgroundmsc.wav')

# kitchen level items
can = pygame.image.load('can.png')
looseplant = pygame.image.load('loose_plant.png')
papertowel = pygame.image.load('paper_towel.png')
pottedplant = pygame.image.load('potted_plant.png')
#recyclingarrow = pygame.image.load('recycling_arrow.png')
recyclingarrow = pygame.image.load('paper_towel_recycling.png')
runningfaucet = pygame.image.load('running_faucet.png')
towels = pygame.image.load('towels.png')
tick = pygame.image.load('tick.png')

# Buttons
playb = pygame.image.load('playbtn.png')
playb = pygame.transform.scale(playb, (750,222))
helpb = pygame.image.load('helpbtn.png')
helpb = pygame.transform.scale(helpb, (750,222))
exitb = pygame.image.load('quitbtn.png')
exitb = pygame.transform.scale(exitb, (750,222))
lvl1 = pygame.image.load('lvl1.png')
lvl1 = pygame.transform.scale(lvl1, (750,222))
lvl2 = pygame.image.load('lvl2.png')
lvl2 = pygame.transform.scale(lvl2, (750,222))
lvl3 = pygame.image.load('lvl3.png')
lvl3 = pygame.transform.scale(lvl3, (750,222))
invplayb = pygame.image.load('invplayb.png')
invplayb = pygame.transform.scale(invplayb, (750,222))
invhelpb = pygame.image.load('invhelpb.png')
invhelpb = pygame.transform.scale(invhelpb, (750,222))
invexitb = pygame.image.load('invquitb.png')
invexitb = pygame.transform.scale(invexitb, (750,222))
invlvl1 = pygame.image.load('invlvl1.png')
invlvl1 = pygame.transform.scale(invlvl1, (750,222))
invlvl2 = pygame.image.load('invlvl2.png')
invlvl2 = pygame.transform.scale(invlvl2, (750,222))
invlvl3 = pygame.image.load('invlvl3.png')
invlvl3 = pygame.transform.scale(invlvl3, (750,222))

hintp = pygame.image.load('hint.png')
blank = pygame.image.load('blank.png')

# classroom level items
closedcurtains = pygame.image.load('cosed_curtains.png')
opencurtains = pygame.image.load('open_curtains.png')
trash = pygame.image.load('trash.png')
compost = pygame.image.load('compost.png')
laptopoff = pygame.image.load('laptop_off.png')
laptopon = pygame.image.load('laptop_on.png')
papertrash = pygame.image.load('paper_trash.png')
paperrecycling = pygame.image.load('paper_recycling.png')

# bedroom level items
openwindow = pygame.image.load('open_window.png')
closedwindow = pygame.image.load('closed_window.png')
loosepaper = pygame.image.load('loose_paper.png')
whiteboard = pygame.image.load('whiteboard.png')
waterbottle = pygame.image.load('waterbottle.png')
reusablewb = pygame.image.load('reusable_water_bottle.png')
ipad = pygame.image.load('ipad.png')
lighton = pygame.image.load('light_on.png')
lightoff = pygame.image.load('light_off.png')

pygame.display.set_caption("What's Wrong With The Room?")
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)

font = pygame.font.Font('Bubblegum.ttf', 32)

level1 = Level()
level1.setBackground(classroomlvl)
level1.addObj(closedcurtains, opencurtains, 750, 100, 100, 130,"Hint: Always try to use Natural Sunlight")
level1.addObj(papertrash, paperrecycling, 280, 320, 100, 130, "Hint: Always Recycle Paper")
level1.addObj(trash, compost, 58, 265, 107, 145, "Hint: Turn food waste into Compost")
level1.addObj(laptopon, laptopoff, 440, 315, 110, 65,"Hint: Turn off things you aren't using")

level2 = Level()
level2.setBackground(bedroomlvl)
level2.addObj(blank, ipad, 540, 370, 55, 55, "Hint: Turn off things you aren't using")
level2.addObj(loosepaper,whiteboard, 240, 365, 80, 45, "Hint: Recycle Paper as much as Possible")
level2.addObj(waterbottle, reusablewb, 20, 420, 40, 80, "Hint: Use Very Little Plastic (Bottles, Bags, etc.) ")
level2.addObj(openwindow, closedwindow,650, 120, 170, 170, "Hint: Close Windows to Keep Your House Warm/Cold")
level2.addObj(lighton, lightoff, 290, 240, 55, 50, "Hint: Turn off things you aren't using")

level3 = Level()
level3.setBackground(kitchenlvl)
level3.setTimer(90)
level3.addObj(papertowel, recyclingarrow, 550, 540, 75, 65, "Hint: Use Things made from Recycled Materials")
level3.addObj(papertowel, towels, 375, 325, 75, 55, "Hint: Avoid Using Paper as much as you can")
level3.addObj(can, pottedplant, 640, 305, 40, 65, "Hint: Create your own projects with recyclables ")
level3.addObj(runningfaucet, blank, 265, 300, 75, 55, "Hint: Don't leave the water running")
level3.addObj(blank, tick, 5, 345, 155, 190, "Hint: Turn off/Close things you aren't using")



def text_objects(text, font, color=(0,0,0)):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()



def intro():
    mixer.music.load('backgroundmsc.wav')
    mixer.music.play(-1)
    #controller.face_update(4)  # HHHHHHHHHHHHHHEEEEEEEEEEEEEEERRRRRRRRRRRRRRRREEEEEEEEEEEEEE
#    controller.head_update([90,90])
    screen.fill((255, 255, 255))
    screen.blit(menu, (0, 0))
    screen.blit(menu, (0,window_size[1]/2))
    playbutton = Button(invplayb, playb, (window_size[0]/2 - 750/2, window_size[1]/4, 750, 222))
    helpbutton = Button(invhelpb, helpb, (window_size[0]/2 - 750/2,  window_size[1]/2, 750, 222))
    quitbutton = Button(invexitb, exitb, (window_size[0]/2 - 750/2,  3*window_size[1]/4, 750, 222))
    TextSurf, TextRect = text_objects("What's Wrong with the Room?", largeText, black)
    TextRect.center = (window_size[0]/2,190)
    screen.blit(TextSurf,TextRect)
    bmenu = True
    while bmenu:

        playbutton.generate()
        helpbutton.generate()
        quitbutton.generate()
        for event in pygame.event.get():
            # Quitting the Game by X-ing out Window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # if event.type == pygame.MOUSEBUTTONUP:
            #     if 360 + 220 > mouse[0] > 360 and 80 + 70 > mouse[1] > 80:
            #         level_select()
            #     elif 360 + 220 > mouse[0] > 360 and 170 + 70 > mouse[1] > 170:
            #         help_screen()
            #     elif 360 + 220 > mouse[0] > 360 and 260 + 70 > mouse[1] > 260:
            #         pygame.quit()
            #         quit()
            if event.type == pygame.MOUSEBUTTONUP:
                touch_status = True
                if(playbutton.is_pressed(touch_status)):
                    level_select()
                if(helpbutton.is_pressed(touch_status)):
                    help_screen()
                if(quitbutton.is_pressed(touch_status)):
                    pygame.quit()
                    quit()



        # mouse = pygame.mouse.get_pos()
        # click = pygame.mouse.get_pressed()
        # print(click)
        # if 360 + 220 > mouse[0] > 360 and 80 + 70 > mouse[1] > 80:
        #     screen.blit(invplayb, (360, 80))
        # else:
        #     screen.blit(playb, (360, 80))
        #
        # if 360 + 220 > mouse[0] > 360 and 170 + 70 > mouse[1] > 170:
        #     screen.blit(invhelpb, (360, 170))
        # else:
        #     screen.blit(helpb, (360, 170))
        #
        # if 360 + 220 > mouse[0] > 360 and 260 + 70 > mouse[1] > 260:
        #     screen.blit(invexitb, (360, 260))
        #
        # else:
        #     screen.blit(exitb, (360, 260))

        pygame.display.update()


def help_screen():
    mixer.music.load('backgroundmsc.wav')
    mixer.music.play(-1)
    bhelp = True
    back = Button(Back_Arrow, Back_Arrow, (10, 10, 100, 80))
    while bhelp:

        screen.fill((255, 255, 255))
        screen.blit(helpbkg, (0,0))
        '''
        screen.blit(helps, (0, 0))
        TextSurf, TextRect = text_objects('How to Play:', largeText, red)
        TextRect.center = ((window_size[0] / 2), (window_size[1] / 6))

        line_spacing = 75   #Spacing between each line of instructions

        Line1Surf, Line1Rect = text_objects('1.) The goal of this game is to make the room more environmentally efficient. Click items that you think need to be improved.', smallText, red)
        Line1Rect.center = ((window_size[0] / 2), (window_size[1] / 4) + (0.5 * 300))

        Line2Surf, Line2Rect = text_objects('2.) If you are lost or would like guidance press the question mark button in the top right.', smallText, red)
        Line2Rect.center = ((window_size[0] / 2), (window_size[1] / 4) + (300 / 2) + (2 * line_spacing) - 10)

        Line3Surf, Line3Rect = text_objects('3.) Once you complete the game, press escape to play again. Press escape to go back to the home screen. ', smallText, red)
        Line3Rect.center = ((window_size[0] / 2), (window_size[1] / 4) + (300 / 2) + (4 * line_spacing))


        #Make entire screen white to clean it

        #Write text to buffer
        screen.blit(TextSurf, TextRect)
        screen.blit(Line1Surf, Line1Rect)
        screen.blit(Line2Surf, Line2Rect)
        screen.blit(Line3Surf, Line3Rect)
        #comments
        #help_message = font.render("The goal of this game is to make the room more environmentally efficient. Click items that you think need to be improved. If you are lost or would like guidance press the question mark button in the top right. Once you complete the game, press escape to play again. ", True, (0, 0, 255))
        '''
        #screen.blit(help_message, (0, 0))
        back.generate()
        pygame.display.update()

        for event in pygame.event.get():
            # Quitting the Game by X-ing out Window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # keystroke check (right/left) and changing val of playerX_change to +/- based on keypress
            if event.type == pygame.MOUSEBUTTONDOWN:
                touch_status = True
                if(back.is_pressed(touch_status)):
                    intro()
        pygame.display.update()


def level_select():
    #pygame.time.delay(720)
    bmenu = True
    mixer.music.load('backgroundmsc.wav')
    mixer.music.play(-1)
    screen.fill((255, 255, 255))
    screen.blit(menu, (0, 0))
    screen.blit(menu, (0,window_size[1]/2))
    back = Button(Back_Arrow, Back_Arrow, (10, 10, 100, 80))
    lvl1b = Button(invlvl1, lvl1, (window_size[0]/2 - 750/2, window_size[1]/4, 750, 222))
    lvl2b = Button(invlvl2, lvl2, (window_size[0]/2 - 750/2, window_size[1]/2, 750, 222))
    lvl3b = Button(invlvl3, lvl3, (window_size[0]/2 - 750/2, 3*window_size[1]/4, 750, 222))
    back.generate()
    pygame.display.update()
    while bmenu:
        # screen.fill((255, 255, 255))
        # screen.blit(menu, (0, 0))
        for event in pygame.event.get():

            lvl1b.generate()
            lvl2b.generate()
            lvl3b.generate()
            back.generate()

            # Quitting the Game by X-ing out Window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.is_pressed(True):
                    intro()

            if event.type == pygame.MOUSEBUTTONUP:
                touch_status = True
                if(lvl1b.is_pressed(touch_status)):
                    level1.run()
                if(lvl2b.is_pressed(touch_status)):
                    level2.run()
                if(lvl3b.is_pressed(touch_status)):
                    level3.run()



            pygame.display.update()


def gamewin():
    #face = random.randint(1, 3)  # HEEEEEEEEEEEEEEEEEERRRRRRRRRRRRRRRRRREEEEEEEEEEEEEE
    #controller.face_update(face)
    # These commands won't over write themselves right? like if i say these three in a row
    # it'll hit all of the positions before going back to [90,90]?
    # controller.head_update([90, 45])
    # controller.head_update([90, 135])
    # controller.head_update([90, 90])
    #rotate=threading.Thread(target=rotate_head, args=(True, [45, 135, 90]))
    #rotate.start()
    bgame = True
    mixer.music.load('game_won.wav')
    mixer.music.play()
    back = Button(Back_Arrow, Back_Arrow, (10, 10, 100, 80))
    game_screen_vshift = (window_size[1]-634)/2
    game_screen_hshift = (window_size[0]-926)/2

    pygame.display.update()
    while bgame:
        #pygame.time.delay(60)
        screen.fill((255, 255, 255))
        screen.blit(gamewon, (game_screen_hshift,game_screen_vshift))
        back.generate()
        for event in pygame.event.get():
            # Quitting the Game by X-ing out Window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.is_pressed(True):
                    level_select()
            #if event.type == pygame.KEYDOWN:
            #    if event.key == pygame.K_ESCAPE:
            #        level_select()
        pygame.display.update()
        #test

def gamelose():
    face = random.randint(5, 7)  # HHHHHHHHHHHHHHEEEEEEEEEEEEERRRRRRRRRRRREEEEEEEEEEEE
    #controller.face_update(face)
    #See game_won head update comments
    # controller.head_update([45, 90])
    # controller.head_update([135, 90])
    # controller.head_update([90, 90])
    #rotate=threading.Thread(target=rotate_head, args=(False, [45, 135, 90]))
    #rotate.start()
    bgame = True
    mixer.music.load('game_lose.wav')
    mixer.music.play()
    back = Button(Back_Arrow, Back_Arrow, (10, 10, 100, 80))
    game_screen_vshift = (window_size[1]-634)/2
    game_screen_hshift = (window_size[0]-926)/2
    while bgame:
        screen.fill((255, 255, 255))
        screen.blit(gamelost, (game_screen_hshift, 50+game_screen_vshift))
        back.generate()
        for event in pygame.event.get():
            # Quitting the Game by X-ing out Window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.is_pressed(True):
                    level_select()
            #if event.type == pygame.KEYDOWN:
            #    if event.key == pygame.K_ESCAPE:
            #        level_select()
        pygame.display.update()

intro()
