# MP8 SparkSQL Template

This is the Java and Python template for MP8 SparkSQL.

## Log 
Updated in Feb 2024, by Gautam Putcha (gputcha2@illinois.edu).

Updated in May 2023, by Shujing Yang (shujing6@illinois.edu).

Updated in Feb 2022, by Yifan Chen (yifanc3@illinois.edu).

Updated in April 2021, by Ruiyang Chen (rc5@illinois.edu).


## Instructions

```bash
docker build -t mp8 .
docker run --name mp8-cntr -it mp8
docker start -a mp8-cntr
```

Inside the docker container

```bash
./run.sh MP8_PartB Output_PartB
```