FROM nvidia/cuda:11.6.0-devel-ubuntu20.04


RUN apt update --fix-missing
RUN apt install -y python3-gi python3-dev python3-gst-1.0 python3-numpy python3-opencv

RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y curl
RUN apt-get update
RUN apt-get install unzip
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt update --fix-missing 
RUN apt-get install -y git

RUN pip install PyTurboJPEG
RUN pip install --upgrade pip
RUN pip3 install openvino==2022.1.0 
RUN pip install openvino-dev termcolor
RUN pip install tqdm


RUN pip3 install -r requirements.txt

COPY app/ /app

WORKDIR /app


CMD ["python3","run.py"]


# COPY app /app

# WORKDIR /app

# RUN mkdir /data


