import os
from flask import Flask, jsonify, render_template, request, send_file,send_from_directory
import zipfile

from dataMasking import main

UPLOAD_FOLDER = 'data/input/'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = "data/output/"



@app.route("/")
def hello_world():
    return "<p>Hello, Wsssddsrldp>"

@app.route("/mask",methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        input_data= request.form.get("input_data")
        print()
        with open(app.config['UPLOAD_FOLDER']+"news.txt", 'w') as f:
                f.write(str(input_data))
        main()
        f = open(app.config['DOWNLOAD_FOLDER']+"news.txt", "r")
        text = f.read().replace('\n',' ')
        return(jsonify(text))
    else:
        files = request.files.getlist("file")
        zipfolder = zipfile.ZipFile('output.zip','w', compression = zipfile.ZIP_STORED) # Compression type 

        # f.save(os.path.join('data/input',"news.txt"))
        for file in files:
            try:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                main()
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
        return 'file uploaded successfully'


if __name__ == '__main__':
    app.run(debug=True)