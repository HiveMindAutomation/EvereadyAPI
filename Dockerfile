# start by pulling the python image
FROM python:3.13.3-alpine

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install gcc
RUN apk add build-base

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy all content from the local file to the image
COPY . /app

# configure the container to run in an executed manner
CMD [ "python", "./main.py"]