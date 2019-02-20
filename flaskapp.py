from flask import *
import os, sys

path = os.path.dirname(__file__)
app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)
