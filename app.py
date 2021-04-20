from flask import Flask
app = Flask(__name__)

#define the starting point, also known as the root
@app.route('/')
def hello_world():
    return 'Hello world'
#/ denotes that we want to put our data at the root of our routes, commonly known as the highest hierarchy in any computer system

#function called hello_world(). put the code you want in that specific route below @app.route('/')
#route completed 