import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from removeDuplicates import remove_duplicates, update_master_csv


UPLOAD_FOLDER = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'upload')
ALLOWED_EXTENSIONS = {'xlsx'}

app = Flask(__name__, static_url_path="/static")
app.secret_key = 'BMJ_INVOICE'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

saved_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'unique.xlsx')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    if os.path.exists(saved_filename):
        os.remove(saved_filename)
    if request.method == 'POST':
        if 'duplicates' in request.form:
            if 'file' not in request.files:
                flash('No file attached in request')
                return redirect(request.url)
            file = request.files['file']
            month = request.form['month']
            if file.filename == '':
                flash('No file selected')
                return redirect(request.url)
            if not allowed_file(file.filename):
                flash('Please choose a file with extension .xlsx')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                outputfile = 'duplicates_removed.xlsx'
                unique = remove_duplicates(UPLOAD_FOLDER, file, outputfile)
                update_master_csv(UPLOAD_FOLDER, unique, month)
                
                return redirect(url_for('uploaded_file', outputfile=outputfile))
        elif 'master' in request.form:
            return redirect(url_for('uploaded_file', outputfile='invoiced_files.csv'))
    return render_template('index.html')


@app.route('/upload/<outputfile>')
def uploaded_file(outputfile):
    return send_from_directory(app.config['UPLOAD_FOLDER'], outputfile, as_attachment=True)


if __name__ == '__main__':
    app.run()
