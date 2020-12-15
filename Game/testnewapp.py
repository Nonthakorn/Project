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

# ctypes.windll.user32.SetProcessDPIAware()
# import pygame
# import tensorflow as tf
# import sys
# import cv2
# import numpy

# from yolo_v3 import Yolo_v3
# from utils import load_images, load_class_names, draw_boxes, draw_frame

# tf.compat.v1.disable_eager_execution()

# _MODEL_SIZE = (416, 416)
# _CLASS_NAMES_FILE = './data/labels/obj.names'
# _MAX_OUTPUT_SIZE = 20

show_comm = False


def Start_stage(num_stage):
    # Initialize pygame ##setscreen
    pygame.init()
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h
    window_width, window_height = screen_width, screen_height
    screen = pygame.display.set_mode(((window_width, window_height)), pygame.FULLSCREEN)
    ####### read_json file อ่าน json #####
    with open(num_stage) as json_file:
        data = json.load(json_file)
        for i in data['grid']:
            stage = i['stage']
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
        f = open("input.txt", "r")  # ใช้อ่านไฟล์
        fileinput = open("input.txt", "r")
        lstf = []
        for i in f.readlines(-3):
            lstf.append(i.rstrip())
        text_file = lstf
        num_of_order = len(text_file)
        return text_file, num_of_order

    num_text = 0
    move = False

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    PINK = (242, 215, 213)
    # This sets the WIDTH and HEIGHT of each grid location  ### set_W_H
    WIDTH = 50
    HEIGHT = 50
    char_scale = 50
    move_space = 50
    bigfont = pygame.font.Font('freesansbold.ttf', 35)
    # This sets the margin between each cell
    MARGIN = 1
    add_space = 50
    if screen_width <= 1900:
        WIDTH = round(WIDTH * 0.711)
        HEIGHT = round(HEIGHT * 0.711)
        char_scale = round(char_scale * 0.711)
        move_space = round(move_space * 0.711)
        add_space = round(add_space * 0.711)
        bigfont = pygame.font.Font('freesansbold.ttf', round(35 * 0.711))
    # elif screen_width >= 2000:
    #     WIDTH = round(WIDTH * 3840/1920)
    #     HEIGHT = round(HEIGHT *3840/1920)
    #     char_scale = round(char_scale *3840/1920)
    #     move_space = round(move_space*3840/1920)
    #     bigfont = pygame.font.Font('freesansbold.ttf', round(35*3840/1920))
    # ขอบสุดของด่านนั้นๆ
    lenght = (WIDTH * num_col) + num_col + (WIDTH * 3)
    hight = (HEIGHT * num_row) + num_row + (HEIGHT * 2)

    # Set title of screen
    pygame.display.set_caption("Robot Simulation")

    ### สร้างตำแหน่งที่ตั้งของตัว จะprint error ถ้าต่ำแหน่งเกินจำนวนของ col และ row Create_def
    def create_grid(x, y):
        if (x * move_space) + x + add_space >= (lenght) or (y * move_space) + y + add_space >= (hight):
            return print('Error pos ')
        else:
            return (x * move_space) + x + add_space, (y * move_space) + y + add_space

    ################ สร้างตัวบล็อคไม่ให้เดิน จะปลดล็อกตามด่านที่ config
    def create_block(x, y):
        return (x * move_space) + x + add_space, (y * move_space) + y + add_space

    def lock_space():
        for k in range(13):
            for m in range(13):
                if k > num_col or m > num_row:
                    i, j = create_block(k, m)
                    screen.blit(char_lock, (i + 2, j + 3))

    def win_stage(x, y):
        brain_x_pos, brain_y_pos = create_grid(brainX, brainY)
        if x == brain_x_pos and y == brain_y_pos:
            showtext('CLEAR', lenght / 3, hight / 2, BLACK)
        else:
            showtext('Not CLEAR', lenght / 3, hight / 2, BLACK)

    colline_lst = []

    def find_colli(x, y, box_x, box_y):
        colline_json = {'F_col': [0, (add_space + 1)], 'B_col': [0, -(add_space + 1)], 'L_col': [-(add_space + 1), 0],
                        'R_col': [(add_space + 1), 0]}
        kst = []
        colline_lst = []
        for i in range(len(box_x)):
            kst.append([box_x[i] - x, box_y[i] - y])
        for h in kst:
            for j, k in colline_json.items():
                if h == k:
                    colline_lst.append(j)
                else:
                    pass

        return colline_lst

    def collide(x, y):
        x_collinde = True
        y_collinde = True
        building_x_pos, building_y_pos = create_grid(box_x, box_y)
        if x < abs(building_x_pos - move_space) and y < abs(building_y_pos - move_space):
            x_collinde = False
            y_collinde = False
        elif x < abs(building_x_pos - move_space):
            x_collinde = True
            y_collinde = False
        elif y < abs(building_y_pos - move_space):
            x_collinde = False
            y_collinde = True
        else:
            x_collinde = True
            y_collinde = True
        return x_collinde, y_collinde, building_x_pos, building_y_pos

    x, y = create_grid(x, y)  # config
    ############# set_object_char
    char_front = pygame.transform.scale(pygame.image.load('char/front.png'), (char_scale, char_scale))
    char_turnRight = pygame.transform.scale(pygame.image.load('char/right.png'), (char_scale, char_scale))
    char_turnLeft = pygame.transform.scale(pygame.image.load('char/left.png'), (char_scale, char_scale))
    char_turnback = pygame.transform.scale(pygame.image.load('char/back.png'), (char_scale, char_scale))
    char_lock = pygame.transform.scale(pygame.image.load('char/lock.png'), (char_scale - 5, char_scale - 5))

    image_file = "char/command2.jpg"
    image = pygame.image.load(image_file).convert()
    image = pygame.transform.scale(image, (round(window_width * 0.5), round(window_height * 0.7)))
    start_rect = image.get_rect(center=(600,350))
    image_rect = start_rect

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

    def random_brain(brainX, brainY):
        brain = pygame.image.load('char/brain.png')
        brain = pygame.transform.scale(brain, (char_scale, char_scale))
        screen.blit(brain, (create_grid(brainX, brainY)))
        # print('x,y = ', create_grid(brainX,brainY))

    def box_block(building_X, building_Y):
        box_x_lst = []
        box_y_lst = []
        for i in range(len(building_X)):
            building = pygame.image.load('char/building.png')
            building = pygame.transform.scale(building, (char_scale, char_scale))
            box_x, box_y = create_grid(building_X[i], building_Y[i])
            screen.blit(building, (create_grid(building_X[i], building_Y[i])))
            box_x_lst.append(box_x)
            box_y_lst.append(box_y)
        return box_x_lst, box_y_lst

    ### text_and_botton
    def botton(text, textx, texty, color, hover_col):  # str input

        click = pygame.mouse.get_pressed()
        my_text = bigfont.render(text, True, color)
        my_text_hover = bigfont.render(text, True, hover_col)
        text_width = my_text.get_width()
        text_height = my_text.get_height()
        screen.blit(my_text, (round(textx), round(texty)))
        if textx + text_width > mouse[0] > textx and texty + text_height > mouse[1] > texty:
            screen.blit(my_text_hover, (textx, texty))
            if pygame.mouse.get_pressed() == (1, 0, 0):
                return True

    def show_command(text, textx, texty, color, hover_col):  # str input
        bigfont = pygame.font.Font('freesansbold.ttf', 35)
        click = pygame.mouse.get_pressed()
        my_text = bigfont.render(text, True, color)
        my_text_hover = bigfont.render(text, True, hover_col)
        text_width = my_text.get_width()
        text_height = my_text.get_height()
        screen.blit(my_text, (round(textx), round(texty)))
        if textx + text_width > mouse[0] > textx and texty + text_height > mouse[1] > texty:
            screen.blit(my_text_hover, (textx, texty))
            if pygame.mouse.get_pressed() == (1, 0, 0):
                get_click = True
                return get_click

    def showtext(text, textx, texty, color):
        my_text = bigfont.render(text, True, color)
        text_width = my_text.get_width()
        text_height = my_text.get_height()
        screen.blit(my_text, (round(textx), round(texty)))
        return text_height

    # text_stageClear = bigfont.render('CLEAR', True, BLACK)  #render text
    # text_stageClearRect = text_stageClear.get_rect().center = (((lenght-50)/2.5), hight/2.3)
    # Loop until the user clicks the close button.

    scence = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    ######################## OPENCV #####################################
    color = False  # True#False
    camera_index = 0
    camera = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    camera.set(3, 600)
    camera.set(4, 600)
    if scence == True:
        screen = pygame.display.set_mode(((window_width, window_height)), pygame.FULLSCREEN)  ####

    def getCamFrame(camera):
        retval, frame = camera.read()
        frame = frame.swapaxes(0, 0)

        # frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        # frame=cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB)

        frame = numpy.fliplr(frame)
        frame = numpy.rot90(frame)
        frame = numpy.rot90(frame)
        frame = numpy.fliplr(frame)

        realframe = frame
        frame = numpy.fliplr(frame)
        frame = numpy.rot90(frame)

        # frame = numpy.fliplr(frame)
        # frame = numpy.rot90(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = pygame.surfarray.make_surface(frame)
        return frame, realframe

    def blitCamFrame(frame, screen):
        screen.blit(frame, (round(window_width * 0.52), 30))
        return screen

    check = 0
    facedirection = 0

    win = 0
    check_start = 0
    text_file, num_of_order = read_input()
    blank_text = [""]
    command_show = 0
    processing_time = 0
    # lst_command = []
    # for j in range(num_of_order):
    #     lst_command.append(35*j)
    # -------- Main_Program_Loop -----------
    pygame.display.update()
    done = False
    while not done:
        mouse = pygame.mouse.get_pos()
        # x_collinde, y_collinde,building_x_pos,building_y_pos = collide(x, y)

        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
                exit()
            if event.type == pygame.KEYDOWN:  # If user clicked close
                if event.key == pygame.K_q:
                    done = True  # Flag that we are done so we exit this loop
                    exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                command_show = 3
        # Set the screen background
        screen.fill(BLACK)

        ############# แสดงภาพบนจอ
        frame, realframe = getCamFrame(camera)
        screen = blitCamFrame(frame, screen)
        ## OPENCV2

        # set_border
        pygame.draw.rect(screen, WHITE, [25, 25, window_width - 50, 5])  # top border
        pygame.draw.rect(screen, WHITE, [25, window_height - 25, window_width - 50, 5])  # bottom border
        pygame.draw.rect(screen, WHITE, [25, 25, 5, window_height - 50])  # left border
        pygame.draw.rect(screen, WHITE, [window_width - 30, 25, 5, window_height - 50])  # right border
        pygame.draw.rect(screen, WHITE, [((MARGIN + WIDTH) * 14) + 25, 25, 5, window_height - 50])  # game border
        pygame.draw.rect(screen, WHITE,
                         [25, ((MARGIN + WIDTH) * 14) + 25, (MARGIN + WIDTH) * 14, 5])  # game bottom border

        # Draw_the_grid
        for row in range(13):
            for column in range(13):
                color = WHITE
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN + add_space,
                                  (MARGIN + HEIGHT) * row + MARGIN + add_space,
                                  WIDTH,
                                  HEIGHT])
        if check == 0:
            showtext("PLEASED PRESS START", ((MARGIN + WIDTH) * 14) + 40, window_height - 200, WHITE)
        try:
            if botton("START", window_width - 200, window_height - 150, WHITE, RED) == True:
                check = 1

            if check == 1:
                cv2.imwrite("test_image/image50.JPG", realframe)
                runyolo.yolo()
                text_file, num_of_order = read_input()
                if num_of_order != 0:
                    num_img = open("num_img.txt", "r").read()
                    tmp_num_img = int(num_img)
                    cv2.imwrite("train_image/image%s.JPG" % str(tmp_num_img), realframe)
                    tmp_num_img = int(num_img) + 1
                    num_img = open("num_img.txt", "w")
                    num_img.write(str(tmp_num_img))
                    num_img.close()
                    lst_command = []
                    for j in range(num_of_order):
                        lst_command.append(35 * j)
                    for i in range(len(lst_command)):
                        showtext(text_file[i], ((MARGIN + WIDTH) * 14) + 50, 100 + lst_command[i], WHITE)
                    show_comm = True


                else:
                    check_start = 1
                check = 2

            if check == 2:
                # showtext("Processing",((MARGIN + WIDTH) * 14)+50,900,WHITE)
                pygame.display.flip()
                check = 3
                processing_time = 2
            if check == 3:
                if len(text_file) >= 1:
                    if text_file[0] == 'start':
                        move = True
        finally:
            pass
        if box == True:
            box_x_lst, box_y_lst = box_block(box_x, box_y)
        ### move_logic
        if move == True:
            key = pygame.key.get_pressed()
            # if move == True:
            if num_text < num_of_order:
                # x_collinde, y_collinde = collide(x, y)
                # if key[pygame.K_LEFT]:
                if text_file[num_text] == 'turn left':
                    facedirection += 1
                    if facedirection > 3:
                        facedirection = 0
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
                    if box == True:
                        colline_lst = find_colli(x, y, box_x_lst, box_y_lst)
                        if len(colline_lst) == 2:
                            if colline_lst[0] == "F_col" and colline_lst[1] == "B_col":
                                if right == True and x >= move_space + move_space:
                                    x -= move_space + MARGIN
                                elif left == True and x <= lenght - move_space - move_space:
                                    x += move_space + MARGIN
                            elif colline_lst[0] == "L_col" and colline_lst[1] == "R_col":
                                if back == True and y >= move_space + move_space:
                                    y -= move_space + MARGIN
                                elif front == True and y <= hight - move_space:
                                    y += move_space + MARGIN
                        elif len(colline_lst) == 1:
                            if colline_lst[0] == "F_col":
                                if right == True and x >= move_space + move_space:
                                    x -= move_space + MARGIN
                                elif left == True and x <= lenght - move_space - move_space:
                                    x += move_space + MARGIN
                                elif back == True and y >= move_space + move_space:
                                    y -= move_space + MARGIN
                            elif colline_lst[0] == "B_col":
                                if right == True and x >= move_space + move_space:
                                    x -= move_space + MARGIN
                                elif left == True and x <= lenght - move_space - move_space:
                                    x += move_space + MARGIN
                                elif front == True and y <= hight - move_space:
                                    y += move_space + MARGIN
                            elif colline_lst[0] == "L_col":
                                if left == True and x <= lenght - move_space - move_space:
                                    x += move_space + MARGIN
                                elif back == True and y >= move_space + move_space:
                                    y -= move_space + MARGIN
                                elif front == True and y <= hight - move_space:
                                    y += move_space + MARGIN
                            elif colline_lst[0] == "R_col":
                                if right == True and x >= move_space + move_space:
                                    x -= move_space + MARGIN
                                elif back == True and y >= move_space + move_space:
                                    y -= move_space + MARGIN
                                elif front == True and y <= hight - move_space:
                                    y += move_space + MARGIN
                        else:
                            if right == True and x >= move_space + move_space:
                                x -= move_space + MARGIN
                            elif left == True and x <= lenght - move_space - move_space:
                                x += move_space + MARGIN
                            elif back == True and y >= move_space + move_space:
                                y -= move_space + MARGIN
                            elif front == True and y <= hight - move_space:
                                y += move_space + MARGIN
                    else:
                        if right == True and x >= move_space + move_space:
                            x -= move_space + MARGIN
                        elif left == True and x <= lenght - move_space - move_space:
                            x += move_space + MARGIN
                        elif back == True and y >= move_space + move_space:
                            y -= move_space + MARGIN
                        elif front == True and y <= hight - move_space:
                            y += move_space + MARGIN
                    redrawGameWindow()
                    pygame.time.wait(100)
                if text_file[num_text] == 'end':
                    win = 1
                showtext("-", ((MARGIN + WIDTH) * 14) + 40, 100 + lst_command[num_text], WHITE)
                for i in range(len(lst_command)):
                    showtext(text_file[i], ((MARGIN + WIDTH) * 14) + 50, 100 + lst_command[i], WHITE)
                pygame.time.wait(700)

                num_text += 1

        # Limit to 60 frames per second
        # call_funtion
        # clock.tick(60)
        redrawGameWindow()
        random_brain(brainX, brainY)  # config

        showtext("Command", ((MARGIN + WIDTH) * 14) + 50, 50, PINK)
        showtext("STAGE", (window_width - 200), (window_height - 200), WHITE)
        showtext(str(stage), (window_width - 110), (window_height - 200), WHITE)

        get_click = botton("SHOW COMMAND", window_width - 500, window_height - 150, WHITE, RED)
        if get_click:
            command_show = 1
            get_click = False

        if botton("RESTART", window_width - 200, window_height - 100, WHITE, RED) == True:
            # t_f = open("input.txt", "w")
            # t_f.write("")
            # t_f.close()
            Start_stage(num_stage)
        lock_space()
        if win == 1:
            win_stage(x, y)
            for i in range(len(lst_command)):
                showtext(text_file[i], ((MARGIN + WIDTH) * 14) + 50, 100 + lst_command[i], WHITE)

        if check_start == 1:
            showtext("TRY AGAIN", ((MARGIN + WIDTH) * 14) + 50, 100, WHITE)

            #### Stage ####
        if botton("STAGE 1", window_width + (add_space) - window_width, window_height - 200, WHITE, RED) == True:
            Start_stage("map/stage1.json")
        elif botton("STAGE 2", window_width + (add_space * 5) - window_width, window_height - 200, WHITE, RED) == True:
            Start_stage("map/stage2.json")
        elif botton("STAGE 3 ", window_width + (add_space * 9) - window_width, window_height - 200, WHITE, RED) == True:
            Start_stage("map/stage3.json")

        if command_show == 1:
            image_rect = start_rect.move(150, 70)
            screen.blit(image, image_rect)
        pygame.display.flip()
        pygame.display.update()

    pygame.quit()
    cv2.destroyAllWindows()


try:
    Start_stage("map/stage1.json")
finally:
    pass