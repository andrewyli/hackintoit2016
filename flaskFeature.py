#!/usr/bin/env python
import requests
import re
import time
from sklearn import linear_model
import numpy as np


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
        industryData = dicts_from_file[v]
        gT = industryData[:-1]
        trainingData = np.array([np.arange(len(gT))]).T

        myModel = linear_model.LassoCV()
        myModel.fit(trainingData, gT)
        futureDate = len(gT) + quartersAhead
        current.append(gT[-1])
        predictions.append(myModel.predict(futureDate)[0])

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

    return (salaryPreds, employmentPreds)


def create_rank(naics_predictions, salary):
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
    try:
        salary = starting_salary(job_title)
    except:
        time.sleep(1)
        salary = starting_salary(job_title)

    try:
        naics = complex_search(job_title)
    except:
        time.sleep(1)
        naics = complex_search(job_title)

    naics_predictions = predictions(naics)
    return create_rank(naics_predictions, salary), salary, naics_predictions