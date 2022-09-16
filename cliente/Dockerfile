FROM python:3.9.6-slim-buster

WORKDIR /cliente

COPY proto_message.proto ./

COPY requirements.txt /cliente

RUN python3 -m pip install --upgrade pip

RUN pip3 install -r requirements.txt

RUN python3 -m grpc_tools.protoc -I ./ --python_out=. --grpc_python_out=. ./proto_message.proto

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV GRPC_DNS_RESOLVER=native

EXPOSE 8000

COPY . .

CMD ["flask", "run"]