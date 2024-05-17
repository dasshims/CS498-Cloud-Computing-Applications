It should be copying all the below files 
# Copy src files folder (requirements.txt and classify.py)
COPY ...

In the reference dockerfile - https://github.com/UIUC-CS498-Cloud/MP12_PublicFiles/blob/main/Dockerfile, the COPY command should be copying 4 files, preload_data.py, train.py alone with the  requirements.txt and classify.py for the docker file to dun

Requirements file has invalid torch version
2.064 ERROR: Could not find a version that satisfies the requirement torch==1.4.0 (from versions: 1.8.0, 1.8.1, 1.9.0, 1.10.0, 1.10.1, 1.10.2)

7.530 ERROR: Could not find a version that satisfies the requirement torchvision==0.5.0 (from versions: 0.1.6, 0.1.7, 0.1.8, 0.1.9, 0.2.0, 0.2.1, 0.2.2, 0.2.2.post2, 0.2.2.post3, 0.9.1, 0.10.0, 0.11.1, 0.11.2, 0.11.3)


Good idead to inlcude --platform linux/amd64 in the Dockerfile since most laptops are ARM based



## Genuine bug
if The increase the desired capacity to 3 the Test 1 fails 