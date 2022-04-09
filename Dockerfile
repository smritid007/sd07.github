FROM python:3

RUN pip3 install sockets
RUN pip3 install thread6

ADD catalog_service.py .
ADD database.csv .

ENTRYPOINT [ "python3", "./catalog_service.py" ]