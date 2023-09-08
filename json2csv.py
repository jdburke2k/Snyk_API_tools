#
# Snyk helper code.
# Author: JD Burke
#
# Best effort - No promises, help or guarantees should be read into this or expected.
# If you don't like what it does...build your own, or modify the stuff below.
#
# What it does:
# Takes the file - bitbucket-cloud-import-targets.json and extracts specific info to help mod other files later
# Only works for a specific file with a specific format...so it is very brittle and essentially hardcoded.
#
# the end result will be a csv of the BB workspaces, repos and their branches
#
import json
import csv

# Opening JSON file and loading the data
with open('bitbucket-cloud-import-targets.json') as json_file:
    data = json.load(json_file)

bb_data = data['targets']

# Open a csv file for writing
data_file = open('bitbucket-cloud-import-targets.csv', 'w')
csv_writer = csv.writer(data_file)

count = 0
for repo in bb_data:
    if count == 0:
        # Writing headers of CSV file
        header = repo.keys()
        csv_writer.writerow(header)
        count += 1

    csv_writer.writerow(repo.values())

data_file.close()