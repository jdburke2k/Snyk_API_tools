import requests
import csv
from datetime import datetime

# Your Snyk API token
API_TOKEN = "TOKEN"
# Snyk API group URL
#API_TOKEN = "TOKEN"

#JDB Corp group id
#GROUP_ID = "yourgroupid"


# Specify the start and end dates
start_date = datetime(2018, 1, 1).isoformat()
end_date = datetime(2023, 5, 31).isoformat()

# Snyk API base URL
BASE_URL = "https://snyk.io/api/v1/"
BASE_URL3 = "https://api.snyk.io/rest/"

# Headers for Snyk API requests
HEADERS = {
    "Authorization": f"token {API_TOKEN}",
    "Content-Type": "application/json",
}

# Retry configuration
max_retries = 3
retry_backoff = 3  # seconds

# Generate timestamp string and csv file name
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Retrieve a list of all organizations
group_url = f"{BASE_URL}group/{GROUP_ID}/orgs"
groups_response = requests.get(group_url, headers=HEADERS, timeout=30.0)
#add some logging to see what is coming back from groups_response
#if goofy then look at pagination
groups_data = groups_response.json()
org_id_list = []
pmbrs_id_list = []

for org in groups_data['orgs']:
    org_id_list.append(org['id']+', '+org['name'])

    mbrs_url = f"{BASE_URL}org/{org['id']}/members?includeGroupAdmins=true"
    mbrs_response = requests.get(mbrs_url, headers=HEADERS, timeout=30.0)
    mbrs_data = mbrs_response.json()

    pmbrs_url = f"{BASE_URL3}orgs/{org['id']}/invites?version=2023-04-28"
    pmbrs_response = requests.get(pmbrs_url, headers=HEADERS, timeout=30.0)
    pmbrs_data = pmbrs_response.json()
#    pmbrs_id_list = []

    myJson = {}
    myJson['id'] = org['id']
    myJson['name'] = org['name']
    myPend = {}
    myList = []

    if pmbrs_data['data']:
        for item in pmbrs_data['data']:
            myList.append(item['attributes'])
    myJson['data'] = myList
    pmbrs_id_list.append(myJson)

#print(pmbrs_id_list)
#print(org_id_list)

# Open a csv file for writing member data
csv_filename = f'snyk_mbrs_{timestamp}.csv'
data_file = open(csv_filename, mode='w', newline='', encoding='utf-8')
csv_writer = csv.writer(data_file)

count = 0
for repo in mbrs_data:
    if count == 0:
        # Writing headers of CSV file
        header = repo.keys()
        csv_writer.writerow(header)
        count += 1

    csv_writer.writerow(repo.values())

data_file.close()

# Open a csv file for writing Pending member data
csv_filename = f'snyk_Pmbrs_{timestamp}.csv'
data_file = open(csv_filename, mode='w', newline='', encoding='utf-8')
csv_writer = csv.writer(data_file)

count = 0
for repo in pmbrs_id_list:
    if count == 0:
        # Writing headers of CSV file
        header = repo.keys()
        csv_writer.writerow(header)
        count += 1

csv_writer.writerow(pmbrs_id_list)

data_file.close()
