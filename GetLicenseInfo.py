#
# Snyk helper code.
# Author: JD Burke
#
# Best effort - No promises, help or guarantees should be read into or expected from this work.
# If you don't like what it does, or how it does it...roll your own, or modify the stuff below.
#
# What it does:
# POST to an endpoint to pull back list of licenses from SOS and writes them to a CSV
#
# TODO: make the json extraction data driven which means some crafty myCol handling
# TODO: add a file path function...whatever that py package was...
# TODO: make the file write a function
# TODO: make the Authorization and orgID system variables
#
import requests
import json
import jmespath
import csv
import time

# AuthToken = 'your-auth-token-goes-here'
# orgId = 'your-orgid-goes-here'
#AuthToken = 'your-token-here'
#orgId = 'your-org-id-goes-here'


headers = {
  'Content-Type': 'application/json',
  'Authorization': '' + AuthToken + ''''''
}

baseurl = 'https://api.snyk.io/api/v1/org/' + orgId
url = baseurl + '/licenses'

# from the API doc but I don't know what it does or if we actually will ever use it
values = {
}

try:
    response = requests.post(url, headers=headers, timeout=5)
    # print(response)
    # print(response.content)
    # print(response.text)
    # print(response.json)
    response.raise_for_status()

# do stuff if the request is successful
# convert from byte to json >> not sure why we return bytes but simple enough to fix
    myresponse = json.loads(response.content.decode('utf-8'))
    # print(myresponse)

# prettify the json if you want/need
    # myresponse = json.dumps(myresponse, indent=2)
    # print(myresponse)

# find selected values in the json https://jmespath.org/tutorial.html
    myCols = ['ID', 'Severity']
    myRows = jmespath.search('results[].[id,severity]', myresponse)
    # print(myRows)

# Write a file with a timestamped file name
    timestr = time.strftime('%Y%m%d-%H%M%S')
    with open('Snyk-License-' + timestr + '.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(myCols)
        write.writerows(myRows)

except requests.exceptions.HTTPError as errh:
    print(errh)
except requests.exceptions.ConnectionError as errc:
    print(errc)
except requests.exceptions.Timeout as errt:
    print(errt)
except requests.exceptions.RequestException as err:
    print(err)
