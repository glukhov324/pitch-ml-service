FROM python:3.12

SHELL [ "/bin/bash", "-c" ]

WORKDIR /app

COPY . /app

RUN apt-get update && \
    apt-get install ffmpeg libsm6 libxext6  -y && \
    pip install --upgrade pip && \ 
    pip install -r /app/requirements.txt

RUN pip install torch==2.2.1 torchvision==0.17.1 torchaudio==2.2.1 --index-url https://download.pytorch.org/whl/cu118

CMD python3 run.py