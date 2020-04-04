import pygame
import tkinter as tk
# get input
f = open("input.txt", "r")
file_contents = f.read()
count = 45
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()
sizewidth = 909
sizehight = 509
size = (909, 515)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Test")

walkRight = [pygame.image.load('R1.png')]
walkLeft = [pygame.image.load('L1.png')]
char = [pygame.image.load('standing.png')]
# done = False
# clock = pygame.time.Clock()
width = 50
height = 50
margin = 1
widthk = 50
heightk = 50
x = 0
y = 0
vel = 50
isJump = False
jumpCount = 10

left = False
right = False
walkCount = 0
boundary = 509

font = pygame.font.Font('freesansbold.ttf', 32)

# create a text suface object,
# on which text is drawn on it.
text = font.render('INPUT', True, BLACK)

# create a rectangular object for the
# text surface object
textRect = text.get_rect()

# set the center of the rectangular object.
textRect.center = (700, 35)

print (file_contents)

def redrawGameWindow():
    global walkCount

    if left:
        screen.blit(walkLeft[walkCount], (x - 10, y - 10))
        # walkCount += 1
    elif right:
        screen.blit(walkRight[walkCount], (x - 10, y - 10))
        # walkCount += 1
    else:
        screen.blit(char[walkCount], (x - 10, y - 10))
        # walkCount = 0
    # pygame.display.flip()
    # screen.fill(255,255,255)
    # pygame.draw.rect(screen, (0, 0, 0), (x, y, width+1, height+1))
    pygame.display.update()

run = True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        for column in range(0 + margin, boundary, width + margin):
            for row in range(0 + margin, boundary, height + margin):
                pygame.draw.rect(screen, WHITE, [column, row, width, height])
        pygame.draw.rect(screen, BLACK, [509, 0, 515, 515])  # set เส้นแบ่ง 2 หน้า
        pygame.draw.rect(screen, WHITE, [514, 1, 900, 515])  # สร้างหน้าฝั่งขวา
    screen.blit(text, textRect)
    for i in (f.read()):
        text1 = font.render(str(i), True, RED, GREEN)
        textRect1 = text1.get_rect()
        textRect1.center = (630, count)
        screen.blit(text1, textRect1)
        count += 45
        pygame.display.flip()
        pygame.display.update()
    key = pygame.key.get_pressed()

    if key[pygame.K_LEFT] and x >= vel:
        x -= vel + margin
        left = True
        right = False
    if key[pygame.K_RIGHT] and x <= 509 - width - vel:
        x += vel + margin
        left = False
        right = True
    if left == True:
        if key[pygame.K_UP] and y >= vel:
            y -= vel + margin
            left = True
            right = False
        if key[pygame.K_DOWN] and y <= 509 - height - vel:
            y += vel + margin
            left = True
            right = False
    else:
        if key[pygame.K_UP] and y >= vel:
            y -= vel + margin
            left = False
            right = True
        if key[pygame.K_DOWN] and y <= 509 - height - vel:
            y += vel + margin
            left = False
            right = True

    redrawGameWindow()
    # clock.tick(60)

    # screen.fill(0,0,0)
    # pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height))
    # pygame.display.update()
# Close the window and quit.
pygame.quit()
