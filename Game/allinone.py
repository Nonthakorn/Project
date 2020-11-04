
import pygame
import random
import math
from tkinter import filedialog
from tkinter import *
import json
import importlib
import runpy
import sys
import os
import py_compile
import ctypes
ctypes.windll.user32.SetProcessDPIAware()

def Start_stage(num_stage):
        
    # Initialize pygame
    pygame.init()
    info = pygame.display.Info() # You have to call this before pygame.display.set_mode()
    screen_width,screen_height = info.current_w,info.current_h
    window_width,window_height = screen_width-150,screen_height
    # # screen = pygame.display.mode_ok((window_width,window_height))
    # screen = pygame.display.set_mode((window_width,window_height), pygame.VIDEORESIZE )
    screen = pygame.display.set_mode((window_width,window_height), pygame.FULLSCREEN )
    # size = pygame.display.list_modes()[1]
    # screen = pygame.display.set_mode(size,pygame.RESIZABLE)
    ### config from json file ###
    # gameplay_screen = pygame.display.set_mode((800,600), pygame.NOFRAME )
    with open('grid.json') as json_file:
        data = json.load(json_file)
        for i in data['grid']:
            if i['stage'] == num_stage:
                num_row = i['row']
                num_col = i['column']
                x = i['char_x']
                y = i['char_y']
                brainX = i['brain_x']
                brainY = i['brain_y']
            

    ###input from text file ###
    f = open("input.txt", "r") # ใช้อ่านไฟล์
    fileinput = open("input.txt", "r")
    lstf = []
    for i in f.read():
        lstf.append(i)
    text_file = lstf
    num_of_order = len(text_file)
    num_text = 0
    move = False

    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    
    # This sets the WIDTH and HEIGHT of each grid location
    WIDTH = 50   
    HEIGHT = 50     
    # This sets the margin between each cell
    MARGIN = 1

    lenght = (WIDTH*num_col) + num_col + 100+50
    hight = (HEIGHT*num_row) + num_row + 5 + 50 +50

    
    # Set the HEIGHT and WIDTH of the screen
    # WINDOW_SIZE = [lenght, hight]  #config # configed
    # screen = pygame.display.set_mode(WINDOW_SIZE)
    
    # Set title of screen
    pygame.display.set_caption("Robot Simulation")
    

    # brainX = 2
    # brainY = 3
    def create_grid(x,y):
        if (x*50)+x+50 >= (lenght-97 - move_space) or (y*50)+y+50 >= (hight-5) :
            return print('Error pos ')
        else:
            return (x*50)+x+50,(y*50)+y+50

    def win_stage(x,y):
        brain_x_pos,brain_y_pos = create_grid(brainX,brainY)
        if x == brain_x_pos and y == brain_y_pos:
            screen.blit(text_stageClear,text_stageClearRect)
            pygame.display.update()
            pygame.time.delay(1000)
            x = 0
            y = 0

    char_front = pygame.transform.scale(pygame.image.load('char/front.png'),(50,50))
    char_turnRight =  pygame.transform.scale(pygame.image.load('char/right.png'),(50,50))
    char_turnLeft = pygame.transform.scale(pygame.image.load('char/left.png'),(50,50))
    char_turnback = pygame.transform.scale(pygame.image.load('char/back.png'),(50,50))
    char_lock = pygame.transform.scale(pygame.image.load('char/lock.png'),(45,45))

    move_space = 50
    x,y = create_grid(x,y)  #config

    def create_block(x,y):
            return (x*50)+x+50,(y*50)+y+50

    def lock_space():       
        for k in range(13):
            for m in range(13):
                if k > num_col or m > num_row:
                    i,j = create_block(k,m)
                    screen.blit(char_lock, (i+2,j+3))
    left = False
    right = False
    back = False
    front = True
    def redrawGameWindow():
            
        if left:  
            screen.blit(char_turnLeft, (x, y))                       
        elif right:
            screen.blit(char_turnRight, (x, y))
        elif back:
            screen.blit(char_turnback, (x, y))
        elif front:
            screen.blit(char_front, (x, y))

    def random_brain(brainX,brainY):
        brain = pygame.image.load('char/brain.png')
        brain = pygame.transform.scale(brain,(50,50))
        screen.blit(brain, (create_grid(brainX,brainY)))
        # print('x,y = ', create_grid(brainX,brainY))
        pygame.display.update()

    bigfont = pygame.font.Font('freesansbold.ttf', 35)
    text_stage = bigfont.render('Stage', True, WHITE,GREEN)  #render text  
    text_stageRect = text_stage.get_rect().center = ((window_width-200),window_height- 225)  # นำ tect ไปใส่บน screen 
    text_stagenumber = bigfont.render(str(num_stage), True, WHITE,GREEN)  #render text  
    text_stagenumberRect = text_stagenumber.get_rect().center = ((window_width-75), window_height -225)  # นำ tect ไปใส่บน screen 
    text_stageClear = bigfont.render('Clear', True, BLACK)  #render text  
    text_stageClearRect = text_stageClear.get_rect().center = (((lenght-50)/2.5), hight/2.3)
    ### Start bottom
    startbott1 = bigfont.render('Start', True, WHITE,BLACK)  #render text  
    startbott1Rect = startbott1.get_rect().center = ((window_width-200), window_height -150)  # นำ tect ไปใส่บน screen 
    startbott2 = bigfont.render('Start', True, GREEN,BLACK)  #render text  
    startbott2Rect = startbott2.get_rect().center = ((window_width-200), window_height -150)
    # Loop until the user clicks the close button.
    done = False
    stage_clear = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    facedirection = 0
    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
            if event.type == pygame.KEYDOWN:  # If user clicked close
                if event.key == pygame.K_q:
                    done = True  # Flag that we are done so we exit this loop
        # Set the screen background
        screen.fill(BLACK)

        #set border
        pygame.draw.rect(screen, WHITE, [25,25,window_width-50,5]) #top border
        pygame.draw.rect(screen, WHITE, [25,window_height-25,window_width-50,5]) #bottom border
        pygame.draw.rect(screen, WHITE, [25,25,5,window_height-50]) #left border
        pygame.draw.rect(screen, WHITE, [window_width-30,25,5,window_height-50])  #right border
        pygame.draw.rect(screen, WHITE, [((MARGIN + WIDTH) * 14)+25,25,5,window_height-50])  #game border
        pygame.draw.rect(screen, WHITE, [25,((MARGIN + WIDTH) * 14)+25,(MARGIN + WIDTH) * 14,5])

        # Draw the grid
        for row in range(13):
            for column in range(13):
                color = WHITE
                pygame.draw.rect(screen,
                                color,
                                [(MARGIN + WIDTH) * column + MARGIN+50,
                                (MARGIN + HEIGHT) * row + MARGIN+50,
                                WIDTH,
                                HEIGHT])


        ### move logic
        if move == True:
            key = pygame.key.get_pressed()
            if num_text < num_of_order:
                # if key[pygame.K_LEFT]:
                if text_file[num_text] == 'L':
                    print('l')
                    facedirection +=1 
                    if facedirection >3:
                        facedirection =0
                    if facedirection == 0:
                        left = False
                        right = False
                        back = False
                        front = True
                    if facedirection == 1:
                        left = True
                        right = False
                        back = False
                        front = False
                    if facedirection == 2:
                        left = False
                        right = False
                        back = True
                        front = False
                    if facedirection == 3:
                        left = False
                        right = True
                        back = False
                        front = False
                    redrawGameWindow()
                    pygame.time.wait(100)
                # if key[pygame.K_SPACE]:
                if text_file[num_text] == 'M':
                    # print('m')
                    if right == True and x >= move_space:
                        x -= move_space+MARGIN
                    elif left == True and x <= lenght-97 - move_space-move_space:
                        x += move_space+MARGIN
                    elif back == True and y >= move_space:
                        y -= move_space+MARGIN
                    elif front == True and y <=hight - move_space -move_space:
                        y += move_space+MARGIN
                    redrawGameWindow()
                    pygame.time.wait(100)
                num_text +=1

        # Limit to 60 frames per second
        clock.tick(60)
        pygame.time.wait(100)
        redrawGameWindow()
        random_brain(brainX,brainY) # config
        screen.blit(text_stage,text_stageRect)
        screen.blit(text_stagenumber,text_stagenumberRect)
        lock_space()



    ###Start Click ####
        screen.blit(startbott1,startbott1Rect)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # print(mouse)
        # print(x,y)
        # print('brain',brainX,brainY)
        if lenght - 7 > mouse[0] > lenght-97 and hight-20 > mouse[1] > hight -50 :
            screen.blit(startbott2,startbott2Rect)
            if pygame.mouse.get_pressed() == (1, 0, 0):
                move = True
        pygame.display.update()
        win_stage(x,y)
        # print(x,y)
        # Go ahead and update the screen with what we've drawn.
        # pygame.display.flip()
        pygame.display.update()
    


    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()
    print(num_col ==5)
Start_stage(1)