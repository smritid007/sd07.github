import json
import socket
import threading

HOST = "127.0.0.1"
PORT = 8080

'''response = """\
HTTP/1.1 {status_code} {status_message}
Content-Type: application/json; charset=UTF-8
Content-Length: {content_length}

{payload}
"""'''

class Session:
    def __init__(self, client_socket, address):
        self.client_socket = client_socket
        self.address = address
        self.response_sent = False

    def run(self):
        while True:
            if self.response_sent:
                break
            print("not broken")
            data = self.client_socket.recv(1024)
            data = data.decode("utf-8")
            print(data.splitlines()[0])
            if "GET" in data.splitlines()[0]:      #== "GET /products/ HTTP/1.1":
                new_s = socket.socket()
                new_s.connect((HOST, 12347))
                print("connection established with catalog:")
                json_temp = json.loads(data.splitlines()[5])
                print(json_temp)
                self.send_response(json_temp,new_s,"Query ")
                data = self.client_socket.recv(1024)
                print("data received from catalog_service:", data)
                

            elif "POST" in data.splitlines()[0]:       #== "GET /products/ HTTP/1.1":
                new_s = socket.socket()
                new_s.connect((HOST, 5000))
                json_temp = json.loads(data.splitlines()[5])
                self.send_response(json_temp,new_s, "Buy ")
                data = self.client_socket.recv(1024)
                
            else:
                response = """\HTTP/1.1 {status_code} {status_message} Content-Type: application/json; charset=UTF-8 Content-Length: {content_length} {payload} """
                payload = json.dumps({"message": "File not found"})
                self.client_socket.send(response.format(status_code=404,
                                   status_message="Not Found",
                                   content_length=len(payload),
                                   payload=payload)
                   .encode("utf-8"))

        self.client_socket.close()
        print(f"Socket with {self.address} closed.")

    def send_response(self,json_temp,new_s, option):
        print("inside send")
        response = """\HTTP/1.1 {status_code} {status_message} Content-Type: application/json; charset=UTF-8 Content-Length: {content_length} {payload} """
        new_s.send(option.encode())
        new_s.sendall(json_temp["data"]["name"].encode())  #sending encoded toy_name to catalog service for Query method
        print("sent toy_name")
        payload=new_s.recv(1024).decode()
        print("received payload from order/catalog")

        self.client_socket.send(response.format(status_code=200,
                                   status_message="OK",
                                   content_length=len(payload),
                                   payload=payload)
                   .encode("utf-8"))
        print("Response sent.")
        self.response_sent = True
'''def main():
    print("into main")
    s = socket.socket()
    s.bind((HOST, PORT))
    s.listen(1)
    print("listening")
    while True:
        c, addr = s.accept()
        data = c.recv(1024)
        data = data.decode("utf-8")
        print(data.splitlines()[0])
        if "GET" in data.splitlines()[0]:       #== "GET /products/ HTTP/1.1":
            new_s = socket.socket()
            new_s.connect((HOST, 12347))
            #print("server received",data.splitlines()[5])
            json_temp = json.loads(data.splitlines()[5])
            #print(json_temp["data"]["name"])
            new_s.send(json_temp["data"]["name"].encode())  #sending encoded toy_name to catalog service for Query method
           
            payload=new_s.recv(1024).decode()
             print("Payload received from catalog: ")
            print(payload)
            print(type(payload))
            
            c.send(response.format(status_code=200,
                                   status_message="OK",
                                   content_length=len(payload),
                                   payload=payload)
                   .encode("utf-8"))

        elif "POST" in data.splitlines()[0]:
            new_s = socket.socket()
            new_s.connect((HOST, 5000))
            print("server received",data.splitlines()[5])
            json_temp = json.loads(data.splitlines()[5])
            print(json_temp["data"]["toy_name"])
            new_s.send(json_temp["data"]["toy_name"].encode())  #sending encoded toy_name to catalog service for Query method
            #payload = json.dumps({"message": "Hello World"})
            # message_rcvd=new_s.recv(1024).decode()
            payload=new_s.recv(1024).decode()
            print("Payload received from catalog in POST: ")
            print(payload)
            print(type(payload))

            #payload = json.loads(payload)
            c.send(response.format(status_code=200,
                                   status_message="OK",
                                   content_length=len(payload),
                                   payload=payload)
                   .encode("utf-8"))

        else:
            payload = json.dumps({"message": "File not found"})
            c.send(response.format(status_code=404,
                                   status_message="Not Found",
                                   content_length=len(payload),
                                   payload=payload)
                   .encode("utf-8"))

        c.close()'''


def serve_forever(host: str, port: int):
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)

    while True:
        client_socket, address = server_socket.accept()
        print(f"Socket established with {address}.")
        session = Session(client_socket, address)
        t = threading.Thread(target=session.run)
        t.start()


if __name__ == "__main__":
    serve_forever("127.0.0.1", 8080)