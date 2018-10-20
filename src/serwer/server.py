import io
import os
import uuid

import cv2
import numpy as np
import tensorflow as tf
from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from keras.applications import inception_v3
from keras.applications.imagenet_utils import decode_predictions
from keras.preprocessing.image import img_to_array
from merc.categories import MercCategories

UPLOAD_FOLDER = "UPLOAD_FOLDER"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__, static_url_path='')

global graph
global inception_model
global merc_cat


def classify(original):
    numpy_image = img_to_array(original)
    image_batch = np.expand_dims(numpy_image, axis=0)
    processed_image = inception_v3.preprocess_input(image_batch.copy())
    predictions = inception_model.predict(processed_image)
    label = decode_predictions(predictions)

    return label


def prepare_model(image, output_dict):
    view_model = dict()
    view_model['image'] = image
    view_model['objects'] = list()

    print(output_dict)
    if len(output_dict[0]) == 0:
        return

    detected_obj = output_dict[0][0]
    obj = dict()
    obj['detectedClass'] = detected_obj[1]
    mapped_class = merc_cat.find_by_cat3(detected_obj[1])
    if mapped_class is not None:
        obj['class'] = mapped_class['category_name']
        obj['stars'] = mapped_class['stars']
        obj['sale_time'] = mapped_class['sale_time']

    view_model['objects'].append(obj)

    return view_model


@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = save_to_file(f)
        in_memory_file = io.BytesIO()
        f.save(in_memory_file)
        data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
        color_image_flag = 1
        img = cv2.imdecode(data, color_image_flag)
        # img = cv2.resize(img, (200, 200))

        with graph.as_default():
            output_dict = classify(img)

        return render_template('list.html', model=prepare_model(filename, output_dict))

    else:
        return render_template('index.html')


@app.before_first_request
def activate_job():
    global graph
    global inception_model
    global merc_cat
    graph = tf.get_default_graph()
    inception_model = inception_v3.InceptionV3(weights='imagenet')
    merc_cat = MercCategories('sales_to_list_ratio.csv')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


def save_to_file(f):
    filename = str(uuid.uuid4()) + ".jpg"
    f.save(os.path.join(UPLOAD_FOLDER, filename))
    f.seek(0)
    return filename


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
