#
# Snyk helper code.
# Author: JD Burke
#
# Best effort - No promises, help or guarantees should be read into this or expected.
# If you don't like what it does...build your own, or modify the stuff below.
#
# What it does:
# Takes two input files:
#   csv file, typically from a Snyk json that has been flattened into a csv for modifying
#   a json output file name
#
# Steps through the csv and builds a json then saves the json to the file name given
#
# expects line 1 of the csv to have a comma separated list of field names (keys). The subsequent lines are the values
# for those keys
#
import csv
import json


def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []

    # read csv file
    with open(csvFilePath, encoding='utf-8') as csvf:
        # load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf)

        # convert each csv row into python dict
        for row in csvReader:
            # add this python dict to json array
            jsonArray.append(row)

    # convert python jsonArray to JSON String and write to file
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)


csvFilePath = r'testdata.csv'
jsonFilePath = r'testdata.json'
csv_to_json(csvFilePath, jsonFilePath)