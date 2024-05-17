import json
import sys
import logging
import redis
import pymysql
import base64


# TODO 1
DB_HOST = "mp6-aurora.cluster-cn4umkoes8ke.us-east-1.rds.amazonaws.com" # Add DB end point
DB_USER = "admin" # Add your database user
DB_PASS = "nitashree27" # Add your database password
DB_NAME = "mp6" # Add your database name
DB_TABLE = "mp6data" # Add your table name
REDIS_URL = "redis://mp6-redis-cluster-001.elhtem.0001.use1.cache.amazonaws.com:6379" # Add redis end point "redis://<end point>"

TTL = 60

class DB:
    def __init__(self, **params):
        params.setdefault("charset", "utf8mb4")
        params.setdefault("cursorclass", pymysql.cursors.DictCursor)

        self.mysql = pymysql.connect(**params)

    def query(self, sql):
        with self.mysql.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def record(self, sql, values):
        with self.mysql.cursor() as cursor:
            insert_res = cursor.execute(sql, values)
            print(f"insert res {insert_res}")
            self.mysql.commit();
            return cursor.fetchone()

    def get_idx(self, table_name):
        with self.mysql.cursor() as cursor:
            cursor.execute(f"SELECT MAX(id) as id FROM {table_name}")
            idx = str(cursor.fetchone()['id'] + 1)
            return idx

    def insert(self, idx, data, table_name):
        with self.mysql.cursor() as cursor:
            hero = data["hero"]
            power = data["power"]
            name = data["name"]
            xp = data["xp"]
            color = data["color"]

            sql = f"INSERT INTO {table_name} (`id`, `hero`, `power`, `name`, `xp`, `color`) VALUES ('{idx}', '{hero}', '{power}', '{name}', '{xp}', '{color}')"
            print(f"sql is {sql}")
            cursor.execute(sql)
            self.mysql.commit()

 # TODO 2
def read(use_cache, xps, Database, Cache):
    # Implement Lazy Loading strategy

    result = []
    print(f"use case is {use_cache}")
    if use_cache:  # Use cache
        for xp in xps:
            data = Cache.get(xp)
            if data:
                result.append(json.loads(data))
            else:
                # If data is not found in cache, fetch from database
                db_result = Database.query(f"SELECT * FROM {DB_TABLE} WHERE xp = '{xp}'")
                if db_result:
                    result.append(db_result[0])
                    Cache.set(xp, json.dumps(db_result[0]), ex=TTL)
    else:  # Do not use cache
        for xp in xps:
            db_result = Database.query(f"SELECT * FROM {DB_TABLE} WHERE xp = '{xp}'")
            #print(f"db_result -- {db_result}")
            if db_result:
                result.append(db_result[0])

    print(f"Result before returning -- {result}")
    return result


# TODO 3
def write(use_cache, sqls, Database, Cache):
    # Implement Write Through strategy

    if use_cache:  # Use cache
        for data in sqls:
            idx = Database.get_idx(DB_TABLE)
            Database.insert(idx, data, DB_TABLE)
            Cache.set(data['xp'], json.dumps(data), ex=TTL)
    else:  # Do not use cache
        for data in sqls:
            idx = Database.get_idx(DB_TABLE)
            Database.insert(idx, data, DB_TABLE)


def lambda_handler(event, context):
    print(event)
    body = event["body"]
    if event["isBase64Encoded"]:
        body = json.loads(base64.b64decode(body))
    else:
        body = json.loads(body)

    print(f"body --- {body}")
    USE_CACHE = (body['USE_CACHE'] == "True")
    REQUEST = body['REQUEST']

    # Initialize database
    try:
        Database = DB(host=DB_HOST, user=DB_USER, password=DB_PASS, db=DB_NAME)
    except pymysql.MySQLError as e:
        print("ERROR: Unexpected error: Could not connect to MySQL instance.")
        print(e)
        sys.exit()

    # Initialize cache
    Cache = redis.Redis.from_url(REDIS_URL)

    result = []
    if REQUEST == "read":
        # event["SQLS"] is a list of all xps for which you have to query the database or redis.
        result = read(USE_CACHE, body["SQLS"], Database, Cache)
        print(f"result --- {result}")

    elif REQUEST == "write":
        # event["SQLS"] should be a list of jsons. You have to write these rows to the database.
        write(USE_CACHE, body["SQLS"], Database, Cache)
        result = "write success"
        print(f"result --- {result}")

    return_json = {
        'statusCode': 200,
        'body': result
    }
    print(f"Success, returning.. {return_json}")
    return json.dumps(return_json)
