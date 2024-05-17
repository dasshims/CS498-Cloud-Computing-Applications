import happybase as hb

# DON'T CHANGE THE PRINT FORMAT, WHICH IS THE OUTPUT
# OR YOU WON'T RECEIVE POINTS FROM THE GRADER

# color = ???
# name = ???
# power = ???
#
# color1 = ???
# name1 = ???
# power1 = ???
#
# print('{}, {}, {}, {}, {}'.format(name, power, name1, power1, color))

connection = hb.Connection('localhost')
connection.open()

# Retrieve a table
table = connection.table("powers")

# Scan the data in the table
scanner = table.scan()

results = {}

# Scan the data and store unique rows based on names (key)
for key, data in table.scan():
    name = data[b'professional:name']
    if name not in results:
        results[name] = {
            "power": data[b'personal:power'],
            "color": data[b'custom:color']
        }

# Perform JOIN using the stored results
for name, info in results.items():
    for other_name, other_info in results.items():
        if name != other_name and info["color"] == other_info["color"]:
            print('{}, {}, {}, {}, {}'.format(name, info["power"], other_name, other_info["power"], info["color"]))