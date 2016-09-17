#!/usr/bin/env python
import requests
import re
import time
from sklearn import linear_model
import numpy as np
import string


def search_niacs(search):
    url = "https://www.naics.com/naics-search-results/"
    r = requests.post(url, data={'words': search})
    text = r.text
    marker = "<a href='https://www.naics.com/naics-code-description/?code="
    occurances = [m.start() + len(marker) for m in re.finditer(re.escape(marker), text)]

    results = []
    for start in occurances:
        code = ""
        j = ""
        i = start
        while j != "'":
            code += j
            j = text[i]
            i += 1
        results.append(code)
    return sorted(list(set(results)))


def complex_search(search):
    basic = search_niacs(search)
    if basic:
        return basic

    words = search.split()

    D = {}
    for word in words:
        D[word] = search_niacs(word)

    words_to_subtract = -1
    while words[:words_to_subtract]:
        overall_set = set(D[words[0]])
        for s in words[1:words_to_subtract]:
            overall_set &= set(D[s])

        if overall_set:
            return sorted(list(overall_set))
        words_to_subtract -= 1

    all = {}
    for s in D:
        all |= set(D[s])

    return sorted(list(all))


def starting_salary(job):
    marker = 'class="salary">$'
    link = "http://www.indeed.com/salary?q1=" + job.replace(" ", "+") + "&l1=&tm=1"
    r = requests.get(link)
    text = r.text
    occurances = [m.start() + len(marker) for m in re.finditer(re.escape(marker), text)]

    results = []
    for start in occurances:
        code = ""
        j = ""
        i = start
        while j != " ":
            code += j
            j = text[i]
            i += 1
        results.append(code)
    return results[0].replace(",", "")


def predictGrowth(file, industryNums, quartersAhead):
    dicts_from_file = []
    with open(file, 'r') as inf:
        dicts_from_file = eval(inf.read())

    current = []
    predictions = []

    for v in industryNums:
        try:
            industryData = dicts_from_file[v]
        except:
            continue
        gT = industryData[:-1]
        trainingData = np.array([np.arange(len(gT))]).T

        myModel = linear_model.LassoCV()
        myModel.fit(trainingData, gT)
        futureDate = len(gT) + quartersAhead
        current.append(gT[-1])
        predictions.append(myModel.predict(futureDate)[0])

    if not current:
        raise ArithmeticError
    avgCur = np.average([int(x) for x in current])
    avgPred = np.average(predictions)

    return avgPred / avgCur - 1


def predictions(industryNums):
    timesToPredict = [4, 20, 40]

    # salary
    salaryPreds = []
    for v in timesToPredict:
        nextPred = predictGrowth('average_weekly_salary_dict.txt', industryNums, v)
        salaryPreds.append(nextPred)

    # employment
    employmentPreds = []
    for v in timesToPredict:
        nextPred = predictGrowth('employment_dict.txt', industryNums, v)
        employmentPreds.append(nextPred)

    return salaryPreds, employmentPreds


def create_rank(naics_predictions, salary):
    salary = int(salary)
    salaryPreds = naics_predictions[0]
    weight = 0.325
    weighted_salary = salary * weight
    for i in range(3):
        weight -= 0.05
        weighted_salary += salary * salaryPreds[i] * weight
    growthPreds = naics_predictions[1]
    composite_score = weighted_salary + weighted_salary * growthPreds[1]**2
    return composite_score


def main(job_title):
    salary = int(starting_salary(job_title))
    naics = complex_search(job_title)
    #print(naics)
    #print(salary)

    naics_predictions = predictions(naics)
    #print(naics_predictions)
    return create_rank(naics_predictions, salary), salary, naics_predictions



"""
with open("/Users/jtstog/linkedin_export.csv") as file:
    csv = [[a.replace('"',"") for a in x.strip().split(",")] for x in file.readlines()]

job_summaries = []
exclude = set(string.punctuation)

progress = 0
for row in csv:
    progress += 1
    print(progress)
    job_title = row[31]
    if not row[31]:
        continue
    job_title = ''.join(ch for ch in job_title if ch not in exclude)
    print(job_title)
    try:
        summary = [row[1], row[3], row[29], row[31], main(row[31])]
        job_summaries.append(summary)
        print(summary)
    except:
        time.sleep(0.5)
"""
