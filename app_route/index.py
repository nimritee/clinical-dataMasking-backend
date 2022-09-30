from turtle import clear
from flask import Flask, flash, request, redirect, render_template
import json
import os

ALLOWED_EXTENSIONS = {'txt'}
UPLOAD_FOLDER = 'data/input/'
file_list = []

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

# @app.route('/', methods=['GET'])
# def get_tasks():
#     return jsonify({'tasks': tasks})

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        if 'input_files' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('input_files')

        for file in files:
            if file and allowed_file(file.filename):
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        flash('File(s) successfully uploaded')
        return redirect('/')


if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=False,threaded=True)

# @app.route('/mask', methods=['POST'])
# def mask():
#     # input = json.loads(request.data)
#     data = request.form
#     files = request.files.getlist('input_files')
#     for file in files:
#         if file and allowed_file(file.filename):
#             filename = file.filename
#             file_list.append(filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#     return file_list

#     # input_files = request.files['input_files']
#     # if input_files.filename == '':
#     #     return "empty"
#     # else:
#     #     if input_files and allowed_file(input_files.filename):
#     #         input_files.save(os.path.join(app.config['UPLOAD_FOLDER'], input_files.filename))

#     #         return input_files.filename
#     #     print(data['input_data'])
#     #     return data['input_data']


if __name__ == '__main__':
    app.run(debug=True)