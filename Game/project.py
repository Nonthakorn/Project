
import pygame
from pygame.locals import *
import cv2
import random
import math
from tkinter import filedialog
from tkinter import *
import json
import importlib
import numpy
import runpy
import sys
import os
import py_compile
import ctypes
import runyolo
ctypes.windll.user32.SetProcessDPIAware()

def Start_stage(num_stage):
        
    # Initialize pygame ##setscreen
    pygame.init()
    info = pygame.display.Info() 
    screen_width,screen_height = info.current_w,info.current_h
    window_width,window_height = screen_width,screen_height
    screen = pygame.display.set_mode((window_width,window_height), pygame.FULLSCREEN )
    ####### read_json file อ่าน json ##### 
    with open(num_stage) as json_file:
        data = json.load(json_file)
        for i in data['grid']:
            stage = i ['stage']
            num_row = i['row']
            num_col = i['column']
            x = i['char_x']
            y = i['char_y']
            brainX = i['brain_x']
            brainY = i['brain_y']
            box = i['box']
            box_x = i['box_x']
            box_y = i['box_y']
            
    ###input from text file ###  read_input
    def read_input():
        f = open("input.txt", "r") # ใช้อ่านไฟล์
        fileinput = open("input.txt", "r")
        lstf = []
        for i in f.readlines(-3):
            lstf.append(i.rstrip())
        text_file = lstf
        num_of_order = len(text_file)
        return text_file,num_of_order
    num_text = 0
    move = False

    def show_command():
        text_file,num_of_order = read_input()
        if num_text == 0:
            print('sth')
    # Define some colors  Define_color
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    
    # This sets the WIDTH and HEIGHT of each grid location  ### set_W_H 
    WIDTH = 50   
    HEIGHT = 50 
    char_scale = 50
    move_space = 50
    bigfont = pygame.font.Font('freesansbold.ttf', 35)
    # This sets the margin between each cell
    MARGIN = 1

    if screen_width <= 1900:
        WIDTH = round(WIDTH * 0.711)
        HEIGHT = round(HEIGHT *0.711)
        char_scale = round(char_scale *0.711)
        move_space = round(move_space*0.711)
        bigfont = pygame.font.Font('freesansbold.ttf', round(35*0.711))
    lenght = (WIDTH*num_col) + num_col + (WIDTH*3)
    hight = (HEIGHT*num_row) + num_row + (HEIGHT*2)
    
    # Set title of screen
    pygame.display.set_caption("Robot Simulation")
    ### สร้างตำแหน่งที่ตั้งของตัว จะprint error ถ้าต่ำแหน่งเกินจำนวนของ col และ row Create_def
    def create_grid(x,y):
        if (x*move_space)+x+50 >= (lenght) or (y*move_space)+y+50 >= (hight) :
            return print('Error pos ')
        else:
            return (x*move_space)+x+50,(y*move_space)+y+50
     ################ สร้างตัวบล็อคไม่ให้เดิน จะปลดล็อกตามด่านที่ config
    def create_block(x,y):
            return (x*move_space)+x+50,(y*move_space)+y+50

    def lock_space():       
        for k in range(13):
            for m in range(13):
                if k > num_col or m > num_row:
                    i,j = create_block(k,m)
                    screen.blit(char_lock, (i+2,j+3))
    def win_stage(x,y):
        brain_x_pos,brain_y_pos = create_grid(brainX,brainY)
        if x == brain_x_pos and y == brain_y_pos:
            showtext('CLEAR',lenght/3,hight/2,BLACK)
            pygame.time.delay(0)
            x = 0
            y = 2
            print("win")
    def collide(x,y):
        building_x_pos,building_y_pos = create_grid(box_x,box_y)
        if x < abs(building_x_pos - 1) and y < abs(building_y_pos-1):
            x_collinde = False
            y_collinde = False
        elif x < abs(building_x_pos - 1):
            x_collinde = True
            y_collinde = False
        elif y < abs(building_y_pos - 1):
            x_collinde = False
            y_collinde = True
        return x_collinde,y_collinde
    x,y = create_grid(x,y)  #config
    ############# set_object_char
    char_front = pygame.transform.scale(pygame.image.load('char/front.png'),(char_scale,char_scale))
    char_turnRight =  pygame.transform.scale(pygame.image.load('char/right.png'),(char_scale,char_scale))
    char_turnLeft = pygame.transform.scale(pygame.image.load('char/left.png'),(char_scale,char_scale))
    char_turnback = pygame.transform.scale(pygame.image.load('char/back.png'),(char_scale,char_scale))
    char_lock = pygame.transform.scale(pygame.image.load('char/lock.png'),(char_scale-5,char_scale-5))


    left = False
    right = False
    back = False
    front = True

    ########## 
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
        brain = pygame.transform.scale(brain,(char_scale,char_scale))
        screen.blit(brain, (create_grid(brainX,brainY)))
        # print('x,y = ', create_grid(brainX,brainY))

    def box_block(building_X,building_Y):
        building = pygame.image.load('char/building.png')
        building = pygame.transform.scale(building,(char_scale,char_scale))
        screen.blit(building, (create_grid(building_X,building_Y)))
    ### text_and_botton
    def botton(text,textx,texty,color,hover_col): # str input
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        my_text = bigfont.render(text, True, color)
        my_text_hover = bigfont.render(text, True, hover_col)
        text_width = my_text.get_width()
        text_height = my_text.get_height()
        screen.blit(my_text,(round(textx),round(texty)))
        if textx +text_width > mouse[0] > textx and texty +text_height > mouse[1] > texty:
            screen.blit(my_text_hover,(textx,texty))
            if pygame.mouse.get_pressed() == (1, 0, 0): 
                return True

    def showtext(text,textx,texty,color):
        my_text = bigfont.render(text, True, color)
        text_width = my_text.get_width()
        text_height = my_text.get_height()
        screen.blit(my_text,(round(textx),round(texty)))
        return text_height


    # text_stageClear = bigfont.render('CLEAR', True, BLACK)  #render text  
    # text_stageClearRect = text_stageClear.get_rect().center = (((lenght-50)/2.5), hight/2.3)
    # Loop until the user clicks the close button.
    done = False
    stage_clear = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    ######################## OPENCV #####################################
    color=False#True#False
    camera_index = 0
    camera=cv2.VideoCapture(camera_index)
    camera.set(3,800)
    camera.set(4,600)
    screen = pygame.display.set_mode((window_width,window_height), pygame.FULLSCREEN ) ####

    def getCamFrame(color,camera):
        retval,frame=camera.read()
        realframe = frame
        frame = frame.swapaxes(0, 0)
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        # frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        # frame=cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB)
        frame=numpy.rot90(frame)
        frame=pygame.surfarray.make_surface(frame) #I think the color error lies in this line?
        return frame,realframe

    def blitCamFrame(frame,screen):
        screen.blit(frame,(round(window_width*0.6),30))
        return screen
    check = 0
    facedirection = 0
    lst_command = []
    win = 0
    check_start = 0
    text_file,num_of_order = read_input()
    for j in range(num_of_order): 
        lst_command.append(35*j)
    # -------- Main_Program_Loop -----------
    pygame.display.update()
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
            if event.type == pygame.KEYDOWN:  # If user clicked close
                if event.key == pygame.K_q:
                    done = True  # Flag that we are done so we exit this loop
        # Set the screen background
        screen.fill(BLACK)


        frame,realframe = getCamFrame(color, camera)
        # screen = blitCamFrame(frame, screen)
        if check == 1:
            cv2.imwrite("test_image/image1.JPG", realframe)
            print('capture sucsuees')
            check = 2

        if check == 2 :
            runyolo.yolo()
            Start_stage(num_stage)
            check = 3
        yolo_check = botton("RUNYOLO",((MARGIN + WIDTH) * 14)+50, window_height -150,WHITE,RED)
        if yolo_check:
            check = 1
        if check == 3:
            showtext("YOLO SUCCESS!!",((MARGIN + WIDTH) * 14)+50,window_height -100,WHITE)
            yolo_check = None
        ## OPENCV2
        
        #set_border
        pygame.draw.rect(screen, WHITE, [25,25,window_width-50,5]) #top border
        pygame.draw.rect(screen, WHITE, [25,window_height-25,window_width-50,5]) #bottom border
        pygame.draw.rect(screen, WHITE, [25,25,5,window_height-50]) #left border
        pygame.draw.rect(screen, WHITE, [window_width-30,25,5,window_height-50])  #right border
        pygame.draw.rect(screen, WHITE, [((MARGIN + WIDTH) * 14)+25,25,5,window_height-50])  #game border
        pygame.draw.rect(screen, WHITE, [25,((MARGIN + WIDTH) * 14)+25,(MARGIN + WIDTH) * 14,5]) # game bottom border

        # Draw_the_grid
        for row in range(13):
            for column in range(13):
                color = WHITE
                pygame.draw.rect(screen,
                                color,
                                [(MARGIN + WIDTH) * column + MARGIN+50,
                                (MARGIN + HEIGHT) * row + MARGIN+50,
                                WIDTH,
                                HEIGHT])


        ### move_logic
        if move == True:
            key = pygame.key.get_pressed()
            # if move == True:
            if num_text < num_of_order:
                # if key[pygame.K_LEFT]:
                if text_file[num_text] == 'turn left':
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
                if text_file[num_text] == 'move':
                    # print('m')
                    if x_collinde == False and y_collinde == True:
                        if right == True and x >= move_space +move_space:
                            x -= move_space+MARGIN
                        elif left == True and x <= lenght - move_space - move_space:
                            x += move_space+MARGIN
                    elif x_collinde == True and y_collinde == False:
                        if back == True and y >= move_space + move_space:
                            y -= move_space+MARGIN
                        elif front == True and y <=hight - move_space:
                            y += move_space+MARGIN
                    else:
                        pass
                    redrawGameWindow()
                    pygame.time.wait(100)
                if text_file[num_text] == 'end':
                    win = 1
                showtext("-",((MARGIN + WIDTH) * 14)+40,100+lst_command[num_text],WHITE)
                pygame.time.wait(500)
                num_text +=1
        if num_of_order == 0:
            showtext("PLEASED RUNYOLO",((MARGIN + WIDTH) * 14)+40,100+75,WHITE)
        else:
            for i in range(len(lst_command)):
                showtext(text_file[i],((MARGIN + WIDTH) * 14)+50,100+lst_command[i],WHITE)
    


        # Limit to 60 frames per second
        #call_funtion
        clock.tick(60)
        pygame.time.wait(100)
        redrawGameWindow()
        random_brain(brainX,brainY) # config
        if box == True:
            box_block(box_x,box_y)
        
        showtext("Command",((MARGIN + WIDTH) * 14)+50,50,WHITE)
        showtext("STAGE",(window_width-200),(window_height- 150),WHITE)
        showtext(str(stage),(window_width-100),(window_height- 150),WHITE)

        x_collinde,y_collinde = collide(x,y)

        if botton("START",window_width-200, window_height -100,WHITE,RED) == True:
            if text_file[0] == 'start':
                move = True
            else:
                 check_start == 0
        if botton("RESTART",window_width-200, window_height -50,WHITE,RED) == True: 
            Start_stage(num_stage)      
        lock_space()
        if win == 1:
            win_stage(x,y)
        if check_start == 1:
            showtext("TRY AGAIN",((MARGIN + WIDTH) * 14)+50,100,WHITE)  

        #### Stage ####
        if botton("STAGE 1",window_width+75 -window_width, window_height -200,WHITE,RED) == True: 
            Start_stage("map/stage1.json")
        if botton("STAGE 2",window_width+225 - window_width, window_height -200,WHITE,RED) == True: 
            Start_stage("map/stage2.json")
        if botton("STAGE 3 ",window_width+375 - window_width, window_height -200,WHITE,RED) == True: 
            Start_stage("map/stage3.json")

        pygame.display.flip()
        pygame.display.update()
    
    pygame.quit()
    cv2.destroyAllWindows()
Start_stage("map/stage1.json")


def open_cv():
    pygame.init()
    info = pygame.display.Info() # You have to call this before pygame.display.set_mode()
    screen_width,screen_height = info.current_w,info.current_h
    window_width,window_height = screen_width,screen_height

    color=False#True#False
    camera_index = 0
    camera=cv2.VideoCapture(camera_index)
    camera.set(3,640)
    camera.set(4,480)
    screen = pygame.display.set_mode((window_width,window_height), pygame.FULLSCREEN )

    def getCamFrame(color,camera):
        retval,frame=camera.read()
        frame = frame.swapaxes(0, 0)
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        frame=cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB)
        frame=numpy.rot90(frame)
        frame=pygame.surfarray.make_surface(frame) #I think the color error lies in this line?
        return frame

    def blitCamFrame(frame,screen):
        screen.blit(frame,(window_width/2,30))
        return screen


    running=True
    while running:
        screen.fill(255)
        for event in pygame.event.get(): #process events since last loop cycle
            if event.type == KEYDOWN:
                running=False
        pygame.draw.rect(screen, [255,255,255], [25,25,window_width-50,5]) #top border
        frame = getCamFrame(color, camera)
        screen = blitCamFrame(frame, screen)
        pygame.display.flip()
    pygame.quit()
    cv2.destroyAllWindows()
