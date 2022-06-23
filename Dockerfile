FROM python:slim-buster
ARG BOT_TOKEN
ARG BOT_ID
ARG DB_PASSWORD
ARG DB_HOST
ARG DB_PORT
ARG DB_USER
WORKDIR /home/ens-domains-availability-checker/

RUN apt-get update
RUN apt-get -y install gcc
RUN apt-get install -y wget
RUN apt-get install -y libnss3 libgconf-2-4

RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get -y install ./google-chrome-stable_current_amd64.deb

COPY . /home/ens-domains-availability-checker/
COPY ./requirements.txt /home/ens-domain-availability-checker/requirements.txt

RUN pip install --user --no-cache-dir -r /home/ens-domain-availability-checker/requirements.txt
ENV BOT_TOKEN="$BOT_TOKEN"
ENV BOT_ID="$BOT_ID"
ENV DB_PASSWORD="$DB_PASSWORD"
ENV DB_HOST="$DB_HOST"
ENV DB_PORT="$DB_PORT"
ENV DB_USER="$DB_USER"
ENV PYTHONPATH=/home/ens-domains-availability-checker/
CMD ["python", "main.py"]