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
default = 1

##add comment check git
def main(num_stage):
    root = Tk()

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    pygame.init()
    sizewidth = 825
    sizehight = 425
    size = (900, 500) # 900 คือความกว้าง
    screen = pygame.display.set_mode(size)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    bigfont = pygame.font.Font('freesansbold.ttf', 50)
    text_stage = bigfont.render('Stage', True, WHITE,GREEN)  #render text  
    text_stageRect = text_stage.get_rect().center = (480, 160)  # นำ tect ไปใส่บน screen 

    text_stage_num = bigfont.render(str(num_stage), True, WHITE,GREEN)  #render text  
    text_stage_numRect = text_stage_num.get_rect().center = (530, 250)  # นำ tect ไปใส่บน screen 


    ####
    font = pygame.font.Font('freesansbold.ttf', 22) 
    bigfont = pygame.font.Font('freesansbold.ttf', 30) #กำหนดฟอนต์
    #### Start bottom ###  
    startbot0 = font.render('Start', True, WHITE,GREEN)  #render text  
    startbotRect0 = startbot0.get_rect().center = (255, 135)  # นำ tect ไปใส่บน screen  
    startbot1 = font.render('Start', True, RED,GREEN)  #render text  
    startbotRect1 = startbot1.get_rect().center = (255, 135)  # นำ tect ไปใส่บน screen  
    ####################

    #### select_stage0 bottom ###  
    select_stage0 = font.render('Select Stage', True, WHITE,GREEN)  #render text  
    select_stageRect0 = select_stage0.get_rect().center = (255, 235)  # นำ tect ไปใส่บน screen  
    select_stage1 = font.render('Select Stage', True, RED,GREEN)  #render text  
    select_stageRect1 = select_stage1.get_rect().center = (255, 235)  # นำ tect ไปใส่บน screen  
    ####################

    #### Exit bottom ###  
    Exit0 = font.render('Exit', True, WHITE,GREEN)  #render text  
    ExitRect0 = Exit0.get_rect().center = (255, 335)  # นำ tect ไปใส่บน screen  
    Exit1 = font.render('Exit', True, RED,GREEN)  #render text  
    ExitRect1 = Exit1.get_rect().center = (255, 335)  # นำ tect ไปใส่บน screen  
    ####################


    def startbottom():
        screen.blit(startbot0, startbotRect0)
        mouse = pygame.mouse.get_pos()
        if 300 > mouse[0] > 255 and 155 > mouse[1] > 135 :
            screen.blit(startbot1, startbotRect1)
            if pygame.mouse.get_pressed() == (1, 0, 0):
                Start_stage(num_stage)

    def select_stagebottom():
        screen.blit(select_stage0, select_stageRect0)
        mouse = pygame.mouse.get_pos()
        if 385 > mouse[0] > 255 and 255 > mouse[1] > 235 :
            screen.blit(select_stage1, select_stageRect1)
            if pygame.mouse.get_pressed() == (1, 0, 0):
                Select_stage()


    def exitbottom():
        screen.blit(Exit0, ExitRect0)
        mouse = pygame.mouse.get_pos()
        if 295 > mouse[0] > 255 and 355  > mouse[1] > 335 :
            screen.blit(Exit1, ExitRect1)
            if pygame.mouse.get_pressed() == (1, 0, 0):
                sys.exit()
    pygame.init()
    run = True
    while run:
        screen.fill(WHITE)
        pygame.time.delay(100)
        pygame.draw.rect(screen, GREEN, [200,75,500,350])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        startbottom()
        select_stagebottom()
        exitbottom()
        # print(run)
        ### mouse pos check ###
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # print(mouse)
        ########################
        #### text show #####
        screen.blit(text_stage, text_stageRect)
        screen.blit(text_stage_num,text_stage_numRect)


        pygame.display.update()
    pygame.quit()

def Select_stage():

    root = Tk()

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    pygame.init()
    sizewidth = 825
    sizehight = 425
    size = (900, 500) # 900 คือความกว้าง
    screen = pygame.display.set_mode(size)

    bigfont = pygame.font.Font('freesansbold.ttf', 50)
    text_stage = bigfont.render('Choose Stage', True, WHITE,GREEN)  #render text  
    text_stageRect = text_stage.get_rect().center = (260, 115)  # นำ tect ไปใส่บน screen 


    ####
    font = pygame.font.Font('freesansbold.ttf', 22) 
    bigfont = pygame.font.Font('freesansbold.ttf', 30) #กำหนดฟอนต์
    #### stage_one bottom ###  
    stage_one_0 = font.render('Stage 1 ', True, WHITE,GREEN)  #render text  
    stage_one_Rect0 = stage_one_0.get_rect().center = (230, 200)  # นำ tect ไปใส่บน screen  
    stage_one_1 = font.render('Stage 1 ', True, RED,GREEN)  #render text  
    stage_one_Rect1 = stage_one_1.get_rect().center = (230, 200)  # นำ tect ไปใส่บน screen  
    ####################

    #### stage_two bottom ###  
    stage_two_0 = font.render('Stage 2 ', True, WHITE,GREEN)  #render text  
    stage_two_Rect0 = stage_two_0.get_rect().center = (400, 200)  # นำ tect ไปใส่บน screen  
    stage_two_1 = font.render('Stage 2 ', True, RED,GREEN)  #render text  
    stage_two_Rect1 = stage_two_1.get_rect().center = (400, 200)  # นำ tect ไปใส่บน screen  
    ####################

        #### stage_three bottom ###  
    stage_three_0 = font.render('Stage 3 ', True, WHITE,GREEN)  #render text  
    stage_three_Rect0 = stage_three_0.get_rect().center = (570, 200)  # นำ tect ไปใส่บน screen  
    stage_three_1 = font.render('Stage 3 ', True, RED,GREEN)  #render text  
    stage_three_Rect1 = stage_three_1.get_rect().center = (570, 200)  # นำ tect ไปใส่บน screen  
    ####################

    #### back bottom ###  
    back0 = font.render('back', True, WHITE,GREEN)  #render text  
    backRect0 = back0.get_rect().center = (255, 335)  # นำ tect ไปใส่บน screen  
    back1 = font.render('back', True, RED,GREEN)  #render text  
    backRect1 = back1.get_rect().center = (255, 335)  # นำ tect ไปใส่บน screen  
    ####################



    def stage_one():
        screen.blit(stage_one_0, stage_one_Rect0)
        mouse = pygame.mouse.get_pos()
        if 305 > mouse[0] > 230 and 225 > mouse[1] > 200 :
            screen.blit(stage_one_1, stage_one_Rect1)
            if pygame.mouse.get_pressed() == (1, 0, 0):
                main(1)
    
    def stage_two():
        screen.blit(stage_two_0, stage_two_Rect0)
        mouse = pygame.mouse.get_pos()
        if 475 > mouse[0] > 400 and 225 > mouse[1] > 200 :
            screen.blit(stage_two_1, stage_two_Rect1)
            if pygame.mouse.get_pressed() == (1, 0, 0):
                main(2)
    
    
    def stage_three():
        screen.blit(stage_three_0, stage_three_Rect0)
        mouse = pygame.mouse.get_pos()
        if 645 > mouse[0] > 570 and 225 > mouse[1] > 200 :
            screen.blit(stage_three_1, stage_three_Rect1)
            if pygame.mouse.get_pressed() == (1, 0, 0):
                main(3)

    def back():
        screen.blit(back0, backRect0)
        mouse = pygame.mouse.get_pos()
        if 295 > mouse[0] > 255 and 355  > mouse[1] > 335 :
            screen.blit(back1, backRect1)
            if pygame.mouse.get_pressed() == (1, 0, 0):
                main()
    pygame.init()
    run = True
    while run:
        screen.fill(WHITE)
        pygame.time.delay(100)
        pygame.draw.rect(screen, GREEN, [200,75,500,350])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        
        back()
        stage_one()
        stage_two()
        stage_three()
        # print(run)
        ### mouse pos check ###
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        print(mouse)
        ########################
        #### text show #####
        screen.blit(text_stage, text_stageRect)


        pygame.display.update()
    pygame.quit()

def Start_stage(num_stage):
        
    # Initialize pygame
    pygame.init()
    ### config from json file ###
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

    lenght = (WIDTH*num_col) + num_col + 100
    hight = (HEIGHT*num_row) + num_row + 5

    
    # Set the HEIGHT and WIDTH of the screen
    WINDOW_SIZE = [lenght, hight]  #config # configed
    screen = pygame.display.set_mode(WINDOW_SIZE)
    
    # Set title of screen
    pygame.display.set_caption("Robot Simulation")
    

    # brainX = 2
    # brainY = 3
    def create_grid(x,y):
        if (x*50)+x >= (lenght-97 - move_space) or (y*50)+y >= (hight-5) :
            return print('Error pos ')
        else:
            return (x*50)+x,(y*50)+y

    def win_stage(x,y):
        brain_x_pos,brain_y_pos = create_grid(brainX,brainY)
        if x == brain_x_pos and y == brain_y_pos:
            screen.blit(text_stageClear,text_stageClearRect)
            pygame.display.update()
            pygame.time.delay(1000)
            x = 0
            y = 0
            main(num_stage)

    char_front = pygame.transform.scale(pygame.image.load('char/front.png'),(50,50))
    char_turnRight =  pygame.transform.scale(pygame.image.load('char/right.png'),(50,50))
    char_turnLeft = pygame.transform.scale(pygame.image.load('char/left.png'),(50,50))
    char_turnback = pygame.transform.scale(pygame.image.load('char/back.png'),(50,50))

    move_space = 50
    x,y = create_grid(x,y)  #config

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
    text_stageRect = text_stage.get_rect().center = ((lenght-97), 25)  # นำ tect ไปใส่บน screen 
    text_stagenumber = bigfont.render(str(num_stage), True, WHITE,GREEN)  #render text  
    text_stagenumberRect = text_stagenumber.get_rect().center = ((lenght-57), 75)  # นำ tect ไปใส่บน screen 
    text_stageClear = bigfont.render('Clear', True, BLACK)  #render text  
    text_stageClearRect = text_stageClear.get_rect().center = (((lenght-100)/2.5), hight/2.3)
    ### Start bottom
    startbott1 = bigfont.render('Start', True, WHITE,BLACK)  #render text  
    startbott1Rect = startbott1.get_rect().center = ((lenght-97), hight -50)  # นำ tect ไปใส่บน screen 
    startbott2 = bigfont.render('Start', True, GREEN,BLACK)  #render text  
    startbott2Rect = startbott2.get_rect().center = ((lenght-97), hight -50)
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
        # Set the screen background
        screen.fill(BLACK)
    
        # Draw the grid
        for row in range(num_row):
            for column in range(num_col):
                color = WHITE
                pygame.draw.rect(screen,
                                color,
                                [(MARGIN + WIDTH) * column + MARGIN,
                                (MARGIN + HEIGHT) * row + MARGIN,
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
        pygame.display.flip()
        pygame.display.update()
    


    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()
main(default)
