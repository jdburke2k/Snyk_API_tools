import requests
import csv
from datetime import datetime
from requests.exceptions import HTTPError, ReadTimeout
import time

# Your Snyk API token
#API_TOKEN = "TOKEN"


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
csv_filename = f'snyk_issues_{timestamp}.csv'

# Retrieve a list of all organizations
orgs_url = f"{BASE_URL}orgs?from=0&to=1000"
orgs_response = requests.get(orgs_url, headers=HEADERS, timeout=30.0)
orgs_data = orgs_response.json()
org_id_list = []

for org in orgs_data['orgs']:
    org_id_list.append(org['id'])

# Data to include in the request body
data = {
    "filters": {
        "orgs": org_id_list,  # Add your organization IDs here
        "isFixed": True  # Set this to True to include fixed issues
        # "dateRange": {
        #     "from": start_date,
        #     "to": end_date
        # }
        # Include other filters as needed
    }
}

# Make the HTTP POST request and handle pagination
HAS_MORE = True
count = 0
page_num = 1
per_page = 1000
response_data = []

while HAS_MORE:
    for retry in range(max_retries):
        try:
            # Make the HTTP POST request
            response = requests.post(f'{BASE_URL}/reporting/issues/latest?page={page_num}&perPage={per_page}',
                                     headers=HEADERS, json=data, timeout=60.0)
            response.raise_for_status()  # Check for any HTTP errors
            break  # Break out of the retry loop if request successful
        except ReadTimeout as e:
            if retry < max_retries - 1:
                print(f"Read timeout occurred. Retrying in {retry_backoff} seconds...")
                time.sleep(retry_backoff)
                continue
            else:
                raise  # Raise the exception if max retries exceeded
        except HTTPError as e:
            if retry < max_retries - 1:
                print(
                    f"HTTP error occurred: {e.response.status_code} - {e.response.text}... Retrying in {retry_backoff} seconds...")
                time.sleep(retry_backoff)
                continue
            else:
                raise  # Raise the exception if max retries exceeded

    print(response.status_code)
    print(response.json())
    print(data)

    # Handle the response data
    if response.ok and response.json()['total'] > 0:
        # Initialize issues array
        issue_data_list = []
        page_data = response.json()
        issue_data_list = page_data['results']
        count = count + len(issue_data_list)
        total = page_data['total']

        # Write data to CSV file
        for item in issue_data_list:
            # Extract issue data
            issue_data = {
                'url': item['issue']['url'],
                'id': item['issue']['id'],
                'title': item['issue']['title'],
                'type': item['issue']['type'],
                'package': item['issue']['package'],
                'version': item['issue']['version'],
                'severity': item['issue']['severity'],
                'originalSeverity': item['issue']['originalSeverity'],
                'uniqueSeveritiesList': item['issue']['uniqueSeveritiesList'],
                'language': item['issue']['language'],
                'packageManager': item['issue']['packageManager'],
                'semver': item['issue']['semver'],
                'isIgnored': item['issue']['isIgnored'],
                'priorityScore': item['issue'].get('priorityScore', ''),
                'isPatchable': item['issue'].get('isPatchable', ''),
                'cloudConfigPath': item['issue'].get('cloudConfigPath', ''),
                'jiraIssueUrl': item['issue']['jiraIssueUrl'],
                'isFixed': item['isFixed'],
                'introducedDate': item['introducedDate'],
                'project_url': item['project']['url'],
                'project_id': item['project']['id'],
                'project_name': item['project']['name'],
                'source': item['project']['source'],
                'project_packageManager': item['project']['packageManager'],
                'target_file': item['project'].get('targetFile', ''),
            }
            response_data.append(issue_data)

        if count >= total:
            HAS_MORE = False
            count = total

        percent = format(count / total * 100, ".1f")
        print(f"Getting Snyk Issues... {count}/{total} ... {percent}%")
        page_num += 1
    else:
        HAS_MORE = False
        continue

# Create CSV to write Snyk Issue Data
if count != 0:
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['url', 'id', 'title', 'type', 'package', 'version', 'severity', 'originalSeverity',
                      'uniqueSeveritiesList',
                      'language', 'packageManager', 'semver', 'isIgnored', 'priorityScore', 'isPatchable',
                      'cloudConfigPath',
                      'jiraIssueUrl', 'isFixed', 'introducedDate', 'project_url', 'project_id', 'project_name',
                      'source',
                      'project_packageManager', 'target_file']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        print("Writing to CSV...")

        # Write row to CSV file
        for data in response_data:
            writer.writerow(data)

    print(f"Found {count} issues in Snyk")
    print(f"CSV file saved: {csv_filename}")
else:
    print("No issues found.")