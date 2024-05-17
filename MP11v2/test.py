import csv
import requests
import json

url = "https://seorwrpmwh.execute-api.us-east-1.amazonaws.com/prod/mp11"

student = {
    "submitterEmail": "hdas4@illinois.edu",  # <Your coursera account email>
    "secret": "MRlKGnZ0nchgZy6W"  # <Your secret token from coursera>
}
lambda_url = "https://d5sgadicepzjz3qk2jtsxztx5m0wllmk.lambda-url.us-east-1.on.aws/"

exerciseACsvPath = "/Users/himangshudas/old_pc/MS/CCA/MPs/MP11v2/a.csv"  # <Filepath for your exercise A csv file>
exerciseBCsvPath = "/Users/himangshudas/old_pc/MS/CCA/MPs/MP11v2/b.csv"  # <Filepath for your exercise B csv file>
exerciseCCsvPath = ""  # <Filepath for your exercise C csv file>


# if left blank that part will be skipped


def readexerciseA(filePath):
    vizData = {}

    with open(filePath, encoding="utf8", errors='ignore') as csvfile:
        reader = csv.reader((line.replace('\0', '')
                             for line in csvfile), delimiter=',')
        header = reader.__next__()
        header = [x.strip() for x in header]
        date = header.index("date")
        cmgr = header.index("cmgr")
        close_price = header.index("close_price")

        for row in reader:
            vizData[row[date]] = [str(row[cmgr]), str(row[close_price])]

    return vizData


def readexerciseB(filePath):
    vizData = {}

    with open(filePath, encoding="utf8", errors='ignore') as csvfile:
        reader = csv.reader((line.replace('\0', '')
                             for line in csvfile), delimiter=',')
        header = reader.__next__()
        header = [x.strip() for x in header]
        date = header.index("date")
        ema = header.index("ema_close_price")
        close_price = header.index("close_price")

        for row in reader:
            vizData[row[date]] = [str(row[ema]), str(row[close_price])]
    return vizData


def readexerciseC(filePath):
    vizData = {}

    with open(filePath, encoding="utf8", errors='ignore') as csvfile:
        reader = csv.reader((line.replace('\0', '')
                             for line in csvfile), delimiter=',')
        header = reader.__next__()
        header = [x.strip() for x in header]
        initialDate = header.index("initialPriceDate")
        dropDate = header.index("dropDate")
        dropPercentage = header.index("dropPercentage")
        initialPrice = header.index("initialPrice")
        lastPrice = header.index("lastPrice")

        for row in reader:
            vizData[row[dropDate]] = [str(row[initialDate]), str(
                row[dropPercentage]), str(row[initialPrice]), str(row[lastPrice])]
    return vizData


def sendToAutograder(payload):
    r = requests.post(url, data=json.dumps(payload))
    r = requests.post(lambda_url, data=json.dumps(payload),
                      headers={"Content-Type": "application/json"})
    print("autograder called")
    print(r.status_code, r.reason)
    print(r.text)


def main():
    payload = {}
    payload['student'] = student
    payload['ans1_output'] = readexerciseA(exerciseACsvPath) if exerciseACsvPath else {}
    payload['ans2_output'] = readexerciseB(exerciseBCsvPath) if exerciseBCsvPath else {}
    payload['ans3_output'] = readexerciseC(exerciseCCsvPath) if exerciseCCsvPath else {}

    print(json.dumps(payload))
    sendToAutograder(payload)


if __name__ == "__main__":
    main()