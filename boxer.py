import cv2
import xml.etree.ElementTree as ET
import os

tree = ET.parse('17NLlog.xml')
root = tree.getroot()

'''
PROBLEM and ANSWER

1. The log file contains multiple images of the same name. Since two different patients may have two different images of the same name, there is no way
of differentiating the 2 images unless you're told which image belonged to which patient. Which is information I don't have. What is happening currently
is that I will read every single replicate and generate multiple boxed images for that unique image. But what happens is that you may get multiple
images that are wrong for different reasons and I cannot differentiate whether it is because the model had wrongly tagged the image or if the image
was from a different patient.
1ANS. To get around this, if I can have a log file per patient, then I won't run into multiple images of the same name in the log file. Then, I can 
simply just extract the box locations and add them to the image.  

See email sent to Travis on Jan 29th 2023.c
'''

for child in root: # for each image try to see if it's there, if not then pass.
    pic_anomaly = False # assume there is no anomaly detected
    try:
        img = cv2.imread(child.attrib['path'])
        #print(child.attrib['path'])
        detected = False # Assume that each image does not have a detected face
        for gchild in child: # for each face tag under each image, check if face is detected, if so get the coordinates of each face, then draw the coordinates, the generate the image
            if gchild.tag == 'face':
                detected = True
                for g2child in gchild: # for eyes tag under face 
                    for g3child in g2child: # for each eye tag under eyes get whether an anomaly was detected or not.
                        anomaly = False
                        anomaly_text = g3child.attrib['anomaly_detected']
                        if g3child.attrib['anomaly_detected'] == 'true':
                            pic_anomaly = True
                            anomaly = True
                        Id = str(g3child.attrib['id'])
                        for g4child in g3child: #for the roi tag under eye tag get the coordinates of the eye then draw the box around the coordinate
                            if g4child.tag == 'roi':
                                x = int(g4child.attrib['x'])
                                y = int(g4child.attrib['y'])
                                width = int(g4child.attrib['width'])
                                height = int(g4child.attrib['height'])
                                #print(Id, anomaly_text, anomaly, x, y, width, height) 
                                if anomaly == False:
                                    cv2.rectangle(img, (x-4*width, y-4*height), (x+4*width, y+4*height), (0,255,0), 3) #BGR
                                else:
                                    cv2.rectangle(img, (x-4*width, y-4*height), (x+4*width, y+4*height), (0,0,255), 3) #BGR
                                ''' 
                PROBLEM
                It's possible to have multiple images of the same name. What ends up happening in this case is that, as you read through the xml file
                you'll get the x y and anomaly attributes of the last image of the same name and this will over-write any images of the same name you had before.
                This is problematic. What if the image you have, say X.jpg, had the attributes of the first instance in the log file and the not the last.
                Then that means the X_boxed.jpg will not represent what the model actually tagged.

                To get around this, you should first check if "imagepath_boxed.jpg" already exists in the directory. If it does, that means that you've
                seen this image name before and have boxed the x y attributes of the first instance seeing it. Then the next time you run into an instance
                You can write a whole new image "imagepath_boxed2" or "imagepath_boxed3" so that you don't over-write the previous image.
                
                SOLUTION
                Check if "imagepath_boxed" already exists in the directory, if it does then write "imagepath_boxed2" instead.
                '''
        if detected and pic_anomaly and os.path.exists(child.attrib['path'] + '_BOXED_ANOMALY.jpg'):
            cv2.imwrite(child.attrib['path'] + '_BOXED_ANOMALY2.jpg', img)
        elif detected and pic_anomaly and os.path.exists(child.attrib['path'] + '_BOXED_ANOMALY2.jpg'):
            cv2.imwrite(child.attrib['path'] + '_BOXED_ANOMALY3.jpg', img)
        elif detected and pic_anomaly:
            cv2.imwrite(child.attrib['path'] + '_BOXED_ANOMALY.jpg', img)
        elif detected and not pic_anomaly and os.path.exists(child.attrib['path'] + '_BOXED_ANOMALY.jpg'):
            cv2.imwrite(child.attrib['path'] + '_BOXED_NO_ANOMALY2.jpg', img)
        elif detected and not pic_anomaly and os.path.exists(child.attrib['path'] + '_BOXED_ANOMALY2.jpg'):
            cv2.imwrite(child.attrib['path'] + '_BOXED_NO_ANOMALY3.jpg', img)
        elif detected and not pic_anomaly:
            cv2.imwrite(child.attrib['path'] + '_BOXED_NO_ANOMALY.jpg', img)
        if detected == False and os.path.exists(child.attrib['path'] + '_BOXED_ANOMALY.jpg') == False:
            #cv2.putText(img, 'NO FACE DETECTED', org = (50,50), fontScale = 25)
            cv2.imwrite(child.attrib['path'] + '_NOFACE.jpg', img)
    except:
        pass