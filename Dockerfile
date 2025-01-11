FROM python:3.10-slim-buster
RUN apt-get update -y
RUN apt-get install git curl python3-pip ffmpeg -y
RUN python3 -m pip install --upgrade pip
RUN pip3 install -U pip
# Install Node.js and npm
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    npm i -g npm

RUN npm i -g npm
COPY . /adarsh/
WORKDIR /adarsh/
RUN pip3 install -U -r Installer
CMD python3 -m Adarsh
