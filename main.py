#
# Snyk helper code.
# Author: JD Burke
#
# Best effort - No promises, help or guarantees should be read into this or expected.
# If you don't like what it does...build your own, or modify the stuff below.
#
# What it does:
#
#
import requests
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'yourbearer'
}

orgId = "yourid"

values = {

}

#url = "http://api.open-notify.org/astros.json"
url = "https://api.snyk.io/api/v1/org/"+orgId+"/licenses"
#request = requests(url, data=values, headers=headers)
try:
    response = requests.post(url, headers=headers, timeout=5)
    response.raise_for_status()
    # do stuff if the request is successful
    # print(response)
    print(response.content)
    # print(response.text)
    # print(response.json)
except requests.exceptions.HTTPError as errh:
    print(errh)
except requests.exceptions.ConnectionError as errc:
    print(errc)
except requests.exceptions.Timeout as errt:
    print(errt)
except requests.exceptions.RequestException as err:
    print(err)
