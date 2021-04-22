import joblib
import os
import numpy as np
import pandas as pd
import os
from flask import Flask, flash, request, jsonify, abort, redirect, url_for, render_template, send_file 
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, FileField
from wtforms.validators import DataRequired, InputRequired

app = Flask(__name__)
UPLOAD_FOLDER = './files/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
knn = joblib.load('knn.joblib')

# functions 
def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


@app.route('/')
def index():
    services = [
        {
            'service': {'name': 'iris task', 'link': 'iris_tasks'}
        },
        {
            'service': {'name': 'iris dataset', 'link': 'iris'}
        },
        {
            'service': {'name': 'avg', 'link': 'avg'}
        }, 
        {
            'service': {'name': 'user', 'link': 'user'}
        },
        {
            'service': {'name': 'Prediction of the type of iris flower from the csv file data', 'link': 'iris_submit'}
        },
        {
            'service': {'name': 'Prediction of the type of iris flower from the csv file data API', 'link': 'iris_upload'}
        }]
    return render_template('index.html', services=services)


@app.route('/iris_tasks')
def iris_tasks():
    form = IrisInputForm()
    services = [
        {
            'service': {'name': 'iris prediction for params', 
                        'link': 'iris',
                        'form': form}
        },
        {
            'service': {'name': 'download iris dataset (csv format)', 'link': 'iris_submit'}
        }]
    
    return render_template('services.html', services=services)

class CheckIrisParams(object):
    def __init__(self, params=[], message=None):
        self.params = params
        if not message:
            message = 'Field must be four characters separated by a commas'
        self.message = message

    def __call__(self, form, field):
        params_list = split(self.params)
        print(str(params))
        print(str(params_list))
        #    raise ValidationError(self.message)

check_iris_params = CheckIrisParams

class IrisInputForm(FlaskForm):
    name = StringField('Name', [InputRequired(), check_iris_params()])

@app.route('/iris/<param>')
def iris(param):
    try:
        form = IrisInputForm()
        param = param.split(',')
        param = [float(num) for num in param]
        param = np.array(param).reshape(1,-1)
        predict = knn.predict(param)
        dict = {1: 'setosa', 2: 'versicolor', 3: 'virginica'}
    except:
        return redirect(url_for('bad_request'))
    image = f'<img height=100 width=100 src="/static/{dict[predict[0]]}.jpg" alt="{dict[predict[0]]}">'
    return render_template('services.html', form_input=form, image=image)


@app.route('/iris_post', methods=['POST'])
def post():
    content = request.get_json()
    try:
        param = content['flower'].split(',')
        param = [float(num) for num in param]
        param = np.array(param).reshape(1,-1)
        predict = knn.predict(param)
        predict = {'class': str(predict[0])}
    except:
        return redirect(url_for('bad_request'))
    return jsonify(predict)


app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

class IrisSubmitForm(FlaskForm):
    #name = StringField('name', validators=[DataRequired()])
    file = FileField(validators=[FileRequired()])

@app.route('/iris_submit', methods=('GET', 'POST'))
def iris_submit():
    form = IrisSubmitForm()
    if form.validate_on_submit():
        f = form.file.data
        filename = 'iris_predict_file.csv'
        #filename = form.name.data + '.csv' 

        #filename = secure_filename(f.filename)
        #f.save(os.path.join(
        #    'files/', filename
        #))

        df = pd.read_csv(f, header=None)
        #print(df.head())

        predict = knn.predict(df)
        #print(predict)

        result = pd.DataFrame(predict)
        result.to_csv(filename, index=False)

        return send_file(filename,
                     mimetype='text/csv',
                     attachment_filename=filename,
                     as_attachment=True)

    return render_template('services.html', form=form)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/iris_upload', methods=['GET', 'POST'])
def upload_file():
    print('request method ='+str(request.method))
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename + 'uploaded')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect(url_for('uploaded_file',
            #                        filename=filename))
            return 'file uploaded'
            
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/badrequest400')
def bad_request():
    return abort(400)