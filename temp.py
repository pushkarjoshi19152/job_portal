import json
print('\n\n\n\n')
with open('data.json', 'r+') as data:
    temp = json.load(data)
    ls = []
    for item in temp['jobs']:
        ls.append(item.lower())

    temp['jobs'] = ls
    json.dump(temp, data)

print('\n\n\n\n')
with open('data1.json', 'r+') as data:
    temp = json.load(data)
    ls = []
    for item in temp['cities']:
        ls.append(item.lower())
    temp['cities'] = ls
    json.dump(temp, data)
