import json
from pprint import pprint

f = open('./data/devices.json')
file_contents = f.read()
data = json.loads(file_contents)
f.close()

names = [obj['name'] for obj in data]

pprint(names)