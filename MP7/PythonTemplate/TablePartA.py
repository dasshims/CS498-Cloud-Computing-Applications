import happybase as hb

connection = hb.Connection('localhost')
connection.open()

powers = {
    'personal': dict(),
    'professional': dict(),
    'custom': dict()
}

connection.create_table('powers', powers)

food = {
    'nutrition': dict(),
    'taste': dict()
}

connection.create_table('food', powers)