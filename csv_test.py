from flask import Flask, render_template, request
import smtplib
from flaskFeature import main

def parse_csv(csv_location):
    import pandas as pd
    df = pd.read_csv(csv_location)
    df = df[['First Name', 'Last Name', 'E-mail Address', 'Company', 'Job Title']]
    return [df[x].tolist() for x in df]

result = parse_csv('linkedin_connections_export.csv')

for j in range(len(result[0])):
    for i in range(len(result)):
        print(result[i][j])
    print("")
