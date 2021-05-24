# CloudFlare API Gateway https://api.cloudflare.com/client/v4/
# IP returns from http://myip.ipip.net/
import requests
import json

# Global Settings
apiToken = 'fD_*************************'
targetDomain = 'example.com'
DNSRecordName = 'go.example.com'

# Get IP Address
myipReturn = requests.get('http://myip.ipip.net/')
ip = myipReturn.text[6:20]

# DEBUG Space detector
# print(ip + 'a')

# load Zones Info
zonesRaw = requests.get('https://api.cloudflare.com/client/v4/zones?name='+targetDomain, headers={'Authorization':'Bearer '+apiToken})
zonesID = zonesRaw.json()['result'][0]['id']

DNSRecordRaw = requests.get('https://api.cloudflare.com/client/v4/zones/'+zonesID+'/dns_records?name='+ DNSRecordName, headers={'Authorization':'Bearer '+apiToken})
recordID = DNSRecordRaw.json()['result'][0]['id']
recordType = DNSRecordRaw.json()['result'][0]['type']
recordName = DNSRecordRaw.json()['result'][0]['name']
recordTTL = DNSRecordRaw.json()['result'][0]['ttl']

#Update
Updates={'type': recordType, 'name': recordName, 'content': ip, 'ttl': recordTTL}
requests.put('https://api.cloudflare.com/client/v4/zones/'+zonesID+'/dns_records/'+recordID, headers={'Authorization':'Bearer '+apiToken, 'Content-Type':'application/json'}, data=json.dumps(Updates))
