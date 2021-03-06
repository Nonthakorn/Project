"""Yolo v3 detection script.

Saves the detections in the `detection` folder.

Usage:
    python detect.py <images/video> <iou threshold> <confidence threshold> <filenames>

Example:
    python detect.py images 0.5 0.5 data/images/dog.jpg data/images/office.jpg
    python detect.py video 0.5 0.5 data/video/shinjuku.mp4

Note that only one video can be processed at one run.
"""

import pygame
import tensorflow as tf
import sys
import cv2
import numpy

from yolo_v3 import Yolo_v3
from utils import load_images, load_class_names, draw_boxes, draw_frame

tf.compat.v1.disable_eager_execution()

_MODEL_SIZE = (416, 416)
_CLASS_NAMES_FILE = './data/labels/obj.names'
_MAX_OUTPUT_SIZE = 20
pygame.init()
screen = pygame.display.set_mode((800,800))

def main(type, iou_threshold, confidence_threshold, input_names):
    class_names = load_class_names(_CLASS_NAMES_FILE)
    n_classes = len(class_names)

    model = Yolo_v3(n_classes=n_classes, model_size=_MODEL_SIZE,
                    max_output_size=_MAX_OUTPUT_SIZE,
                    iou_threshold=iou_threshold,
                    confidence_threshold=confidence_threshold)

    if type == 'webcam':
        inputs = tf.compat.v1.placeholder(tf.float32, [1, *_MODEL_SIZE, 3])
        detections = model(inputs, training=False)
        saver = tf.compat.v1.train.Saver(tf.compat.v1.global_variables(scope='yolo_v3_model'))

        with tf.compat.v1.Session() as sess:
            saver.restore(sess, './weights/model.ckpt')

            win_name = 'Webcam detection'
            # cv2.namedWindow(win_name)
            
            cap = cv2.VideoCapture(0)
            cap.set(3,640)
            cap.set(4,480)
            frame_size = (cap.get(cv2.CAP_PROP_FRAME_WIDTH),
                          cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fourcc = cv2.VideoWriter_fourcc(*'X264')
            fps = cap.get(cv2.CAP_PROP_FPS)
            out = cv2.VideoWriter('./detections/detections.mp4', fourcc, fps,
                                  (int(frame_size[0]), int(frame_size[1])))
            
            screen = pygame.display.set_mode((1300,800))
            done =True
            try:
                while done:
                    screen.fill((255,55,210))
                    for event in pygame.event.get():  # User did something
                        print('event')
                        if event.type == pygame.QUIT:  # If user clicked close
                            break  # Flag that we are done so we exit this loop
                        if event.type == pygame.KEYDOWN:  # If user clicked close
                            if event.key == pygame.K_q:
                                print('kill')
                                done = False
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    frame = frame.swapaxes(0, 0)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    resized_frame = cv2.resize(frame, dsize=_MODEL_SIZE[::-1],
                                               interpolation=cv2.INTER_NEAREST)
                    detection_result = sess.run(detections,
                                                feed_dict={inputs: [resized_frame]})
                    draw_frame(frame, frame_size, detection_result, class_names, _MODEL_SIZE)
                    frame=numpy.rot90(frame)
                    frame=pygame.surfarray.make_surface(frame)

                    screen.blit(frame,(0,0))
                    key = cv2.waitKey(1) & 0xFF

                    if key == ord('q'):
                        print('qqqq')
                        break
                    pygame.display.flip()
                    # out.write(frame)
            finally:
                cv2.destroyAllWindows()
                # cap.release()
                print('Detections have been saved successfully.')

    else:
        raise ValueError("Inappropriate data type. Please choose either 'video' or 'images'.")


if __name__ == '__main__':
    main('webcam', 0.5, 0.5, sys.argv[4:])
