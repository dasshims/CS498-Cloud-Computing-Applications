import requests
import json
import uuid

url = "https://seorwrpmwh.execute-api.us-east-1.amazonaws.com/prod/mp3-lexv2-autograder"

payload = {
    "graphApi": "https://6up4i7h103.execute-api.us-east-1.amazonaws.com/default/graph_search_bfs",
    # <post api for storing the graph>,
    "botId": "FMIQC57RZZ",  # <id of your Amazon Lex Bot>,
    "botAliasId": "VSDXUB5TXM",  # <Lex alias id>,
    "identityPoolId": "us-east-1:5c16a07a-45e1-4c78-b106-6534082fb479",  # <cognito identity pool id for lex>,
    "accountId": "550114587963",  # <your aws account id used for accessing lex>,
    "submitterEmail": "hdas4@illinois.edu",  # <insert your coursera account email>,
    "secret": "3kAwCEzRwD3dd7xI",  # <insert your secret token from coursera>,
    "region": "us-east-1"  # <Region where your lex is deployed (Ex: us-east-1)>
}

r = requests.post(url, data=json.dumps(payload))

print(r.status_code, r.reason)
print(r.text)
