import json
from flask import Flask, render_template, request
import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import requests
import requests

app = Flask(__name__, template_folder="templates")
model = load_model('nutrition.h5')
print("Loaded model from disk")

# Replace 'YOUR_API_KEY_HERE' with your actual Calorie Ninjas API key
API_KEY = 'EhapY/itUznqgJOTIr/sWw==QpPe21sVezPJRjbi'

def vishak(output):
    api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
    query = output
    response = requests.get(api_url + query, headers={'X-Api-Key': 'EhapY/itUznqgJOTIr/sWw==QpPe21sVezPJRjbi'})
    if response.status_code == requests.codes.ok:
        print(response.text)
        return response.text
    else:
        print("Error:", response.status_code, response.text)
        return 'error'

def nutrition(index):
    url = "https://calorieninjas.p.rapidapi.com/v1/nutrition"
    querystring = {"query": index}
    headers = {
        'X-RapidAPI-Key': API_KEY,
        'X-RapidAPI-Host': 'calorieninjas.p.rapidapi.com'
    }
    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    print("Response:")
    print(response.text)
    return response.json().get("items", [])  # Handle empty response gracefully

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/image1', methods=['GET', 'POST'])
def image1():
    return render_template("image.html")

@app.route('/predict', methods=['GET', 'POST'])
def launch():
    nutrition_data = []  # Initialize nutrition_data here
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        filepath = os.path.join(basepath, "uploads", f.filename)
        f.save(filepath)

        img = image.load_img(filepath, target_size=(64, 64))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)

        pred = np.argmax(model.predict(x), axis=1)
        index = ['APPLE', 'BANANA', 'ORANGE', 'PINEAPPLE', 'WATERMELON']
        result = index[pred[0]]
        nutrition_data = nutrition(result)
        print(nutrition_data)
    nd=vishak(result)
    showcase_json = json.dumps(nd)
    return render_template("imageprediction.html", result=result, showcase=showcase_json)
if __name__ == "__main__":
    app.run(debug=True)
