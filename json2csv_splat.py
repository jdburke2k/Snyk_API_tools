import json
import csv

# Opening JSON file and loading the data
with open('snyk-created-orgs.json') as json_file:
    data = json.load(json_file)

bb_data = data['orgData']

# Open a csv file for writing
data_file = open('snyk-created-orgs.csv', 'w')
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