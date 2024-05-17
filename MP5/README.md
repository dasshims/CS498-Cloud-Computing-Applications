# MP5_SparkMapReduce_Template
This is the template for MP5 Spark MapReduce, including the Docker image and Python template.

## Setup

# clone the repository and find the docker file
git clone https://github.com/UIUC-CS498-Cloud/MP5_SparkMapReduce_Template.git
cd MP5_SparkMapReduce_Template/Docker

# build an image for mp5 based on the docker file
docker build -t mp5 .

# create a container named 'mp5-cntr' for mp5 using the image mp5
docker run --name mp5-cntr -it mp5
# or start the 'mp5-cntr' container if you have created it
docker start -a mp5-cntr

# Running the code 

Part C:
spark-submit OrphanPagesSpark.py dataset/links/ partC
Part D:
spark-submit TopPopularLinksSpark.py dataset/links/ partD
Part E:
spark-submit PopularityLeagueSpark.py dataset/links/ dataset/league.txt partE

Part A: Congrats!_All_lines_are_correct!      ;
Part B: Congrats!_All_lines_are_correct!      ;
Part C: Invalid_output.The_number_of_lines_produced_by_your_code_is_not_valid.      ;
Part D: Your_output_contains:_10_incorrect_lines_in_our_test.Please_try_again!      ;
Part E: Invalid_input_file_format      ;


