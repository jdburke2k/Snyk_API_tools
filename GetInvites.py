#
# Snyk helper code.
# Author: JD Burke
#
# Best effort - No promises, help or guarantees should be read into this or expected.
# If you don't like what it does...build your own, or modify the stuff below.
#
# What it does:
# Takes a Group ID and API token and dumps info for the orgs of that group, specifically email invites
# dumps data to console, a json file and a csv file
#
#
#
import requests
import json
import csv
import time

# # Your Snyk API token
# API_TOKEN = "your-api-token-here"
#
# # Your Group ID
# GROUP_ID = "your-group-token-here"

#JDB group service
API_TOKEN = "yourtoken"
#JDB Corp group id
GROUP_ID = "yourgroupid"
#Goof ltd
#GROUP_ID = "yourgroupid"

BASE_URL = "https://api.snyk.io/rest/"
VERSION_STR = "version=2023-06-22"

# Headers for Snyk API requests
HEADERS = {
    "Authorization": f"token {API_TOKEN}",
    "Content-Type": "application/json",
}
#
# gets info for whatever Group ID you used
group_url = f"{BASE_URL}groups?version=2023-06-22~beta"
group_response = requests.get(group_url, headers=HEADERS, timeout=30.0)
group_data = group_response.json()

for orgs in group_data['data']:
    print(orgs['attributes']['name']+"  ["+orgs['id']+"]")
# gets info about the orgs in the Group ID
    orgs_url = f"{BASE_URL}orgs?{VERSION_STR}"
    orgs_response = requests.get(orgs_url, headers=HEADERS, timeout=30.0)
    orgs_data = orgs_response.json()

    myJSON = []
    for org in orgs_data['data']:
        org_names = org['attributes']['name']
        print("\t"+org['attributes']['name']+"  ["+org['id']+"]")
# gets detail info for the org
        org_url = BASE_URL+"orgs/"+org['id']+"/invites?"+VERSION_STR
        org_response = requests.get(org_url, headers=HEADERS, timeout=30.0)
        org_data = org_response.json()
        myJSON.extend(org_data['data'])

        for name in org_data['data']:
            print('\t\t'+name['attributes']['email'])
        print()

    timestr = time.strftime('%Y%m%d-%H%M%S')
    fnout = 'Snyk-GetInvites-' + timestr
    with open(fnout + '.json', 'w') as f:
        json.dump(myJSON, f)
        # Open a csv file for writing
        data_file = open(fnout + '.csv', 'w')
        csv_writer = csv.writer(data_file)

        count = 0
        for i in myJSON:
            if count == 0:
                # Writing headers of CSV file
                header = i.keys()
                csv_writer.writerow(header)
                count += 1

            csv_writer.writerow(i.values())

        data_file.close()
