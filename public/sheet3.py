from flask import Flask, render_template, url_for, request, redirect, session
import csv
from  math import log10


def get_soil_type():
    soil_type = list()
    for index in range(3):
        pF_input = index
        table = list()
        with open('sheet3.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                expo = (-10 ** pF_input)
                calculate = round(float(row[1]) + ((float(row[2]) - float(row[1])) / (
                        (1 + (abs(float(row[4]) * expo) ** float(row[6]))) ** (1 - 1 / float(row[6])))), 4)
                table.append([row[0], pF_input, expo, calculate, row[1], row[2], row[3], row[4], row[5], row[6]])
        soil_type.append(table)
    return soil_type

def get_oh_by_pF(pF_input, b_value='B1'):
    calculate = 0
    with open('sheet3.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if (row[0] == b_value):
                expo = (-10 ** pF_input)
                calculate = round(float(row[1]) + ((float(row[2]) - float(row[1])) / (
                    (1 + (abs(float(row[4]) * expo) ** float(row[6]))) ** (1 - 1 / float(row[6])))), 4)
    return calculate


def get_pf_at_oact(oact, b_value='B1'):
    calculate = 0
    with open('sheet3.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

        for row in spamreader:
            if (row[0] == b_value):
                f4 = float(row[2])
                e4 = float(row[1])
                j4 = float(row[6])
                h4 = float(row[4])
                calculate = (((f4 - e4) / (oact - e4)) ** (j4 / (j4 - 1)) - 1) ** (1 / j4) / abs(h4)
                break
    print(round(calculate))
    pf = log10(round(calculate))
    return round(pf, 1)


def get_soil_type_by_pf(pF_input, b_value='B1'):
    with open('sheet3.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            expo = (-10 ** pF_input)
            calculate = round(float(row[1]) + ((float(row[2]) - float(row[1])) / (
                    (1 + (abs(float(row[4]) * expo) ** float(row[6]))) ** (1 - 1 / float(row[6])))), 4)
            if (row[0] == b_value):
                return calculate
    return 1


def sheet3():
    soil_type = get_soil_type()
    return render_template('sheet3.html',
                           data={"soil_type": enumerate(soil_type)})
