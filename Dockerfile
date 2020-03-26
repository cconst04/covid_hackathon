 FROM ubuntu
 ENV PYTHONUNBUFFERED 1
 ARG DEBIAN_FRONTEND=noninteractive
 RUN mkdir /code
 WORKDIR /code
 ADD requirements.txt /code/
 ADD . /code/
 RUN apt-get update ; apt-get install -y python ; apt-get install -y python3-pip
 RUN apt-get install -y libsm6 libxext6 libxrender-dev
 RUN pip3 install -r requirements.txt
 RUN apt-get install -y binutils libproj-dev gdal-bin postgis postgresql-10-postgis-scripts
