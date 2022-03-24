import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import pandas as pd


UPLOAD_FOLDER = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'upload')
ALLOWED_EXTENSIONS = {'xlsx'}

app = Flask(__name__, static_url_path="/static")
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

saved_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'unique.xlsx')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    if os.path.exists(saved_filename):
        os.remove(saved_filename)

    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print(file)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.rename(new_file, saved_filename)
            filename = 'unique.xlsx'
            remove_duplicates(os.path.join(
                app.config['UPLOAD_FOLDER'], filename), filename)
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('index.html')


def remove_duplicates(path, filename):

    df = pd.DataFrame(pd.read_excel(path))
    thismonth = df[['Article', 'Page count']]
    unique_data = thismonth.drop_duplicates()
    downloads_path = os.path.join(UPLOAD_FOLDER, filename)
    with pd.ExcelWriter(downloads_path) as writer:
        unique_data.to_excel(writer, sheet_name='unique', index=False)


@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
