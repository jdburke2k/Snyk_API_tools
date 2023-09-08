import json
import csv

def csv_to_json(csv_file_in, json_file_out):
    myarray =[]
    test = {'orgtest':{'name':0, 'orgId':0,'bitbucket-server':0}}
    test2 = {}

    with open(csv_file_in, encoding='utf-8-sig') as csvf:
        mycsv = csv.DictReader(csvf)

        for row in mycsv:
            #making a list
            myarray.append(row)
            row.popitem()
            tmpints = row.popitem()
            mykv = {tmpints[0]:tmpints[1]}
            row.update({'integrations':mykv})
        myarray = {'orgData':myarray}
    #for key in myarray:
     #   for k in myarray[key]:
      #      for i in k['integrations']:
                #print(i)

    with open(json_file_out, 'w', encoding='utf-8-sig') as jsonf:
        jsonstring = json.dumps(myarray, indent=4)
        jsonf.write(jsonstring)


csv_file_path = r'BBBook1.csv'
json_file_path = r'BB_OrgData_1.json'

csv_to_json(csv_file_path, json_file_path)