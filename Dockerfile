FROM python:slim
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . . 
RUN apt update -y &&\
    apt install -y curl gnupg2 tini lsb-release &&\
    echo "deb http://packages.cloud.google.com/apt gcsfuse-jessie main" | \
    tee /etc/apt/sources.list.d/gcsfuse.list &&\
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | \
    apt-key add - &&\
    apt update -y &&\
    apt install -y  gcsfuse kmod git &&\
    mkdir /bucket &&\
    chmod +x gcsmount.sh gitclone.sh

ENV PORT 8080
ENTRYPOINT exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app

