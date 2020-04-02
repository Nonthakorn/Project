import pygame
import tkinter as tk
from tkinter import ttk
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()


size = (509, 600)
screen = pygame.display.set_mode(size)
tkinput_1 = True
pygame.display.set_caption("Test")

walkRight = [pygame.image.load('Game\R1.png')]
walkLeft = [pygame.image.load('Game\L1.png')]
char = pygame.image.load('Game\standing.png')
#done = False
#clock = pygame.time.Clock()
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
walkCount = 0
def redrawGameWindow():
    global walkCount
        
    if left:  
        screen.blit(walkLeft[walkCount], (x-10,y-10))
        #walkCount += 1                          
    elif right:
        screen.blit(walkRight[walkCount], (x-10,y-10))
        #walkCount += 1
    else:
        screen.blit(walkRight[walkCount], (x-10, y-10))
        #walkCount = 0
    #pygame.display.flip()
    #screen.fill(255,255,255)
    #pygame.draw.rect(screen, (0, 0, 0), (x, y, width+1, height+1))

    pygame.display.update()
run = True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        for column in range(0+margin, 509, width+margin):
            for row in range(0+margin, 509, height+margin):
                pygame.draw.rect(screen, WHITE, [column,row,width,height])
            
    key = pygame.key.get_pressed()

    if key[pygame.K_LEFT] and x >= vel:
        x -= vel+margin
        left = True
        right = False
    if key[pygame.K_RIGHT] and x <= 509 - width - vel:
        x += vel+margin
        left = False
        right = True
    if left == True:
        if key[pygame.K_UP] and y >= vel:
            y -= vel+margin
            left = True
            right = False
        if key[pygame.K_DOWN] and y <= 509 - height - vel:
            y += vel+margin
            left = True
            right = False
    else:
        if key[pygame.K_UP] and y >= vel:
            y -= vel+margin
            left = False
            right = True
        if key[pygame.K_DOWN] and y <= 509 - height - vel:
            y += vel+margin
            left = False
            right = True
    redrawGameWindow()

    window = tk.Tk()
    window.title("Python Tkinter Text Box")
    window.minsize(600, 400)
    #clock.tick(60)
    def clickMe():
        label.configure(text='Hello ' + name.get())
        print(name.get())
        return name.get()

    label = ttk.Label(window, text="Enter Your Name")
    label.grid(column=0, row=0)
    name = tk.StringVar()
    nameEntered = ttk.Entry(window, width=15, textvariable=name)
    nameEntered.grid(column=0, row=1)
    button = ttk.Button(window, text="Click Me", command=clickMe)
    button.grid(column=0, row=2)
    window.mainloop()
    #mainloop()
    #screen.fill(0,0,0)
    #pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height))
    #pygame.display.update()
# Close the window and quit.
pygame.quit()
