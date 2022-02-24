from flask import Flask, render_template, request, session, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from glob import glob
import json
import os
import sqlite3

path = os.path.join(os.getcwd(), 'static/img')

if not os.path.exists(path):
  os.makedirs(path, exist_ok=True)

UPLOAD_FOLDER = path

# from aws_s3 import AWS_S3_BUCKET_NAME, AWS_S3_BUCKET_REGION, s3_connection, s3_put_object, s3_get_object

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'test'

@app.route('/',methods=['GET', 'POST'])
def index():
  if request.method =='POST':
    userid = request.form["id"]
    userpwd = request.form['pwd']
    conn = sqlite3.connect('login.db', check_same_thread=False)
    cur = conn.cursor()
    x =cur.execute('''
    SELECT userid, userpwd FROM info WHERE userid=?''', (userid,))
    y = list(x)
    if (userid == y[0][0]) and(userpwd == y[0][1]):
      return render_template('upload.html')
    if (userid == y[0][0]) and(userpwd != y[0][1]):
      flash("비밀번호를 확인해주세요.")
      return render_template('index.html')
    cur.close()
    conn.close()
  return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method =='POST':
    userid = request.form["id"]
    userpwd = request.form['pwd']
    conn = sqlite3.connect('login.db', check_same_thread=False)
    cur = conn.cursor()
    x =cur.execute('''
    SELECT userid, userpwd FROM info WHERE userid=?''', (userid,))
    y = list(x)
    if userid != y[0][0]:
      cur.execute('''
        INSERT INTO info (userid, userpwd) VALUES (?,?)''', (userid, userpwd),)
      conn.commit()
      return redirect(url_for('index'))
    else:
      flash("아이디가 존재합니다.")
      return render_template('register.html')

  return render_template('register.html')

@app.route('/upload',methods=['GET', 'POST'])
def upload():
  # if request.method == 'POST':
  #   f = request.files.getlist('file[]')
  #   for i in f:
  #       y = os.join(current_app.config['UPLOAD_FOLDER'], i.filename)
  #       i.save(y)
  return render_template('upload.html')


@app.route('/fileUpload', methods=['GET', 'POST'])
def fileupload():
#if request.methods=='POST'
  from model import model
  # f = request.files.getlist('file[]')
  # # s3 = s3_connection()
  # for i in f:
  #   i.save('static/image/' + i.filename)
  
    #s3_put_object(s3, AWS_S3_BUCKET_NAME, 'static/image', f'{i}')
  if request.method == 'POST':
    f = request.files.getlist('file[]')
    y = []
    for i in f:
      if i.filename.split('.')[1] != 'jpg' or 'JPG' or 'PNG' or 'png' or 'webp':
        i.save(os.path.join(current_app.config['UPLOAD_FOLDER'], i.filename.replace(i.filename.split('.')[1], 'JPG')))
        y.append(i.filename.replace(i.filename.split('.')[1], 'JPG'))
      else:
        i.save(os.path.join(current_app.config['UPLOAD_FOLDER'], i.filename))
        y.append(i.filename)

    x = []
    for j in y:
      x.append(os.path.join('static/img', j))
    # x = glob('static/image/*.*')
    json_name = './kor_list.json'
    with open(json_name, encoding='utf-8') as j:
      read = json.load(j)

    model.eval()
    result = {}
    for i in x:
      model_result = model(i, size=640)

      targets = set()

      for pred in model_result.pred[0]:
        t = read[int(pred[-1])]
        targets.add(t)
      result[i] = list(targets)

    return render_template('main.html', results= result)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
  # x = glob('static/image/*.*')
  x = os.listdir('static/img')
  for i in x:
    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], i))
  session.clear()
  return redirect(url_for('index'))

if __name__ == '__main__':
  # import torch 

  # model2 = torch.hub.load('ultralytics/yolov5', 'yolov5m', pretrained=True)
  # model =model2.eval()
  
  app.run(host='127.0.0.1', port=5000, debug=True)