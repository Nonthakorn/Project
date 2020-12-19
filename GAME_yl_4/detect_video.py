
import pygame

import time
import tensorflow as tf
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
from absl import app, flags, logging
from absl.flags import FLAGS
import core.utils as utils
from core.yolov4 import filter_boxes
from tensorflow.python.saved_model import tag_constants
from PIL import Image
import numpy
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
from pygame.locals import *
import cv2
import json
import runyolo




flags.DEFINE_string('framework', 'tf', '(tf, tflite, trt')
flags.DEFINE_string('weights', './checkpoints/yolov4-416',
                    'path to weights file')
flags.DEFINE_integer('size', 416, 'resize images to')
flags.DEFINE_boolean('tiny', False, 'yolo or yolo-tiny')
flags.DEFINE_string('model', 'yolov4', 'yolov3 or yolov4')
flags.DEFINE_string('video', '0', 'path to input video or set to 0 for webcam')
flags.DEFINE_string('output', None, 'path to output video')
flags.DEFINE_string('output_format', 'XVID', 'codec used in VideoWriter when saving video to file')
flags.DEFINE_float('iou', 0.45, 'iou threshold')
flags.DEFINE_float('score', 0.25, 'score threshold')
flags.DEFINE_boolean('dont_show', False, 'dont show video output')

pygame.init()
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
window_width, window_height = screen_width, screen_height
screen = pygame.display.set_mode(((window_width, window_height)), pygame.FULLSCREEN)
bg = pygame.image.load("char/background.jpg").convert_alpha()
bg.set_alpha(254)
start = True
num = 0
while start:
    screen.blit(bg,(0,0))
    start = False
def main(_argv):
    with open('stage/stage1.json') as json_file:
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
            item = i['item']
            item_x = i['item_x']
            item_y = i["item_y"]
    ### Funtion
    def read_input():
        f = open("input.txt", "r")  # ใช้อ่านไฟล์
        fileinput = open("input.txt", "r")
        lstf = []
        for i in f.readlines(-3):
            lstf.append(i.rstrip())
        text_file = lstf
        num_of_order = len(text_file)
        return text_file, num_of_order

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
            showtext('NOT CLEAR', lenght / 3, hight / 2, BLACK)

    def not_win_stage(x, y):
        brain_x_pos, brain_y_pos = create_grid(brainX, brainY)
        if x == brain_x_pos and y == brain_y_pos:
            showtext('NOT CLEAR', lenght / 3, hight / 2, BLACK)
        else:
            showtext('CLEAR', lenght / 3, hight / 2, BLACK)

    def pick_item(x, y):
        item_xX, item_yY = create_grid(item_x, item_y)
        if x == item_xX and y == item_yY:
            return True
        else:
            return False

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
    def create_item(item_x,item_y):
        item = pygame.image.load('char/apple.png')
        item = pygame.transform.scale(item, (char_scale, char_scale))
        screen.blit(item, (create_grid(item_x, item_y)))
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
        pygame.draw.rect(screen, WHITE, [textx - 5, texty - 5, text_width + 10, 2])  # top border
        pygame.draw.rect(screen, WHITE, [textx - 5, texty + text_height, text_width + 10, 2])  # bottom border
        pygame.draw.rect(screen, WHITE, [textx - 5, texty - 5, 2, text_height + 5])  # left border
        pygame.draw.rect(screen, WHITE, [textx + text_width + 5, texty - 5, 2, text_height + 5])  # right border
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

    #### YOLO running
    config = ConfigProto()
    config.gpu_options.allow_growth = True
    # session = InteractiveSession(config=config)
    # STRIDES, ANCHORS, NUM_CLASS, XYSCALE = utils.load_config(FLAGS)
    input_size = FLAGS.size
    video_path = FLAGS.video

    if FLAGS.framework == 'tflite':
        interpreter = tf.lite.Interpreter(model_path=FLAGS.weights)
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        # print(input_details)
        # print(output_details)
    else:
        saved_model_loaded = tf.saved_model.load(FLAGS.weights, tags=[tag_constants.SERVING])
        infer = saved_model_loaded.signatures['serving_default']

    # begin video capture
    try:
        vid = cv2.VideoCapture(int(video_path))
    except:
        vid = cv2.VideoCapture(video_path)

    # out = None

    # if FLAGS.output:
    #     # by default VideoCapture returns float instead of int
    #     width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    #     height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #     fps = int(vid.get(cv2.CAP_PROP_FPS))
    #     codec = cv2.VideoWriter_fourcc(*FLAGS.output_format)
    #     # out = cv2.VideoWriter(FLAGS.output, codec, fps, (width, height))

        ##### PYGAME ###

    # screen = pygame.display.set_mode(((1360, 720)))




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

    # ############# set_object_char
    char_front = pygame.transform.scale(pygame.image.load('char/front.png'), (char_scale, char_scale))
    char_turnRight = pygame.transform.scale(pygame.image.load('char/right.png'), (char_scale, char_scale))
    char_turnLeft = pygame.transform.scale(pygame.image.load('char/left.png'), (char_scale, char_scale))
    char_turnback = pygame.transform.scale(pygame.image.load('char/back.png'), (char_scale, char_scale))
    char_lock = pygame.transform.scale(pygame.image.load('char/lock.png'), (char_scale - 5, char_scale - 5))

    img_command = "char/command2.jpg"
    img_command = pygame.image.load(img_command).convert()
    img_command = pygame.transform.scale(img_command, (round(window_width * 0.5), round(window_height * 0.7)))
    img_command_rect = img_command.get_rect(center=(600, 350))



    left = False
    right = False
    back = False
    front = True

    #restart fn
    def restart():
        with open('stage/stage1.json') as json_file:
            data = json.load(json_file)
            for i in data['grid']:
                x = i['char_x']
                y = i['char_y']
        left = False
        right = False
        back = False
        front = True

        # Set funtion and and variable
        check = 0
        facedirection = 0
        win = 0
        check_start = 0
        command_show = 0
        text_file, num_of_order = read_input()
        x, y = create_grid(x, y)
        num_text = 0
        move = False
        re_game = False
        return left,right,back,front,check,facedirection,win,check_start,command_show,text_file, num_of_order,x,y,num_text,move,re_game

    # getstage_fn
    def get_stage(stage_read = 'stage/stage1.json'):
        with open(stage_read) as json_file:
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
                item = i['item']
                item_x = i['item_x']
                item_y = i["item_y"]
                win = 0
            change_stage = False
            x, y = create_grid(x, y)
        return stage,num_row,num_col, x,y,brainX,brainY, box ,box_x,box_y,item,item_x,item_y,change_stage,win
    # Set funtion and and variable
    stagess = 1
    check = 0
    facedirection = 0
    win = 0
    check_start = 0
    command_show = 0
    text_file, num_of_order = read_input()
    x, y = create_grid(x, y)
    num_text = 0
    move = False
    done = True
    re_game = False
    change_stage =False
    pickking = True

    # runn while
    while done:
        if change_stage:
            stage,num_row,num_col, x,y,brainX,brainY, box ,box_x,box_y,item,item_x,item_y,change_stage,win = get_stage(stage_read)
            left, right, back, front, check, facedirection, win, check_start, command_show, text_file, num_of_order, x, y, num_text, move, re_game = restart()
        if re_game:
            left, right, back, front, check, facedirection, win, check_start, command_show, text_file, num_of_order, x, y, num_text, move, re_game = restart()
        # set varibale inwhile
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = False  # Flag that we are done so we exit this loop
                exit()
            if event.type == pygame.KEYDOWN:  # If user clicked close
                if event.key == pygame.K_q:
                    done = False  # Flag that we are done so we exit this loop
                    exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                command_show = 3
        # Set screen
        screen.blit(bg, (0, 0))
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



        ## SET move

        if box == True:
            box_x_lst, box_y_lst = box_block(box_x, box_y)
        ### move_logic
        if move == True:
            key = pygame.key.get_pressed()
            # if move == True:
            if num_text < num_of_order:
                if text_file[num_text] == 'pick':
                    if pick_item(x,y):
                        pickking = False
                        print('pick')
                        char_front = pygame.transform.scale(pygame.image.load('char/frontpick.png'),
                                                            (char_scale, char_scale))
                        char_turnRight = pygame.transform.scale(pygame.image.load('char/rightpick.png'),
                                                                (char_scale, char_scale))
                        char_turnLeft = pygame.transform.scale(pygame.image.load('char/leftpick.png'),
                                                               (char_scale, char_scale))
                        char_turnback = pygame.transform.scale(pygame.image.load('char/backpick.png'),
                                                               (char_scale, char_scale))

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

        ## SET WEBCAM and DETECT
        return_value, frame = vid.read()
        if return_value:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, -1)
            cap_frame = frame
            image = Image.fromarray(frame)
        else:
            print('Video has ended or failed, try a different video format!')
            break

        frame_size = frame.shape[:2]
        image_data = cv2.resize(frame, (input_size, input_size))
        image_data = image_data / 255.
        image_data = image_data[numpy.newaxis, ...].astype(numpy.float32)
        start_time = time.time()

        if FLAGS.framework == 'tflite':
            interpreter.set_tensor(input_details[0]['index'], image_data)
            interpreter.invoke()
            pred = [interpreter.get_tensor(output_details[i]['index']) for i in range(len(output_details))]
            if FLAGS.model == 'yolov3' and FLAGS.tiny == True:
                boxes, pred_conf = filter_boxes(pred[1], pred[0], score_threshold=0.25,
                                                input_shape=tf.constant([input_size, input_size]))
            else:
                boxes, pred_conf = filter_boxes(pred[0], pred[1], score_threshold=0.25,
                                                input_shape=tf.constant([input_size, input_size]))
        else:
            batch_data = tf.constant(image_data)
            pred_bbox = infer(batch_data)
            for key, value in pred_bbox.items():
                boxes = value[:, :, 0:4]
                pred_conf = value[:, :, 4:]

        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
            boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
            scores=tf.reshape(
                pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
            max_output_size_per_class=50,
            max_total_size=50,
            iou_threshold=FLAGS.iou,
            score_threshold=FLAGS.score
        )
        if check != 1:
            pred_bbox = [boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy()]
            image = utils.draw_bbox(frame, pred_bbox)
            # fps = 1.0 / (time.time() - start_time)
            # print("FPS: %.2f" % fps)
            result = numpy.asarray(image)
            # cv2.namedWindow("result", cv2.WINDOW_AUTOSIZE)
            result = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        else:
            if check == 1:
                cap_frame = cv2.cvtColor(cap_frame, cv2.COLOR_RGB2BGR)
                pygame.time.wait(200)
                cv2.imwrite("test_image/image50.JPG", cap_frame)
                runyolo.yolo()
                text_file, num_of_order = read_input()
                if num_of_order != 0:
                    num_img = open("num_img.txt", "r").read()
                    tmp_num_img = int(num_img)
                    cv2.imwrite("train_image/image%s.JPG" % str(tmp_num_img), frame)
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

        if cv2.waitKey(1) & 0xFF == ord('q'): break
        frame = frame.swapaxes(0, 0)
        frame = numpy.fliplr(frame)
        frame = numpy.rot90(frame)

        # frame = np.fliplr(frame)
        #OPEN camera
        show_frame = pygame.surfarray.make_surface(frame)
        screen.blit(show_frame, (window_width * 0.52, 30))


        # Call fun botton
        # sett Start bot
        if check == 0:
            showtext("PLEASED PRESS START", ((MARGIN + WIDTH) * 14) + 40, window_height - 200, WHITE)
        try:
            if botton("START", window_width - 500, window_height - 400, WHITE, RED) == True:
                check = 1

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

        if item and pickking:
            create_item(item_x, item_y)
        redrawGameWindow()
        random_brain(brainX, brainY)


        lock_space()
        showtext("Command", ((MARGIN + WIDTH) * 14) + 50, 50, PINK)
        showtext("STAGE", (window_width + (add_space * 5) - window_width), (window_height - 300), WHITE)
        showtext(str(stagess), (window_width + (add_space * 5)-window_width +150), (window_height - 300), WHITE)
        get_click = botton("SHOW COMMAND", window_width - 500, window_height - 300, WHITE, RED)
        if get_click:
            command_show = 1
            get_click = False

        if botton("RESTART", window_width - 500, window_height - 350, WHITE, RED) == True:
            re_game = True
        if win == 1:
            if item and pickking:
                not_win_stage(x, y)
            else:
                win_stage(x, y)
            for i in range(len(lst_command)):
                showtext(text_file[i], ((MARGIN + WIDTH) * 14) + 50, 100 + lst_command[i], WHITE)
        if command_show == 1:
            image_rect = img_command_rect.move(150, 70)
            screen.blit(img_command, image_rect)
        ### botton
        #### Stage ####
        if botton("STAGE 1", window_width + (add_space) - window_width, window_height - 200, WHITE, RED) == True:
            stage_read = "stage/stage1.json"
            stagess = '1'
            change_stage = True
        if botton("STAGE 2", window_width + (add_space * 5) - window_width, window_height - 200, WHITE, RED) == True:
            stage_read = "stage/stage2.json"
            stagess = '2'
            change_stage = True
        if botton("STAGE 3 ", window_width + (add_space * 9) - window_width, window_height - 200, WHITE, RED) == True:
            stage_read = "stage/stage3.json"
            stagess = '3'
            change_stage = True

        pygame.display.flip()
        pygame.display.update()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
