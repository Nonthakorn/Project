import pygame
import random
import math
from tkinter import filedialog
from tkinter import *


root = Tk()


#get input
f = open("input.txt", "r") # ใช้อ่านไฟล์
lstf = []
for i in f.read():
    lstf.append(i)
count = 45
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

def building(num_of_building):
    random.seed(1)
    cbuilding = pygame.image.load('char/building.png')
    cbuilding = pygame.transform.scale(cbuilding,(40,40))

    building = []
    for _ in range(num_of_building):
        getxy = []
        getxy.append(cbuilding)
        for j in range(2):
            getxy.append(random.randrange(51,458,51))
        building.append(getxy)
    return building



buildings = building(5)
    

def redrawGameWindow():
    global walkCount
        
    if left:  
        screen.blit(walkLeft[walkCount], (x+5, y))
        #walkCount += 1                          
    elif right:
        screen.blit(walkRight[walkCount], (x+5, y))
        #walkCount += 1
    elif back:
        screen.blit(stback[walkCount], (x+5, y))
    elif front:
        screen.blit(char[walkCount], (x+5, y))
        #walkCount = 0
    #pygame.display.flip()
    #screen.fill(255,255,255)
    #pygame.draw.rect(screen, (0, 0, 0), (x, y, width+1, height+1))
    # pygame.display.update()
#building

random.seed(2)
#brain 
brainX = random.randrange(51,458,51)
brainY = random.randrange(51,458,51)
def random_brain(brainX,brainY):
    brain = pygame.image.load('char/brain.png')
    brain = pygame.transform.scale(brain,(53,52))
    screen.blit(brain, (brainX-1, brainY))
    pygame.display.update()

 # เมื่อเจอสิ่งกีดขวาง
def iscollision(x,y,buildingX,buildingY):
    distance =  math.sqrt(math.pow(x-buildingX,2) + math.pow(y-buildingY,2))
    if distance < 50 :
        return True
    else:
        return False




pygame.init()
sizewidth = 909
sizehight = 509
size = (909, 515) # 900 คือความกว้าง 515 ความยาว
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Test")



walkRight = [pygame.image.load('char/right.png')]
walkLeft = [pygame.image.load('char/left.png')]
char = [pygame.image.load('char/front.png')]
stback = [pygame.image.load('char/back.png')]


width=50
height=50
margin=1
widthk = 50
heightk =50
x = 0
y = 0
vel = 50
isJump = False
jumpCount = 10

left = False
right = False
back = False
front = True
walkCount = 0
boundary = 509
font = pygame.font.Font('freesansbold.ttf', 22)  #กำหนดฟอนต์
  
text = font.render('INPUT', True, GREEN,RED)  #render text  
textRect = text.get_rect()   # นำ tect ไปใส่บน screen  
textRect.center = (700, 35)  # จัดตำแหน่งของ Text

textCrash = font.render('Crash', True, RED,WHITE)  #render text
textCrash_ = textCrash.get_rect()   # นำ tect ไปใส่บน screen
textCrash_.center = (700, 70)  # จัดตำแหน่งของ 

textPass = font.render('Pass', True, GREEN,WHITE)  #render text
textPass_ = textPass.get_rect()
textPass_.center = (700, 70)   # นำ tect ไปใส่บน screen

bottonleft = font.render('Start', True, GREEN,WHITE)  #render text
bottonleft_ = bottonleft.get_rect()   # นำ tect ไปใส่บน screen
bottonleft_.center = (700, 450)  # จัดตำแหน่งของ Text

bottonstart = font.render('Start', True, WHITE,GREEN)  #render text
bottonstart_ = bottonstart.get_rect()   # นำ tect ไปใส่บน screen
bottonstart_.center = (700, 450)  # จัดตำแหน่งของ Text







text_file = lstf
num_of_order = len(text_file)
num_text = 0
status = 'start'
def table():
    for column in range(0+margin,boundary, width+margin):
        for row in range(0+margin, boundary, height+margin):
            pygame.draw.rect(screen, WHITE, [column,row,width,height])

building_break = True
move = False

run = True
facedirection = 0
while run:
    pygame.time.delay(100)
    # screen.fill((255,255,255))
    table()
    if num_text == num_of_order:
        move = False
        num_text = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False



        pygame.draw.rect(screen, WHITE, [514,1,900,515]) # สร้างหน้าฝั่งขวา
    screen.blit(text, textRect)
    screen.blit(bottonleft, bottonleft_) # โชว์ สตาร์ท
######## MOUSE CLICK ###############
    
###set click ####
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # print(mouse)
    if 727 > mouse[0] > 667 and 456 > mouse[1] > 439 :
        screen.blit(bottonstart, bottonstart_)
        if pygame.mouse.get_pressed() == (1, 0, 0):
            move = True
    pygame.display.update()
            



################Brain and Building Block######################          
    if x == brainX and y == brainY:
        pygame.time.wait(700)
        screen.blit(textPass, textPass_)
        left = False
        right = False
        back = False
        front = True
        x= 0
        y=0
        brainX = random.randrange(51,458,51)
        brainY = random.randrange(51,458,51)
        random_brain(brainX,brainY)
        building_break = True
    if building_break == True:
        # pass
        building1 = building(15)
    building_break = False
    
    for j in building1:
        screen.blit(j[0], (j[1]+5, j[2]+6))
        if x == j[1] and y == j[2]:
            screen.blit(textCrash, textCrash_)
            x = 0
            y = 0
            left = False
            right = False
            back = False
            front = True
            move = False
    random_brain(brainX,brainY)
##################################################################
#################### MOVE LOGIC############################
    key = pygame.key.get_pressed()
    # if key[pygame.K_LEFT] and x >= vel:
    if move == True:
        if text_file[num_text] == 'l':
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
            table()
            redrawGameWindow()
        if text_file[num_text] == 'm':
            print('m')
            if left == True and x >= vel:
                x -= vel+margin
            elif right == True and x <= 509 - width - vel:
                x += vel+margin
            elif back == True and y >= vel:
                y -= vel+margin
            elif front == True and y <= 509 - height - vel:
                y += vel+margin
            table()
            redrawGameWindow()
        pygame.time.wait(700)
        redrawGameWindow()
        num_text+=1
            # pygame.time.delay(1000)
    if key[pygame.K_LEFT]:
    # if text_file[num_text] == 'l':
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
        table()
        redrawGameWindow()
    if key[pygame.K_SPACE]:
    # if text_file[num_text] == 'm':
        print('m')
        if left == True and x >= vel:
            x -= vel+margin
        elif right == True and x <= 509 - width - vel:
            x += vel+margin
        elif back == True and y >= vel:
            y -= vel+margin
        elif front == True and y <= 509 - height - vel:
            y += vel+margin
        table()
        redrawGameWindow()


#############################################################

    # redrawGameWindow()
    # pygame.display.update()
    #clock.tick(60)
    

    #pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height))
    #pygame.display.update()
# Close the window and quit.
pygame.quit()




