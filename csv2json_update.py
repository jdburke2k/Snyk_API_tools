#
# Snyk helper code.
# Author: JD Burke
#
# Best effort - No promises, help or guarantees should be read into this or expected.
# If you don't like what it does...build your own, or modify the stuff below.
#
# What it does:
# Takes two input files:
#   <bitbucket>-cloud-import-targets.json from the running of the snyk-api-import tool step (3?)
#   <bitbucket>-cloud-import-targets.csv from the running of the json2csv.py tool (which rips selected bits of
#       <bitbucket>-cloud-import-targets.json to csv for mod-ing
#
# Steps through the json and updates the orgId in the json with whatever is in the csv orgId
#
# Only works for orgId. Only works with set csv column orders...so it is very brittle and essentially hardcoded.
#
import json
import csv

def csv_to_json(csv_file_in, json_file_out):
# Open the json file that is to be modified
    with open(json_file_out, encoding='utf-8-sig') as myjson:
        mydata = json.load(myjson)
        for repo in mydata['targets']:
            myrepo = repo['target']
            # open the csv file with the modifications
            with open(csv_file_in, encoding='utf-8-sig') as csvf:
                mycsv = csv.DictReader(csvf)
                # step through the csv for this sub-item in the json and replace the v of k if the index matches
                for row in mycsv:
                    if str(myrepo) == list(row.values())[0]:
                        repo['orgId'] = list(row.values())[2]
#  write out the new json data to the old json file
# TODO: add the timestamp code to the file name so this is not a destructive action
#
    with open(json_file_out, 'w', encoding='utf-8') as jsonf:
        jsonstring = json.dumps(mydata, indent=4)
        jsonf.write(jsonstring)

# The input csv and json files
# TODO: add some notes about file formats and how to create
#
# Write a file with a timestamped file name
#    timestr = time.strftime('%Y%m%d-%H%M%S')
#    with open('Snyk-License-' + timestr + '.csv', 'w') as f:
#        write = csv.writer(f)
#        write.writerow(myCols)
#        write.writerows(myRows)

# TODO: put these in a config file or something...or maybe with some sort of ui/input
csv_file_path = r'bitbucket-cloud-import-targets.csv'
json_file_path = r'bitbucket-cloud-import-targets.json'

csv_to_json(csv_file_path, json_file_path)