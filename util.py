import json

# serialize data into json file
def save(data):
    dic = buildDic(data)
    with open('meldungen.json', 'w') as f:
        json.dump(dic, f)


# build a dictionary from data array
def buildDic(data):
    d = dict()
    d['name'] = data[0]
    d['meldung'] = data[1]
    return d