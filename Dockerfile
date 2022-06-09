FROM python:slim-buster
ARG BOT_TOKEN
ARG DB_PASSWORD
WORKDIR home/ens-domains-availability-checker/
RUN apt-get update
RUN apt-get -y install gcc

RUN apt-get install -y wget
RUN apt-get install -y unzip
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get -y install ./google-chrome-stable_current_amd64.deb
RUN wget -q https://chromedriver.storage.googleapis.com/103.0.5060.24/chromedriver_linux64.zip
RUN unzip  /home/ens-domains-availability-checker/chromedriver_linux64.zip -d chromedriver
RUN chmod +x /home/ens-domains-availability-checker/chromedriver


COPY ./requirements.txt home/ens-domain-availability-checker/requirements.txt
RUN pip install --user --no-cache-dir -r home/ens-domain-availability-checker/requirements.txt
COPY . /home/ens-domains-availability-checker/
ENV BOT_TOKEN="$BOT_TOKEN"
ENV DB_PASSWORD="$DB_PASSWORD"
ENV PYTHONPATH=/home/ens-domains-availability-checker/
CMD ["python", "main.py"]