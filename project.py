import pygame


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()

size = (509, 509)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")


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

    if key[pygame.K_RIGHT] and x <= 509 - width - vel:
        x += vel+margin

    if key[pygame.K_UP] and y >= vel:
        y -= vel+margin

    if key[pygame.K_DOWN] and y <= 509 - height - vel:
        y += vel+margin

    pygame.display.flip()
    #screen.fill(255,255,255)
    pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height))
    pygame.display.update()
    
    # --- Limit to 60 frames per second
    #clock.tick(60)
    
    #screen.fill(0,0,0)
    #pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height))
    #pygame.display.update()
# Close the window and quit.
pygame.quit()
