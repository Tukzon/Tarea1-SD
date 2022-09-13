FROM python:3.9.6-slim-buster

WORKDIR /cliente

COPY proto_message.proto ./

COPY requirements.txt /cliente

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

RUN python -m grpc_tools.protoc -I ./ --python_out=. --grpc_python_out=. ./proto_message.proto

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 8000

COPY . .

CMD ["flask", "run"]