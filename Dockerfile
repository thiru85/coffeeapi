FROM alpine:latest
RUN apk add --update python3 py3-pip libpq-dev python3-dev gcc wget aws-cli curl
RUN mkdir app
COPY . app/
WORKDIR app
RUN pip3 install -r requirements.txt
EXPOSE 80
ENTRYPOINT ["python3", "app.py"]

