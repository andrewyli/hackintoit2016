from flask import Flask, render_template, request
import smtplib
from flaskFeature import main
app = Flask(__name__)

def parse_csv(csv_location):
    import pandas as pd
    df = pd.read_csv(csv_location)
    df = df[['First Name', 'Last Name', 'E-mail Address', 'Company', 'Job Title']]
    return [df[x].tolist() for x in df]

result = parse_csv('linkedin_connections_export.csv')

@app.route("/")
def hello_world(name=None):
    return render_template("index.html", name=name)

@app.route('/result', methods = ['POST', 'GET'])
def result():
    return render_template("result.html", result=result)

@app.route('/thankyou', methods = ['POST', 'GET'])
def thankyou():
    thankyou_result = request.form
    return render_template("thankyou.html", result=thankyou_result)

class SendMessage:

    def __init__(self, address, password):
        self.username = address
        self.password = password

    def send_message(self, email, message, subject = "Text Message", from_address = "The Doctor"):

        fromaddr = self.username
        toaddrs  = email
        msg = "\n".join([
	  "From: " + from_address,
	  "To: "+email,
	  "Subject: " + subject,
	  "",
	  message
	  ])
        username = self.username
        password = self.password
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(username,password)
        server.sendmail(fromaddr, toaddrs, msg)
        server.quit()
        print('sent')

email = SendMessage('ifeelthebern69@gmail.com', 'Potatoes1')
email.send_message(email.username, "Text Here", "ConnectMe Report", "ConnectMe")
