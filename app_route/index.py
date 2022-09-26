
from flask import Flask, request
 
app = Flask(__name__)
 
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/' , methods=['POST'])
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'Hello World'

# @app.route('/mask', methods=['POST'])
# # ‘/’ URL is bound with hello_world() function.
# def mask():
#     variable_name = request.form['<key name>']


# main driver function
if __name__ == '__main__':
    app.run()