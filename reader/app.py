from flask import Flask, render_template, request, redirect, url_for,flash
import PyPDF2
import os
from werkzeug.utils import secure_filename
import requests
from bs4 import BeautifulSoup
import sys
import time
import json
import string
import re
import unicodedata
#pymupdf is called fitz for some odd reason
import fitz

def strip_accents(text):

    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

"""
def read(file_name):
    newfile=relativepath(file_name)
    file = open(newfile,'rb')
    fileReader=PyPDF2.PdfFileReader(file)
    words=[]
    for i in range(fileReader.numPages):
        pageObj = fileReader.getPage(i)
        stringraw=pageObj.extractText()
        sometype=stringraw.split()
        for j in range(len(sometype)):
            words.append(sometype[j])
    return words
"""
def read(file_name):
    newfile=relativepath(file_name)
    doc=fitz.open(newfile)
    pages = len(doc)
    words=[]
    for page in doc:
        text=page.getText()
        for word in text.splitlines():
            words.append(word)
    return words
def relativepath(filename, subdirectory=''):
    dirname=os.getcwd()
    if subdirectory is not '':
        dirname=os.path.join(dirname,subdirectory)
    filepath = os.path.join(dirname, filename)
    return filepath
UPLOAD_FOLDER = relativepath('')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = relativepath('')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            
            #filename = secure_filename(file.filename)
            filename="temp"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('scroller'))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''



@app.route('/reader')
def reader():
    text = read('temp')
    table=str.maketrans('','', string.punctuation)
    only_letters=[words.translate(table) for words in text ]
    stripped=[strip_accents(words) for words in only_letters]
    lowered=[words.lower() for words in stripped]

    return render_template('reader.html', text=json.dumps(lowered))

@app.route('/scroller')
def scroller():
    text = read('temp')
    table=str.maketrans('','', string.punctuation)
    only_letters=[words.translate(table) for words in text ]
    new_text=' '.join(only_letters)
    print(new_text)
    """
    stripped=[strip_accents(words) for words in text]
    new_text=' '.join(stripped)
    return render_template('scroll.html', text=json.dumps(new_text, ensure_ascii=False))
    """
    return render_template('scroll.html', text=json.dumps(new_text, ensure_ascii=False))
if __name__ == '__main__':
    app.run(debug=True)
