FROM python:3.7.8
COPY . /app
WORKDIR /app

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential

RUN pip install --upgrade pip && \
    pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm

COPY nginx.conf /etc/nginx
RUN chmod +x ./start.sh

CMD ["./start.sh"]


