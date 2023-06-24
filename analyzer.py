'''
GOAL OF SCRIPT
The goal of this script is to scrape some parts of the xml file into a csv. The parts we are interested in are whether
the model classified any eyes as leukocoric or not and what the HSV metrics are.
The features of the csv we're interested in are the following:

image name | face # | left eye detected (T/F) | right eye detected (T/F) 
------------------------------------------------------------------------
'''
import csv
import xml.etree.ElementTree as ET
import os

tree = ET.parse('17NLlog.xml')
root = tree.getroot()
features = ['Image_Name', 'Face #', 'Left Eye Detected (T/F)', 'Right Eye Detected (T/F)', 'Face #', 'Left Eye Detected (T/F)', 'Right Eye Detected (T/F)', 'Face #', 'Left Eye Detected (T/F)', 'Right Eye Detected (T/F)',
'Face #', 'Left Eye Detected (T/F)', 'Right Eye Detected (T/F)', 'Face #', 'Left Eye Detected (T/F)', 'Right Eye Detected (T/F)']

rowsData = []
for child in root: # for each image...
    # write the image name to column 0. You can get image name from child.attrib['path']
    rowData = []
    rowData.append(child.attrib['path'])
    detected = False # Assume that each image does not have a detected face
    faceID = -1 #declare a faceID

    for gchild in child: # for each potential face...
        # First check if there even is a face, if so, for each face tag under each image, assign that face an ID. Then write the face ID to column 2. If not write "NO FACE DETECTED"
        if gchild.tag == 'face':
            detected = True
        if detected and gchild.tag == 'face':
            faceID += 1
            rowData.append(faceID)
            for g2child in gchild: # for eyes tag under face 
                for g3child in g2child:
                    # for each eye tag, you know the first one is always left. So, in column 3 for left, return T if anomaly_deteted = 'true else return F. Do the same thing for right eye in column 4
                    if g3child.attrib['anomaly_detected'] == 'true':
                        anomaly = True
                    else:
                        anomaly = False
                    rowData.append(anomaly)
        else:
            rowData.append('NO FACE DETECTED')
    rowsData.append(rowData)

with open('analyzedEyes.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(features)
    writer.writerows(rowsData)
