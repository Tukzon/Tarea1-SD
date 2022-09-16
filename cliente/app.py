from flask import Flask, request, render_template  

import grpc
import redis
import logging

import proto_message_pb2 as pb2_grpc
import proto_message_pb2_grpc as pb2
import json, time

app = Flask(__name__, template_folder='template')


r = redis.Redis(host="redis1", port=6379, db=0)
#r.config_set('maxmemory', 865200*2)
r.config_set('maxmemory-policy', 'allkeys-lru')
r.flushall()

class SearchClient(object):
    """
    Client for gRPC functionality
    """

    def __init__(self):
        self.host = 'backend'
        self.server_port = '50051'

        # instantiate a channel
        self.channel = grpc.insecure_channel('{}:{}'.format(self.host, self.server_port))

        # bind the client and the server
        self.stub = pb2.SearchStub(self.channel)

    def get_url(self, message):
        """
        Client function to call the rpc for GetServerResponse
        """
        message = pb2_grpc.Message(message=message)
        print(f'{message}')
        stub = self.stub.GetServerResponse(message)
        return stub


@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/search', methods = ['GET'])
def search():
    client = SearchClient()
    print(client)
    search = request.args['search']
    cache = r.get(search)
    if cache == None:
        data = client.get_url(message=search)
        
        r.set(search, str(data))
        
        return render_template('index.html', datos = data, procedencia = "Datos sacados de PostgreSQL")
    
    else:
        print(cache)
        data = cache.decode("utf-8")
        print(data)
        dicc = dict()
        dicc['Resultado'] = data
        print(cache)
        print(dicc)
        return render_template('index.html', datos = data, procedencia = "Datos sacados de Redis")
        #line = "Datos sacados de Redis" + item
        #print("en redis")

if __name__ == '__main__':
    #time.sleep(25)
    app.run(debug=True)
    #result = client.get_url(message="Hello Server you there?")
    #print(result.product[0].name + "*******")
    #print(f'{result}')