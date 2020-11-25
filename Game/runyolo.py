#pip install opencv-python
import cv2
import numpy as np
import pandas as pd
#Load YOLO
def change_loop_command(lst):
    check = [i for i,x in enumerate(lst) if x=='loop' or x=='end_num']
    for i in range(0, len(check), 2):
        count = 1
        for j in range(check[i]+1, check[i+1]):
            lst[j] = (count)
            count+=1
            
    check2 = [i for i,x in enumerate(lst) if x=='end_num' or x=='end loop']
    count = 0
    for i in range(0, len(check2), 2):
        for p in range(0, lst[check2[i]-2+count]):
            for j in range(check2[i]+1+count, check2[i+1]+count):
                lst.insert(check2[i+1]+count,lst[j])
                count += 1
        check = [i for i,x in enumerate(lst) if x=='loop' or x=='end_num']
    for i in range(0, len(check), 2):
        del lst[check[0]:check[1]+1]
        check = [i for i,x in enumerate(lst) if x=='loop' or x=='end_num']

    check_end_loop = [i for i,x in enumerate(lst) if x=='end loop']
    for i in range(0, len(check_end_loop)):
        lst.remove('end loop')
    return lst
def yolo():
    net = cv2.dnn.readNet("weights/yolov3_custom3_final.weights","weights/yolov3_custom3.cfg")
    classes = []
    with open("weights/obj.names","r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    outputlayers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors= np.random.uniform(0,255,size=(len(classes),3))
    #loading image
    img = cv2.imread("test_image/img_loop.JPG")
    img = cv2.resize(img,None,fx=0.4,fy=0.3)
    height,width,channels = img.shape
    blob = cv2.dnn.blobFromImage(img,0.00392,(416,416),(0,0,0),True,crop=False)
    #     for n,img_blob in enumerate(b):
    #         cv2.imshow(str(n),img_blob)

    net.setInput(blob)
    outs = net.forward(outputlayers)
    # print(outs[1])


    # Showing info on screen/ get confidence score of algorithm in detecting an object in blob
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # onject detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # cv2.circle(img,(center_x,center_y),10,(0,255,0),2)
                # rectangle co-ordinaters
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                # cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                boxes.append([x, y, w, h])  # put all rectangle areas
                confidences.append(float(confidence))  # how confidence was that object detected and show that percentage
                class_ids.append(class_id)  # name of the object tha was detected
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.5)

    font = cv2.FONT_HERSHEY_PLAIN
    lst = []
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            yolo = x, y, w, h
            label = str(classes[class_ids[i]])
            # color = colors[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, label, (x, y + 30), font, 1, (255, 255, 255), 2)
            # print(label)
            lst.append([x, y, label])
            # print(x, y)
    # cv2.imshow("prediction", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    sorted(lst, key=lambda x: x[-2])
   
    df = pd.DataFrame(sorted(lst, key=lambda x: x[1]), columns=['X', 'Y', 'label'])
    df.head()
    df['label'] = df['label'].astype(str)
    yoloclass = {
        "0": "start",
        "1": "end",
        "2": "move",
        "3": "turn left",
        "4": "loop",
        "5": "move",
        "6": "end_num",
        "7": "end loop",
        "8": "command3",
        "9": "if",
        "10": "condition1",
        "11": "condition2",
        "12": "condition3",
        "13": "command",
        "14": "else"
    }
    lst = []
    for i in df['label']:
        # print(yoloclass[i])
        lst.append(yoloclass[i])
    lst = change_loop_command(lst)
    df2 = pd.DataFrame(lst, columns=['label'])
    df2.to_csv('input.txt', index=False, header=False)
    print("Sucessfully please check input.txt")

