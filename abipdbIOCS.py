#https://docs.abuseipdb.com/?python#reports-parameters
#https://docs.abuseipdb.com/?python#blacklist-country-filtering

import requests
import json
import pandas as pd
import csv

# Defining the api-endpoint
url = 'https://api.abuseipdb.com/api/v2/blacklist'

#Confidence Score
querystring = {
    'confidenceMinimum':'80',
    'maxAgeInDays':'90',
    'onlyCountries':'US,MX,CA'
}

#headers with API Key
headers = {
    'Accept': 'application/json',
    'Key': 'xxxxxxxxxxxxxx'
}

#GET and make json
response = requests.request(method='GET', url=url, headers=headers, params=querystring)
r = response.json()

#Create dictionary
dictionary = r

#JSON Dictonary dump
json_object = json.dumps(dictionary, indent=4)

#Create JSON File
with open('/home/user/pythonflask1/sample1.json', "w") as outfile:
	outfile.write(json_object)

# Read JSON
with open('/home/user/pythonflask1/sample1.json') as inputfile:
  data = json.load(inputfile)  

# Extract values
values_list = data.get('data', [])

# Normalize nested values
df = pd.json_normalize(data['data'])

# Extract desired fields
selected_columns = [
    'abuseConfidenceScore', 
    'countryCode', 
    'ipAddress',
    'lastReportedAt',
]
df_selected = df[selected_columns]


#Create CSV.
df.to_csv('apdb.csv', mode='a', index=False, header=False) 
print("Values have been added. Please check the output.csv file.")


#Dedup CSV
data = pd.read_csv('apdb.csv')

ddata = data.drop_duplicates()

#Define Headers
hl = ['IP', 'Country', 'Score', 'DateAdded' ]

#Create new csv
ddata.to_csv('apdb.csv', header=hl, index=False)
print("CSV successfully deduplicated")
