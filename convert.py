import lxml.etree
import glob
import os
import xml.etree.ElementTree as ET
from shutil import copyfile
import sys

# SET THIS INPUT FOLDER ONLY
INPUT_FOLDER = '/Users/Maitham/Developer/5_vid/test'

##############################################################

TRAIN_FOLDER = '{}/train'.format(INPUT_FOLDER)
TEST_FOLDER = '{}/test'.format(INPUT_FOLDER)

FOLDERS_RECURSE = [TRAIN_FOLDER, TEST_FOLDER]


CLASSES_TRAIN = [name for name in os.listdir(
    TRAIN_FOLDER) if os.path.isdir(TRAIN_FOLDER + '/' + name) and name.find('_processed') == -1]

CLASSES_TEST = [name for name in os.listdir(
    TEST_FOLDER) if os.path.isdir(TEST_FOLDER + '/' + name) and name.find('_processed') == -1]

# Check if classes in test and train folder are the same
if not len(CLASSES_TRAIN) == len(CLASSES_TEST):
    print('ERROR: number of classes in test and train do not match please double check')
    sys.exit()


CLASSES = CLASSES_TRAIN.copy()


# output all of classes
print('TOTAL CLASSES FOUND: {}'.format(len(CLASSES_TEST)))


# recurse over folders and classes and convert xml files to yolov2
for FOLDER in FOLDERS_RECURSE:
    for CLASS_NAME in CLASSES:
        OUTPUT_FOLDER = '{}/{}_processed/'.format(FOLDER,
                                                  CLASS_NAME)
        for filename in glob.glob('{}/{}/**/*.png'.format(FOLDER, CLASS_NAME), recursive=True):
            xmlFile = '{}/{}/'.format(FOLDER, CLASS_NAME) + \
                filename.split('/')[-1][:-4] + '.xml'

            if os.path.isfile(xmlFile):
                outputTxtFile = OUTPUT_FOLDER + \
                    filename.split('/')[-1][:-4] + '.txt'

                outputPngFile = OUTPUT_FOLDER + \
                    filename.split('/')[-1][:-4] + '.png'

                root = ET.parse(xmlFile).getroot()
                height = float(root[4][1].text)
                width = float(root[4][0].text)

                for objectXml in root.findall('object'):
                    for bndBox in objectXml.findall('bndbox'):
                        xmin = float(bndBox.find('xmin').text)
                        ymin = float(bndBox.find('ymin').text)
                        xmax = float(bndBox.find('xmax').text)
                        ymax = float(bndBox.find('ymax').text)

                        YOLO_x_cent = ((xmin + xmax) / 2) / width
                        YOLO_y_cent = ((ymin + ymax) / 2) / height
                        YOLO_x_width = xmax - xmin
                        YOLO_y_height = ymax - ymin

                if not os.path.exists(OUTPUT_FOLDER):
                    os.makedirs(OUTPUT_FOLDER)

                copyfile(filename, outputPngFile)
                with open(outputTxtFile, 'w') as text_file:
                    text_file.write('{} {} {} {} {}'.format(0, YOLO_x_cent, YOLO_y_cent,
                                                            YOLO_x_width, YOLO_y_height))
            else:
                print('XML FILE DOES NOT EXIST {}'.format(filename))
