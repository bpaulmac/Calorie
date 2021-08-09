from datetime import time
from flask import Flask, request, render_template, flash, redirect, jsonify
from image_processing import detect_contour
from werkzeug.utils import secure_filename
import os
import base64, time
from urllib import request as eeee
import json

from cal_api import calorie_info



app = Flask(__name__)

UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def my_form():
    return render_template('home.html')

@app.route('/upload', methods=['POST', 'GET'])
def my_form_post():
    if request.method == 'GET':
        return render_template('index.html')

    dir = app.config['UPLOAD_FOLDER']
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    # print(request.form.keys())
    # if 'file' not in request.form.keys():
    #     if 'file' not in 
    #     flash('No file part')
    #     return redirect(request.url)
    
    # if user does not select file, browser also
    # submit an empty part without filename
    print(type(request.form['new_dude']), request.form['new_dude'])
    if request.form['new_dude'] == '4':
        # print(file)
        file = request.form['file']
        img_data = file
        
        filename = 'in_{}.jpg'.format(time.time())
        
        with eeee.urlopen(img_data) as response:
            data = response.read()

        with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), "wb") as f:
            f.write(data)
       
    else:
        file = request.files['file']
        filename = request.files['file'].filename
        
        # elif file.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)
        if file and allowed_file(filename):
            filename = 'in_{}.jpg'.format(time.time())
            filename = secure_filename(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    calories, detections = calorie_info(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    if len(calories.keys()) == 0:
        return jsonify({'full_detctions' : 'none', 'area' :  '0 cm Square', 'data' : calories, 'names' : 'No food', 'free_area' : '440 cm Square	'})
    else:
        food_names = [i for i in calories]
    
    contour, area = detect_contour(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    print(area)
    free_area = area
    area = 420 - area
    
    return jsonify({'full_detctions' : detections, 'area' :  '{} cm Square'.format(area), 'data' : json.dumps(calories), 'names' : food_names, 'free_area' : '{} cm Square'.format(free_area)})

# @app.route('/view', methods=['POST', 'GET'])
# def view():
#     if request.method == 'GET':
#         return render_template(r'view/index.html')
#     return render_template(r'view/index.html')

if __name__ == "__main__":
    app.run(debug=True, threaded=False)
