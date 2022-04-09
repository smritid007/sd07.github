import json
import socket
import threading
import concurrent
from concurrent.futures import ThreadPoolExecutor

HOST = "127.0.0.1"
PORT = 8080


class Session:
    def __init__(self, client_socket, address):
        self.client_socket = client_socket
        self.address = address
        self.response_sent = False

    def run(self):
        while True:
            
            data = self.client_socket.recv(1024)
            data = data.decode("utf-8")
            if not data:
                break

            if "GET" in data.splitlines()[0]:      #== "GET /products/ HTTP/1.1":
                new_s = socket.socket()
                new_s.connect((HOST, 12347))
                json_temp = json.loads(data.splitlines()[5])
                #print("http server receives this data from client: ",json_temp)
                self.send_response(json_temp["name"],new_s,"Query ")
                

            elif "POST" in data.splitlines()[0]:       #== "GET /products/ HTTP/1.1":
                new_s = socket.socket()
                new_s.connect((HOST, 5000))
                json_temp = json.loads(data.splitlines()[5])
                #print("http server receives this data from client: ",json_temp)
                temp = json_temp["name"]+" "+json_temp["quantity"]
                self.send_response(temp ,new_s, "Buy ")
                
            else:
                response = """\HTTP/1.1 {status_code} {status_message} Content-Type: application/json; charset=UTF-8 Content-Length: {content_length} {payload} """
                payload = json.dumps({"message": "File not found"})
                self.client_socket.send(response.format(status_code=404,
                                   status_message="Not Found",
                                   content_length=len(payload),
                                   payload=payload)
                   .encode("utf-8"))

        self.client_socket.close()
        #print(f"Socket with {self.address} closed.")

    def send_response(self,temp,new_s, option):
        response = """\HTTP/1.1 {status_code} {status_message} \r\nContent-Type: application/json; \r\ncharset=UTF-8 \r\nContent-Length: {content_length} \r\n{payload} """
        new_s.send(option.encode())
        new_s.sendall(temp.encode())  #sending encoded toy_name to catalog service for Query method
        payload=new_s.recv(1024).decode('utf-8').splitlines()[-1]
        if option=="Query ":
            payload = json.loads(payload)
            payload = {"data":{"toy_name":payload['toy_name'],"price":payload['price'],"quantity":payload['quantity']}}
            payload= json.dumps(payload)
        elif option=="Buy ":
            payload= json.loads(payload)
        self.client_socket.send(response.format(status_code=200,
                                   status_message="OK",
                                   content_length=len(payload),
                                   payload=payload)
                   .encode("utf-8"))
        #print("Response sent to client.")

'''def serve_forever(host: str, port: int):
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)
    pool = ThreadPoolExecutor(5) 

    while True:
        client_socket, address = server_socket.accept()
        print(f"Socket established with {address}.")
        session = Session(client_socket, address)
        pool.submit(session.run)
        print("final count of # threads: ",threading.active_count())


if __name__ == "__main__":
    serve_forever("127.0.0.1", 8080)
       # 5 Processes 1 Direct service '''

class MyTcpServer:
  def __init__(self, ip, port):
    self.ip = ip
    self.port = port
    self.server = socket.socket()
    self.server.bind((self.ip, self.port))
    self.server.listen(5)

  def wait_accept(self):
    conn, addr = self.server.accept()
    return conn, addr



if __name__ == '__main__':
    server = MyTcpServer('127.0.0.1', 8080)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:    

        while 1:
            client_socket, address = server.wait_accept()
            print(f"Socket established with {address}.")
            session = Session(client_socket, address)
            future = pool.map(session.run())
            print("final count of # threads: ",threading.active_count())

  