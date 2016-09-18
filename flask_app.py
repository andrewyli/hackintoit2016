from flask import Flask, render_template, request
import smtplib
from flaskFeature import main
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
app = Flask(__name__)

def email_table(table):
    return '<html> <head> <link rel="stylesheet" href="/static/tablepage.css" /> </head> <body>' + ''.join(c for c in pd.DataFrame.from_records(table).to_html() if c not in "\n") + '</body> </html>'

def parse_csv(csv_location):
    import pandas as pd
    df = pd.read_csv(csv_location)
    df = df[['First Name', 'Last Name', 'E-mail Address', 'Company', 'Job Title']]
    return [df[x].tolist() for x in df]

contacts_result = parse_csv('linkedin_connections_export.csv')
output = []

@app.route("/")
def hello_world(name=None):
    return render_template("index.html", name=name)

@app.route('/result', methods = ['POST', 'GET'])
def result():
    return render_template("result.html", result=contacts_result)

@app.route('/thankyou', methods = ['POST', 'GET'])
def thankyou():
    thankyou_result = request.form
    global output
    for j in range(20):
        try:
            summary = main(contacts_result[4][j])
        except:
            continue
        comp_score = str(summary[0])
        salary = str(summary[1])
        output.append([contacts_result[0][j], contacts_result[1][j], contacts_result[2][j], contacts_result[3][j], contacts_result[4][j], comp_score, salary])
        print([contacts_result[0][j], contacts_result[1][j], contacts_result[2][j], contacts_result[3][j], contacts_result[4][j], comp_score, salary])

    output = sorted(output, key=lambda x: x[5])
    print(output)

    with open("output.csv", "w") as f:
        f.write("\n".join([",".join(x) for x in output]))

    return render_template("thankyou.html", result=thankyou_result)

@app.route('/tablepage', methods = ['POST', 'GET'])
def tablepage():
    with open("./templates/tablepage.html", "w") as f:
        f.write(email_table([["First Name", "Last Name", "Email", "Company", "Job Title", "Composite Score", "Starting Salary"]] + output))
    return render_template("tablepage.html", result=result)

class SendMessage:

    def __init__(self, address, password):
        self.username = address
        self.password = password

    def send_message(self, email, message, subject = "Text Message", from_address = "The Doctor"):
        # me == my email address
        # you == recipient's email address
        me = email
        you = email

        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "ConnectMe Report"
        msg['From'] = me
        msg['To'] = you

        # Create the body of the message (a plain-text and an HTML version).
        html = email_table(message)

        # Record the MIME types of both parts - text/plain and text/html.
        part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part2)

        # Send the message via local SMTP server.
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(self.username, self.password)
        server.sendmail(me, you, msg.as_string())
        # sendmail function takes 3 arguments: sender's address, recipient's address
        # and message to send - here it is sent as one string.
        server.quit()

# fromaddr = self.username
# toaddrs  = email
# msg = "\n".join([
#     "From: " + from_address,
#     "To: "+email,
#     "Subject: " + subject,
#     "",
#     message
# ])
# username = self.username
# password = self.password
# server = smtplib.SMTP('smtp.gmail.com:587')
# server.ehlo()
# server.starttls()
# server.login(username,password)
# server.sendmail(fromaddr, toaddrs, msg)
# server.quit()
# print('sent')

# email = SendMessage('ifeelthebern69@gmail.com', 'Potatoes1')
# email.send_message(email.username, email_table(output), "ConnectMe Report", "ConnectMe")
