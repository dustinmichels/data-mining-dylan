from flask import Flask, render_template, send_from_directory
import folium

app = Flask(__name__, static_url_path='')

@app.route('/maps/map.html')
def show_map():
    return send_from_directory('maps', 'map.html')

@app.route('/')
def index():
    # start_coords = (46.9540700, 142.7360300)
    # folium_map = folium.Map(location=start_coords, zoom_start=14)
    # folium_map.save('templates/map.html')
    return render_template('index.html')
    # return app.send_static_file('maps/map.html')

if __name__ == '__main__':
    app.run(debug=True)
