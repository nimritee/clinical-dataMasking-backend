from flask import Flask, jsonify, request, send_file
import os
import zipfile
from nerm import nerm
from mask import masking


UPLOAD_FOLDER = 'data/input/unannotated_texts/'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = "data/output/"

def nerm_process():
    process_ner = nerm.call_nerm()
    mask_ner = masking.main()

@app.route("/")
def hello_world():
    return "<p>Hello, Wsssddsrldp>"


@app.route("/mask",methods=['POST'])
def upload_file():
    if 'file'  in request.files:
        files = request.files.getlist("file")
        zipfolder = zipfile.ZipFile('output.zip','w', compression = zipfile.ZIP_STORED)
        for file in files:
            try:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                nerm_process()
                zipfolder.write(app.config['DOWNLOAD_FOLDER']+file.filename)
                os.remove(app.config['DOWNLOAD_FOLDER']+file.filename)
                os.remove(app.config['UPLOAD_FOLDER']+file.filename)
            except Exception as e:
                print(e)
                os.remove(app.config['DOWNLOAD_FOLDER']+file.filename)
                os.remove(app.config['UPLOAD_FOLDER']+file.filename)
                print(app.config['UPLOAD_FOLDER']+file.filename)
                return("Invalid file type/name")

        zipfolder.close()
        return send_file('output.zip',
            mimetype = 'zip',
            as_attachment = True)
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