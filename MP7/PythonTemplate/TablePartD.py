import happybase as hb

# DON'T CHANGE THE PRINT FORMAT, WHICH IS THE OUTPUT
# OR YOU WON'T RECEIVE POINTS FROM THE GRADER
connection = hb.Connection('localhost')
connection.open()

table = connection.table('powers')

row = table.row('row1')
# hero = ???
# power = ???
# name = ???
# xp = ???
# color = ???
hero = row[b'personal:hero']
power = row[b'personal:power']
name = row[b'professional:name']
xp = row[b'professional:xp']
color = row[b'custom:color']

print('hero: {}, power: {}, name: {}, xp: {}, color: {}'.format(hero, power, name, xp, color))

# hero = ???
# color = ???
row = table.row('row19')

hero = row[b'personal:hero']
color = row[b'custom:color']

print('hero: {}, color: {}'.format(hero, color))

# hero = ???
# name = ???
# color = ???
row = table.row('row1')

hero = row[b'personal:hero']
name = row[b'professional:name']
color = row[b'custom:color']
print('hero: {}, name: {}, color: {}'.format(hero, name, color))
