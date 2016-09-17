from flask import Flask, render_template, request
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
