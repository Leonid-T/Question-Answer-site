FROM python:3.10
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY ./ask ./ask
WORKDIR ./ask
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]