
import pygame
from pygame.locals import *
import cv2
import numpy
def open_cv():
    color=False#True#False
    camera_index = 0
    camera=cv2.VideoCapture(camera_index)
    camera.set(4,800)
    camera.set(4,1000)


    #This shows an image the way it should be
    # cv2.namedWindow("w1",cv2.COLOR_BGR2GRAY)
    #retval,frame=camera.read()
    #if not color:
    #    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #cv2.flip(frame,1,frame)#mirror the image
    # cv2.imshow("w1",frame)

    #This shows an image weirdly...
    screen_width, screen_height = 1366, 720
    screen=pygame.display.set_mode((screen_width,screen_height))
    cam_screen=pygame.display.set_mode((1000,720))

    def getCamFrame(color,camera):
        retval,frame=camera.read()
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        frame=numpy.rot90(frame)
        frame=pygame.surfarray.make_surface(frame) #I think the color error lies in this line?
        return frame

    def blitCamFrame(frame,screen):
        screen.blit(frame,(50,100))
        return screen

    screen.fill(0) #set pygame screen to black
    #frame=getCamFrame(color,camera)
    #screen=blitCamFrame(frame,screen)
    #pygame.display.flip()

    running=True
    while running:
        screen.fill(0)
        for event in pygame.event.get(): #process events since last loop cycle
            if event.type == KEYDOWN:
                running=False

        frame = getCamFrame(color, camera)
        cam_screen = blitCamFrame(frame, cam_screen)
        pygame.display.flip()
    pygame.quit()
    cv2.destroyAllWindows()

open_cv()