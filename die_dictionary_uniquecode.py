import pandas as pd

# Forging Die Generation
elementList = ['UPT', 'UPB', 'BLT', 'BLB', 'FIT', 'FIB', 'TRD', 'TRP', 'PRP', 'PDT', 'PDB', 'STP']

dieNo = ['244', '644', '654', '699', '1161', '1168', '1169', '1267', '1364', '1378', '1396', '1432', '1440',
         '1458', '1483', '1502', '1557', '1559', '1560', '1574', '1602', '1610', '1624', '1632', '1641', '1642',
         '1643', '1660', '1756', '1757', '1758', '1772', '1784', '1785', '1803', '1223', '1225', '1226', '1775', '1753',
         '1450', '1294']

len(dieNo)
# Create a set of 5 dies for each element
dieElement = []
for die in dieNo:
    for element in elementList:
        for x in range(0, 5):
            list_type = [die, element]
            dieElement.append(list_type)


# Key List Generation
keyList = []
for i in range(0, len(dieElement)):
    i = f'{i:05}'
    keyList.append(i)

# Create a Dictionary from List
dieDict = dict(zip(keyList, dieElement))
for key, value in dieDict.items():
    pass
    # print(key, value)

# Hatebur Unique Code Generation
hateburDie = ['188', '189', '237', '243', '244', '245', '1154', '1155',
              '1157', '1159', '1178', '1290', '1529', '1660']

hateburElements = ['Upset Plate', 'Upset Punch', '1st Punch', '2nd Punch', '3rd Punch', '4th Punch',
                   '1st Ring Die', '1st Die', '1st Ejector', '2nd Ring Die', '2nd Die', '2nd Ejector',
                   '3rd Ring Die', '3rd Die', '3rd Ejector', 'Piercing Die']

hateburDieElement = []
for die in hateburDie:
    for element in hateburElements:
        for x in range(0, 10):
            list_type = [die, element]
            hateburDieElement.append(list_type)

# print(len(hateburDieElement))

# for x in hateburDieElement:
#     print(x)

hateburKey = []
for i in range(7000, 9240):
    i = f'{i:05}'
    hateburKey.append(i)

hateburDict = dict(zip(hateburKey, hateburDieElement))

for key, value in hateburDict.items():
    pass
    # print(key, value)

uniquecodeDict = dieDict | hateburDict

for key, value in uniquecodeDict.items():
    pass
    # print(key, value)


df = pd.DataFrame(uniquecodeDict)
df.T.to_excel('Unique Code Dict.xlsx')
