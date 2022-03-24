from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from removeDuplicates import remove_duplicates

ALLOWED_EXTENSIONS = ['xlsx']

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('duplicate_removal.html')

@app.route('/getunique', methods=['GET', 'POST'])
def getunique():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if not allowed_file(file.filename):
            flash('Please choose a file with extension .xlsx')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            path = remove_duplicates(file)
            return "Please find the output file in the path " + path


if __name__ == '__main__':
    app.run(debug=True)