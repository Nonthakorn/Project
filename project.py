import pygame
pygame.init()

win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("game")

x = 0
y = 0
width = 50
height = 50
vel = 50

run = True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    key = pygame.key.get_pressed()

    if key[pygame.K_LEFT] and x >= vel:
        x -= vel

    if key[pygame.K_RIGHT] and x <= 500 - width - vel:
        x += vel

    if key[pygame.K_UP] and y >= vel:
        y -= vel

    if key[pygame.K_DOWN] and y <= 500 - height - vel:
        y += vel

    
    win.fill((255, 255, 255))
    pygame.draw.rect(win, (0, 0, 0), (x, y, width, height))
    pygame.display.update()
pygame.quit()
