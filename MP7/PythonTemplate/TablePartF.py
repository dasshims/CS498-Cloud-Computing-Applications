import happybase as hb

# DON'T CHANGE THE PRINT FORMAT, WHICH IS THE OUTPUT
# OR YOU WON'T RECEIVE POINTS FROM THE GRADER

# 1. update the data in a particular cell using the put() method
# 2. retrieve all versions of all columns, with the most recent version coming first

connection = hb.Connection('localhost')
connection.open()

table = connection.table('powers')

# Row key for the row to update
row_key = 'row7'

# Update the data in a particular cell
table.put(row_key, {'custom:color': 'purple'})

row = table.row(row_key, include_timestamp=True)
for column_family, data in row.items():
    #print(f"{column_family} ::: {data}")

    value, timestamp = data
    if column_family == b'custom:color':
        cells = table.cells(row=row_key, column='custom:color', versions=2, include_timestamp=True)
        #print(f"cells {cells}")
        for color, timestamp_inner in cells:
            ##print(f"color {color}")
            print("row: {}, column family:qualifier: {}, value: {}, timestamp: {}".format(row_key.encode('ascii'), column_family, color, timestamp_inner))
    else:
        print("row: {}, column family:qualifier: {}, value: {}, timestamp: {}".format(row_key.encode('ascii'), column_family, value, timestamp))
