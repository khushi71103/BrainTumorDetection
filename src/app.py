import os
import tensorflow as tf
import numpy as np
from email.message import EmailMessage
from PIL import Image
import cv2
from keras.models import load_model
from flask import Flask,request;
from flask import render_template;
from werkzeug.utils import secure_filename
import pymongo
import pdfkit
from fpdf import FPDF
import smtplib
import concurrent.futures
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from time import sleep

app = Flask(__name__, template_folder='template',static_folder='static')
global new

model=load_model('src\BrainTumor10EpochsCategorical.h5')
print('Model loaded. Check htttps://127.0.0.1:3000/')

# def mail(receiver_mail_id, message):
#     s = smtplib.SMTP('smtp.gmail.com', 587)
#     s.starttls()
#     s.login("jackson10021903@gmail.com", "cszveeybeisomffb")
#     s.sendmail("khushi71103@gmail.com", receiver_mail_id, message)
#     s.quit()


# def databaseInsert(name, emailId, username, contact, nu):
#     client = pymongo.MongoClient("mongodb://localhost:27017")
#     db = client['braintumor']
#     collection = db['braintumor']
#     dictionary = {"Name": name, "Email-ID": emailId,"Username": username, "Contact": contact, "Prediction": nu}
#     collection.insert_one(dictionary)

predictions = ["No", "Yes"]


def getResult(img,name, emailId, username, contact):
    image=cv2.imread(img)
    img=Image.fromarray(image)
    img=img.resize((64,64))
    img=np.array(img)
    input_img=np.expand_dims(img,axis=0)
    result = model.predict(input_img)
    result_final=np.argmax(result,axis=-1)
    # result = np.argmax(model.predict(input_img), axis=0)
    a=predictions[result_final[0]]
    print(f"\n\n\n\n\n\nPredicted: {a}\n\n\n\n\n\n")
    
    file1 = open("basefile.txt", "w")
  
    if(a=="No"):
        mm =   f"""
                        BRAIN TUMOR report by MindTumorVision

     Patient name:Khushi
     Age: 18
     Email id:jackson10021903@gmail.com
     Contact no:7708138923

     Diagnosis:
     1. Brain MRI scan shows signs of no tumor.
     2. Patient is advised to get a checkup regularly.

     Further advice for treatment:
     ->For further advice the patient can visit the nearest hospital 
        to the current location(as displayed on the website).
     ->To contact us visit our MindTumorVision web app."""
        
    elif(a=="Yes"):
        mm =  f"""
                        BRAIN TUMOR report by MindTumorVision

     Patient name:Khushi
     Age: 18
     Email id:jackson10021903@gmail.com
     Contact no:7708138923

     Diagnosis:
     1. Brain MRI scan shows signs of tumor.
     2. Patient is stronlgy advised to meet a neurosurgeon or neuro-oncologist.
     3. Patient will require surgery to avoid any further tumor related issues.

     Further advice for treatment:
     ->Based on the imaging findings, further medical evaluation and consultation 
       with a neurosurgeon or neuro-oncologist are recommended.
     ->For further advice the patient can visit the nearest hospital 
        to the current location(as displayed on the website).
     ->To contact us visit our MindTumorVision web app."""
        
    file1.writelines(mm)
    file1.close()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    f = open("basefile.txt", "r")
    for x in f:
        pdf.cell(200, 8, txt=x, ln=.8, align='L')
    print("Done with pdf")
    # databaseInsert(name, emailId, username, contact, a)
    pdf.output('report.pdf')
    body = '''Hello,
    This is the body of the email
    sicerely yours
    G.G.
    '''
    sender = 'jackson10021903@gmail.com'
    password = 'cszveeybeisomffb'
    receiver = emailId
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = 'This email has an attacment, a pdf file'
    message.attach(MIMEText(body, 'plain'))
    pdfname = 'report.pdf'
    binary_pdf = open(pdfname, 'rb')
    payload = MIMEBase('application', 'octate-stream', Name=pdfname)
    payload.set_payload((binary_pdf).read())
    encoders.encode_base64(payload)
    payload.add_header('Content-Decomposition', 'attachment', filename=pdfname)
    message.attach(payload)
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender, password)
    text = message.as_string()
    session.sendmail(sender, receiver, text)
    session.quit()
    print('Mail Sent')

img='src\\y1.jpg'
name='ayaan'
emailId='zzrex0711@gmail.com'
username='sdsd'
contact='434343453'
getResult(img,name, emailId, username, contact)
@app.route('/', methods=['GET'])
def hello_world():
    return render_template('form.html')


@app.route('/', methods=['POST'])
def predict():
    name = request.form['name']
    emailId = request.form['emailId']
    contact = request.form['contact']
    username = request.form['username']
    print(name, emailId, contact, username)
    imagefile = request.files['imagefile']
    image_path = "images/"+imagefile.filename
    imagefile.save(image_path)
    getResult(image_path, name, emailId, username, contact)
    return render_template('form.html')

if __name__ == '__main__':
    app.run(port=3000, debug=True)

#print(getResult('src\\y1.jpg'))
# classNo = getResult('src\y1.jpg')
# def get_className(classNo):
#     if classNo==0:
#         return "No brain Tumor"
#     elif classNo==1:
#         return "Yes brain Tumor"


# @app.route("/",method=['GET'])
# def index():
#     return render_template('index.html')

# @app.route('/predict',methods=['GET','POST'])
# def upload():
#     if request.method=="POST":
#         f=request.files['file']
#         basepath=os.path.dirname(__file__)
#         file_path=os.path.join(basepath,'uploads',secure_filename(f.filename))
#         f.save(file_path)
#         value=getResult(file_path)
#         result=get_className(value)
#         return result
#     return None

# if __name__ == '__main__':
#     app.run(port=3000, debug=True)