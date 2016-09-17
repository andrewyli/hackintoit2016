from flask import Flask, render_template
app = Flask(__name__)

def parse_csv(csv_location):
    import pandas as pd
    df = pd.read_csv(csv_location)
    df = df[['First Name', 'Last Name', 'E-mail Address', 'Company', 'Job Title']]
    return [df[x].tolist() for x in df]

connections = parse_csv('linkedin_connections_export.csv')

@app.route("/")
def hello_world(name=None):
    return render_template("index.html", name=name)
