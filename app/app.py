import json
import pandas as pd

from ipywidgets import IntSlider
from ipywidgets.embed import embed_data
from viz import get_place_selector

from flask import Flask, jsonify, render_template, request
app = Flask(__name__)


@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/widget')
def widget():

    # s1 = IntSlider(max=200, value=100)
    # s2 = IntSlider(value=40)
    # data = embed_data(views=[s1, s2])

    city_df = pd.read_json('data/city_counts.json')
    songs_df = pd.read_json('data/songs.json')
    widget = get_place_selector(city_df, songs_df)
    widget.children[0].children[0].value = 'Boston'
    data = embed_data(widget)

    manager_state = json.dumps(data['manager_state'])
    widget_views = [json.dumps(view) for view in data['view_specs']]

    return render_template(
        'main.html',
        manager_state=manager_state,
        widget_views=widget_views)


@app.route('/old')
def hello_world():

    s1 = IntSlider(max=200, value=100)
    s2 = IntSlider(value=40)
    data = embed_data(views=[s1, s2])

    manager_state = json.dumps(data['manager_state'])
    widget_views = [json.dumps(view) for view in data['view_specs']]

    return render_template(
        'hello.html', manager_state=manager_state, widget_views=widget_views)
