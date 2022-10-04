from flask import Flask, jsonify, request, send_file
from jinja2 import Undefined
from nerm import nerm
import os
import zipfile
import sys
sys.path.insert(0, 'mask')
from masking import main

UPLOAD_FOLDER = 'data/input/'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = "data/output/"

def nerm_process():
    process_ner = nerm.call_nerm()
    






@app.route("/")
def hello_world():
    return "<p>Hello, Wsssddsrldp>"

@app.route("/mask",methods=['POST'])
def upload_file():
    if 'file'  in request.files:
        files = request.files.getlist("file")
        zipfolder = zipfile.ZipFile('output.zip','w', compression = zipfile.ZIP_STORED) # Compression type 

        # f.save(os.path.join('data/input',"news.txt"))
        for file in files:
            try:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                nerm_process()
                zipfolder.write(app.config['DOWNLOAD_FOLDER']+file.filename)
                os.remove(app.config['DOWNLOAD_FOLDER']+file.filename)
                os.remove(app.config['UPLOAD_FOLDER']+file.filename)

            except:
                # os.remove(app.config['DOWNLOAD_FOLDER']+file.filename)
                os.remove(app.config['UPLOAD_FOLDER']+file.filename)
                # print(app.config['UPLOAD_FOLDER']+file.filename)
                return("Invalid file type/name")

        zipfolder.close()
        return send_file('output.zip',
            mimetype = 'zip',
            as_attachment = True)
            # return send_file(path)

    else:
        input_data= request.form.get("input_data")
        if(input_data):
            print()
            with open(app.config['UPLOAD_FOLDER']+"uploaddate.txt", 'w') as f:
                    f.write(str(input_data))
            nerm_process()
            f = open(app.config['DOWNLOAD_FOLDER']+"uploaddate.txt", "r")
            text = f.read().replace('\n',' ')
            return(jsonify(text))
        else:
            return "invalid input"

if __name__ == '__main__':
    app.run(debug=True)