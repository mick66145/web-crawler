FROM python:3.9.5

# M1系列使用這個
# FROM --platform=linux/amd64 python:3.9.5
ENV PYTHONUNBUFFERED 1
EXPOSE 80

RUN mkdir /app
WORKDIR /app

COPY requirements.txt ./
COPY startup.sh ./

RUN pip install -r requirements.txt

RUN apt-get update
RUN apt-get install -y wget
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get -y install google-chrome-stable

CMD ["/bin/bash","-c","./startup.sh"]