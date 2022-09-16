FROM python:3.9.6-slim-buster

WORKDIR /backend

COPY requirements.txt /backend

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

RUN python -m grpc_tools.protoc -I config --python_out=. --grpc_python_out=. config/proto_message.proto

EXPOSE 3000

ENV GRPC_DNS_RESOLVER=native

CMD ["python", "app.py"]