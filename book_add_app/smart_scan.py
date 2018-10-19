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


def smart_scan(img):
    # import pdb; pdb.set_trace()
    client = vision.ImageAnnotatorClient()
    img = '.' + img
    with io.open(img, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    results = client.text_detection(image=image)
    serialized = json.loads(MessageToJson(results))

    # blocks = serialized['fullTextAnnotation']['pages'][0]['blocks']
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(serialized['textAnnotations'])
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

    books = []
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
    return books

