import grpc
from concurrent import futures
import proto_message_pb2 as pb2
import proto_message_pb2_grpc as pb2_grpc
from time import sleep
from routes import querys

class SearchService(pb2_grpc.SearchServicer):

    def __init__(self, *args, **kwargs):
        pass

    def GetServerResponse(self, request, context):
        item = []
        response = []
        message = request.message
        result = f'"{message}" '
        cursor.execute("SELECT * FROM data;")
        query_res = cursor.fetchall()
        for row in query_res:
            if message in row[1]:
                item.append(row)
        for i in item:
            result = dict()
            result['id'] = i[1]
            result['url']= i[2]
            result['title'] = i[3]
            result['description']= i[4]
            result['keywords']= i[5]
            response.append(result)
        
        print(pb2.SearchResults(product=response))
        return pb2.SearchResults(product=response)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_SearchServicer_to_server(SearchService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

def insert_from_txt():
    with open('./db/insert.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            try:
                cursor.execute(line)
            except:
                pass
if __name__ == '__main__':
    #sleep(20)
    conn = querys.init_db()
    cursor = conn.cursor()
    serve()
    insert_from_txt()