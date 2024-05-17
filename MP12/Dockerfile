FROM python:3.6

# Creating Application Source Code Directory
RUN mkdir -p /usr/src/app

# Setting Home Directory for containers
WORKDIR /usr/src/app

# Copy src files folder (requirements.txt and classify.py)
COPY * /usr/src/app/
#COPY data_preload.py /usr/src/app/
#COPY train.py /usr/src/app/
#COPY classify.py /usr/src/app/

RUN mkdir -p /usr/src/app/models

# Installing python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Application Environment variables.
# These variables will be used when you run the image.
# You will also need to pass corresponding DATASET and TYPE variables from the job yaml files of both free-service and default types of jobs.
ENV APP_ENV development
ENV DATASET mnist
ENV TYPE ff

# Preload the data
RUN python data_preload.py

# Pretrain the models
RUN python train.py --dataset mnist --type ff
RUN python train.py --dataset mnist --type cnn
RUN python train.py --dataset kmnist --type ff
RUN python train.py --dataset kmnist --type cnn

# Exposing Ports
EXPOSE 5035

# Setting Persistent data
VOLUME ["/app-data"]

# Running Python Application (classify.py)
CMD ["python", "classify.py"]
