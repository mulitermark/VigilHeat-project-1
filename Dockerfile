FROM nvidia/cuda:11.6.0-devel-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update --fix-missing

RUN apt install -y python3-gi python3-dev python3-gst-1.0 python3-numpy python3-opencv

RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y curl
RUN apt update --fix-missing 
RUN apt-get install -y git
RUN apt install python3-pip -y


# RUN pip3 install openvino openvino-dev termcolor

RUN ls

COPY app/ /app

WORKDIR /app


RUN apt-get install python3-tk -y
RUN apt-get install python3-scipy -y
RUN pip3 install -r requirements.txt

CMD ["python3","main.py"]


# COPY app /app

# WORKDIR /app

# RUN mkdir /data


