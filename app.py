from flask import Flask, render_template, send_file
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/graphs')
def graphs():
    # Get the list of all image filenames in the "graphs" folder
    images = [f for f in os.listdir('graphs') if f.endswith('.png')]
    return render_template('graphs.html', images=images)

@app.route('/graphs/<filename>')
def graph(filename):
    # Serve a specific image file from the "graphs" folder
    return send_file(f'graphs/{filename}')

if __name__ == '__main__':
    app.run(debug=True)
