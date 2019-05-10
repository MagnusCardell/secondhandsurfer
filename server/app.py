# server/app.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello world to python flask web api '


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)