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
import time

# AuthToken = 'token your-auth-token-goes-here'
# orgId = '"your-orgid-goes-here-between-the-double-quotes"'



headers = {
  'Content-Type': 'application/json',
  'Authorization': '' + AuthToken + ''''''
}

values = """
  {
    "filters": {
      "orgs": [""" + orgId + """],
      "severity": [
        "critical",
        "high",
        "medium",
        "low"
      ],
      "exploitMaturity": [
        "mature",
        "proof-of-concept",
        "no-known-exploit",
        "no-data"
      ],
      "types": [
        "vuln",
        "license",
        "configuration"
      ],
      "languages": [
        "node",
        "javascript",
        "ruby",
        "java",
        "scala",
        "python",
        "golang",
        "php",
        "dotnet",
        "swift-objective-c",
        "elixir",
        "docker",
        "linux",
        "dockerfile",
        "terraform",
        "kubernetes",
        "helm",
        "cloudformation",
        "arm"
      ],
      "projects": [],
      "issues": [],
      "identifier": "",
      "ignored": false,
      "patched": false,
      "fixable": false,
      "isFixed": false,
      "isUpgradable": false,
      "isPatchable": false,
      "isPinnable": false,
      "priorityScore": {
        "min": 0,
        "max": 1000
      }
    }
  }
"""

# There are two flavors of Snyk API's loose in the wild with plug differences. Be mindful...
# baseurl = 'https://api.snyk.io/api/v1/org/' + orgId
# url = baseurl + '/licenses'
#
baseurl = 'https://api.snyk.io/api/v1/'
url = baseurl + 'reporting/issues/latest'

# This is currently set up only for POST endpoints. Be mindful...
try:
    # print(values)
    response = requests.post(url, headers=headers, data=values, timeout=5)
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
    myresponse = json.dumps(myresponse, indent=2)
    # print(myresponse)

# Write a file with a timestamped file name
    timestr = time.strftime('%Y%m%d-%H%M%S')
    with open('Snyk-Issues-' + timestr + '.json', 'w') as f:
        f.write(myresponse)

except requests.exceptions.HTTPError as errh:
    print(errh)
except requests.exceptions.ConnectionError as errc:
    print(errc)
except requests.exceptions.Timeout as errt:
    print(errt)
except requests.exceptions.RequestException as err:
    print(err)
