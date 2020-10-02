from pygame.locals import KEYDOWN, K_ESCAPE, K_q
import pygame
import cv2
import sys
import numpy as np
import cv2

cap = cv2.VideoCapture(0)
pygame.init()
pygame.display.set_caption("OpenCV camera stream on Pygame")
screen = pygame.display.set_mode([1280, 720])
while(True):
    # Capture frame-by-frame
    screen.fill([0, 0, 0])
    ret, frame = cap.read()
    frame = frame.swapaxes(0, 0)
    # ret = cap.set(3,120)
    # ret = cap.set(4,120)
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    pygame.display.update()
    # Display the resulting frame
    # pygame.surfarray.blit_array(screen, frame)
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE or event.key == K_q:
                        sys.exit(0)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
print('test',frame)


# import pygame
# import pygame.camera
# from pygame.locals import *

# pygame.init()
# pygame.camera.init()
# cam = pygame.camera.Camera("/dev/video0",(640,480))
# cam.start()
# image = cam.get_image()