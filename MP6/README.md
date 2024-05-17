# MP6_AuroraElastiCache_Grader_Version_2_2023_Testing_Public

Public repo for MP 6 Version 2 - 2023 Testing

In this repository, you will find:

1) mp6data.csv - csv file with the data to be loaded into the database. This file has 1000000 rows along with the header.
2) mp6_template.py - solution template - some of the code is already provided. You need to write the read and write functionalities.
3) submission.py - fill in your details and make submission. Run this script on your computer to make a submission.


## Loading data into mysql 

mysql -h mp6.cn4umkoes8ke.us-east-1.rds.amazonaws.com -P 3306 -u admin -p

mysql -h mp6-aurora.cluster-cn4umkoes8ke.us-east-1.rds.amazonaws.com -P 3306 -u admin -p

## Load data

LOAD DATA FROM S3 's3://uiuc-himangshu-mp6/mp6data.csv'
INTO TABLE mp6.mp6data
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(id,name,hero,power,xp,color);


### 
DELETE FROM mp6.mp6data WHERE  id > 1000000
select * FROM mp6.mp6data WHERE  id > 1000000


{"submitterEmail": "hdas4@illinois.edu", "secret": "rWuhfdiqH8gJXYBb", "dbApi": "https://6up4i7h103.execute-api.us-east-1.amazonaws.com/default/mp6"}
Running the autograder. This might take several seconds...
<Response [200]>
200 OK
All test cases passed: Time for Read without cache - 90.33640885353088 Time for Read with cache - 10.718011617660522 Time for Write without cache - 9.012333631515503 Time for Write with cache - 0.18088841438293457
