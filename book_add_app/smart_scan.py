import io
import os
import json
from google.protobuf.json_format import MessageToJson
import cv2
import numpy as np
from matplotlib import pyplot as plt
import pprint

from google.cloud import vision
from google.cloud.vision import types


def smart_scan(img_path):
    books = []
    # import pdb; pdb.set_trace()
    client = vision.ImageAnnotatorClient()
    img_path = '.' + img_path
    with io.open(img_path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    results = client.text_detection(image=image)
    serialized = json.loads(MessageToJson(results))
    if 'textAnnotations' in serialized:
        blocks = serialized['textAnnotations']

        text_boxes = []
        for i in range(1, len(blocks)):
            block = blocks[i]
            text_box = {'text': block['description'], 'boundingPoly':[], 'midpoints':[], 'slope': None, 'intercept': None}
            for vertex in block['boundingPoly']['vertices']:
                curr_tuple = [vertex['x'], vertex['y']]
                text_box['boundingPoly'].append(curr_tuple)
            x = 0
            y = 1
            text_box['midpoints'].append(((text_box['boundingPoly'][0][x]+text_box['boundingPoly'][3][x])//2,
                                (text_box['boundingPoly'][0][y]+text_box['boundingPoly'][3][y])//2 ))
            text_box['midpoints'].append(((text_box['boundingPoly'][1][x]+text_box['boundingPoly'][2][x])//2,
                                (text_box['boundingPoly'][1][y]+text_box['boundingPoly'][2][y])//2 ))
            try:
                text_box['slope'] = (text_box['midpoints'][1][y]-text_box['midpoints'][0][y])/(text_box['midpoints'][1][x]-text_box['midpoints'][0][x])
                if text_box['slope'] > 50:
                    text_box['slope'] = 50
                    text_box['intercept'] = text_box['midpoints'][1][x]
                else:
                    text_box['intercept'] = (-text_box['slope']*text_box['midpoints'][1][x])+text_box['midpoints'][1][y]
            except ZeroDivisionError:
                text_box['slope'] = 1000000
                text_box['intercept'] = text_box['midpoints'][1][x]

            text_boxes.append(text_box)

    # pp.pprint(text_boxes)


        added = {}
        for i, first_text_box in enumerate(text_boxes):
            if i not in added:
                first_slope = first_text_box['slope']
                first_intercept = first_text_box['intercept']
                curr_book = first_text_box['text']
                for j, second_text_box in enumerate(text_boxes):
                    if j not in added and i is not j:
                        second_slope = second_text_box['slope']
                        second_intercept = second_text_box['intercept']
                        next_book = second_text_box['text']
        #                 print(curr_word,first_slope, next_word, second_slope)
                        if (abs((first_slope*0.90)) <= abs(second_slope) <= abs((first_slope*1.10))) and (abs((first_intercept*0.90)) <= abs(second_intercept) <= abs((first_intercept*1.10))):
                            curr_book += ' ' + next_book
                            added[j] = True
                if len(curr_book) > 5:
                    books.append(curr_book)
        # print(books)
        img = cv2.imread(img_path)
        for text in text_boxes:
            bounds = text['boundingPoly']
            pts = np.array(bounds, np.int32)
            pts = pts.reshape((-1,1,2))
            img = cv2.polylines(img,[pts],True,(0,255,0),3)
            img = cv2.line(img,text['midpoints'][0],text['midpoints'][1],(255,0,0),5)
        plt.rcParams['figure.figsize'] = (10,10)

        plt.imshow(img)
        cv2.imwrite(img_path, img)

    return books

