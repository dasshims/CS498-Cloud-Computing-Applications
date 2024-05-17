# MP7_HBase_Template
The Docker image, Python and Java template for MP7 HBase


## Prepare env

git clone https://github.com/UIUC-CS498-Cloud/MP7_HBase_Template.git
cd MP7_HBase_Template/Docker
docker build -t mp7 .
docker run -name mp7 -it mp7 bin/bash