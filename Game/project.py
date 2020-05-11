import pygame
import random
import math
from tkinter import filedialog
from tkinter import *


root = Tk()


#get input
f = open("input.txt", "r") # ใช้อ่านไฟล์
fileinput = open("input.txt", "r")
lstf = []
for i in f.read():
    lstf.append(i)
textin = fileinput.read()
count = 45
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
random.seed(3)
def building(num_of_building):
    random.seed(1)
    cbuilding = pygame.image.load('char/building.png')
    cbuilding = pygame.transform.scale(cbuilding,(50,50))

    building = []
    for _ in range(num_of_building):
        getxy = []
        getxy.append(cbuilding)
        for _ in range(2):
            getxy.append(random.randrange(71,350,71))

 
        building.append(getxy)
    return building



# buildings = building(2)
    

def redrawGameWindow():
    global walkCount
        
    if left:  
        screen.blit(walkLeft[walkCount], (x+15, y))
        #walkCount += 1                          
    elif right:
        screen.blit(walkRight[walkCount], (x+15, y))
        #walkCount += 1
    elif back:
        screen.blit(stback[walkCount], (x+15, y))
    elif front:
        screen.blit(char[walkCount], (x+15, y))
        #walkCount = 0
    #pygame.display.flip()
    #screen.fill(255,255,255)
    #pygame.draw.rect(screen, (0, 0, 0), (x, y, width+1, height+1))
    # pygame.display.update()
#building

random.seed(17)
#brain 
brainX = random.randrange(71,350,71)
brainY = random.randrange(71,350,71)
def random_brain(brainX,brainY):
    brain = pygame.image.load('char/brain.png')
    brain = pygame.transform.scale(brain,(70,70))
    screen.blit(brain, (brainX+1, brainY+3))
    pygame.display.update()

 # เมื่อเจอสิ่งกีดขวาง
def iscollision(x,y,buildingX,buildingY):
    distance =  math.sqrt(math.pow(x-buildingX,2) + math.pow(y-buildingY,2))
    if distance < 50 :
        return True
    else:
        return False

def firststage():
    x = 142
    y = 142
    brain = pygame.image.load('char/brain.png')
    brain = pygame.transform.scale(brain,(70,70))
    screen.blit(brain, (x, y))
    pygame.display.update()
    return x,y


pygame.init()
sizewidth = 825
sizehight = 425
size = (900, 430) # 900 คือความกว้าง 515 ความยาว
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Test")



walkRight = [pygame.image.load('char/right.png')]
walkLeft = [pygame.image.load('char/left.png')]
char = [pygame.image.load('char/front.png')]
stback = [pygame.image.load('char/back.png')]


width=70
height=70
margin=1
widthk = 50
heightk =50
x = 0
y = 0
vel = 70
isJump = False
jumpCount = 10

left = False
right = False
back = False
front = True
walkCount = 0
boundary = 425
font = pygame.font.Font('freesansbold.ttf', 22) 
bigfont = pygame.font.Font('freesansbold.ttf', 30) #กำหนดฟอนต์
  
text = font.render('INPUT', True, GREEN,RED)  #render text  
textRect = text.get_rect()   # นำ tect ไปใส่บน screen  
textRect.center = (650, 35)  # จัดตำแหน่งของ Text

textCrash = font.render('Crash', True, RED,WHITE)  #render text
textCrash_ = textCrash.get_rect()   # นำ tect ไปใส่บน screen
textCrash_.center = (650, 300)  # จัดตำแหน่งของ 

textPass = font.render('Pass', True, GREEN,WHITE)  #render text
textPass_ = textPass.get_rect()
textPass_.center = (650, 300)   # นำ tect ไปใส่บน screen

bottonleft = font.render('Start', True, GREEN,WHITE)  #render text
bottonleft_ = bottonleft.get_rect()   # นำ tect ไปใส่บน screen
bottonleft_.center = (650, 350)  # จัดตำแหน่งของ Text

bottonstart = font.render('Start', True, WHITE,GREEN)  #render text
bottonstart_ = bottonstart.get_rect()   # นำ tect ไปใส่บน screen
bottonstart_.center = (650, 350)  # จัดตำแหน่งของ Text

textmove = font.render('Move', True, BLACK,WHITE)  #render text
textmove_ = textmove.get_rect()
textmove_.center = (650, 70)   # นำ tect ไปใส่บน screen

textturnleft = font.render('Turnleft', True, BLACK,WHITE)  #render text
textturnleft_ = textturnleft.get_rect()
textturnleft_.center = (650, 70)   # นำ tect ไปใส่บน screen

textstageclear = bigfont.render('Stage 1 Clear ', True, BLACK,WHITE)  #render text
textstageclear_ = textstageclear.get_rect()
textstageclear_.center = (600, 210)   # นำ tect ไปใส่บน screen

textinput= font.render(textin ,True, BLACK,WHITE)  #render text
textinput_ = textinput.get_rect()
textinput_.center = (650, 100)   # นำ tect ไปใส่บน screen


text_file = lstf
num_of_order = len(text_file)
num_text = 0
status = 'start'
def table():
    for column in range(0+margin,boundary, width+margin):
        for row in range(0+margin, boundary, height+margin):
            pygame.draw.rect(screen, WHITE, [column,row,width,height])


def showcommand(forward,turntoleft):
    if forward == True:
        screen.blit(textmove, textmove_)
    if turntoleft == True:
        screen.blit(textturnleft, textturnleft_)

building_break = False
move = False

run = True
facedirection = 0
stage = 1
brainX, brainY = 142,213
stageclear =0
while run:
    if stage == 2:
        screen.fill((255,255,255))
        pygame.draw.rect(screen, WHITE, [0,0,825,425])
        stageclear = 1
    if stageclear ==1:
        screen.fill((255,255,255))
        screen.blit(textstageclear, textstageclear_)

    pygame.time.delay(100)
    table()
    if num_text == num_of_order:
        move = False
        num_text = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False



        pygame.draw.rect(screen, WHITE, [430,1,825,425]) # สร้างหน้าฝั่งขวา
    if stage != 2:
        screen.blit(text, textRect)
        screen.blit(textinput, textinput_)
        screen.blit(bottonleft, bottonleft_) # โชว์ สตาร์ท
    ######## MOUSE CLICK ###############
    
###set click ####

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # print(mouse)
        # print(x,y)
        # print('brain',brainX,brainY)
        if 670 > mouse[0] > 630 and 360 > mouse[1] > 340 :
            screen.blit(bottonstart, bottonstart_)
            if pygame.mouse.get_pressed() == (1, 0, 0):
                move = True
    pygame.display.update()
            
    
    if stage == 1:
        # firststage()
        redrawGameWindow()
        random_brain(brainX,brainY)

    if stage == 4:
        # firststage()
        redrawGameWindow()
        random_brain(brainX,brainY)
        if building_break == True:
        # pass
            building1 = building(15)
        for j in building1:
            screen.blit(j[0], (j[1]+6, j[2]+7))
            if x == j[1] and y == j[2]:
                screen.blit(textCrash, textCrash_)
                x = 0
                y = 0
                left = False
                right = False
                back = False
                front = True
                move = False

    if stage == 3:
        pygame.draw.rect(screen, WHITE, [0,0,825,425]) 
################Brain and Building Block######################          
    if x == brainX and y == brainY:
        pygame.time.wait(700)
        # screen.blit(textPass, textPass_)
        left = False
        right = False
        back = False
        front = True
        x= 0
        y=0
        brainX = random.randrange(71,350,71)
        brainY = random.randrange(71,350,71)
        random_brain(brainX,brainY)
        building_break = True
        stage += 1
    if building_break == True:
        # pass
        building1 = building(15)
        for j in building1:
            screen.blit(j[0], (j[1]+6, j[2]+7))
            if x == j[1] and y == j[2]:
                screen.blit(textCrash, textCrash_)
                x = 0
                y = 0
                left = False
                right = False
                back = False
                front = True
                move = False

    
    redrawGameWindow()
    # random_brain(brainX,brainY)
##################################################################
#################### MOVE LOGIC############################
    key = pygame.key.get_pressed()
    # if key[pygame.K_LEFT] and x >= vel:
    if move == True:
        pygame.draw.rect(screen, WHITE, [650,60,100,50])
        if text_file[num_text] == 'L':
            forward = False
            turntoleft =True
            # showcommand(forward,turntoleft)
            pygame.time.wait(500)
            
            # print('l')
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
        if text_file[num_text] == 'M':
            forward = True
            pygame.time.wait(500)
            # print('m')
            if right == True and x >= vel:
                x -= vel+margin
            elif left == True and x <= 425 - width - vel:
                x += vel+margin
            elif back == True and y >= vel:
                y -= vel+margin
            elif front == True and y <= 425 - height - vel:
                y += vel+margin
            table()
            redrawGameWindow()
        
        pygame.time.wait(700)
        redrawGameWindow()
        num_text+=1
            # pygame.time.delay(1000)
################## Move with key########################
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
        if right == True and x >= vel:
            x -= vel+margin
        elif left == True and x <= 425 - width - vel:
            x += vel+margin
        elif back == True and y >= vel:
            y -= vel+margin
        elif front == True and y <= 425 - height - vel:
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




