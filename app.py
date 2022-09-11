import psycopg2
import sys
import boto3
import os
import json
import warnings
import random
from flask import Flask
import socket

app = Flask(__name__)

@app.route("/")
def coffee_api():

    query_list=[]
    for result in query_results:
        t = (result[0], result[1], result[2])
        query_list.append(t)
    output=(query_list[random.randint(0,len(query_results))])
    return {
        "id": output[0],
        "coffeeType": output[1],
        "coffeeSize": output[2],
        "containerID": socket.gethostname()
    }


warnings.filterwarnings('ignore', category=FutureWarning, module='botocore.client')
ENDPOINT="pgdb1.coathyy6no9j.us-east-1.rds.amazonaws.com"
PORT="5432"
USER="dbiamuser"
REGION="us-east-1"
DBNAME="postgres"

session = boto3.Session()
client = session.client('rds')
token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION)

try:
    conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USER, password=token, sslrootcert="SSLCERTIFICATE")
    cur = conn.cursor()
    cur.execute("""SELECT * FROM public.coffee""")
    query_results = cur.fetchall()

except Exception as e:
    print("Database connection failed due to {}".format(e))

app.run(host='0.0.0.0', port='8081')