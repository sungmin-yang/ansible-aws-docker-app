# Flask image

#FROM alpine:3.13
FROM python:3.8-alpine
RUN apk add build-base

#ADD ./app /home/app/
ADD requirements.txt /home/app/
WORKDIR /home/app/


Run apk update
RUN apk add --no-cache postgresql-dev gcc python3 python3-dev musl-dev
RUN apk add --update py3-pip && \
#    python3 -m ensurepip && \
#    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip

Run apk add jpeg-dev zlib-dev && \
    pip install --ignore-installed pillow && \
    pip3 install setuptools && \
    rm -r /root/.cache && \
    pip3 install -r requirements.txt

EXPOSE 5000

#ENTRYPOINT ["python3", "app.py"]