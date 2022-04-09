import json
import socket
import threading
import csv
import concurrent
from concurrent.futures import ThreadPoolExecutor

read_count=0
read_lock=threading.Lock()
write_lock=threading.Lock()

class Session:
    def __init__(self, client_socket, address):
        self.client_socket = client_socket
        self.address = address
        self.response_sent = False

    def run(self):
        while True:
            #if self.response_sent:
            #   break
            print("inside run")
            data = self.client_socket.recv(1024)
            data = data.decode("utf-8")
            if not data:
                break
            print(data)
            print("sending connection to catalog")
            new_s = socket.socket()
            new_s.connect(('127.0.0.1', 12347))
            print("got cpnnected to catalog")
            order_no=self.writer(data,'file.csv')
            print(order_no)
            self.send_response(new_s, data, order_no)
            print(f"Received {data}")
        self.client_socket.close()
        print(f"Socket with {self.address} closed.")

    def send_response(self,new_s, data, order_no):
        response = """\HTTP/1.1 {status_code} {status_message}\r\n Content-Type: application/json; \r\ncharset=UTF-8 \r\nContent-Length: {content_length} \r\n{payload} """
        new_s.send(data.encode())  #sending encoded toy_name to catalog service for Query method 
        
        payload = {"data":{"order_no":order_no}}
        payload = json.dumps(payload)
        self.client_socket.send(response.format(status_code=200,
                                   status_message="OK",
                                   content_length=len(payload),
                                   payload=payload)
                   .encode("utf-8"))
        print("Response sent.")
        self.response_sent = True
    
    def writer(self, data, filename):
        print("inside update function")
        write_lock.acquire()
        with open(filename, 'r') as f:
            header=f.readlines()[0]
        
        with open(filename, 'r') as f:
            last_line = f.readlines()[-1]
            
        
        with open(filename, 'a') as f:
            writer = csv.writer(f)
            if header!=last_line:
                t=last_line.split(',')
                fields=[int(t[0])+1,t[1],int(t[2])]
                writer.writerow(fields)
                order_no=int(t[0])+1
            else:
                writer.writerow([0,data,2])
                order_no=0
        
        write_lock.release()
        return order_no

    


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
    server = MyTcpServer('127.0.0.1', 5000)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:    

        while 1:
            client_socket, address = server.wait_accept()
            print(f"Socket established with {address}.")
            session = Session(client_socket, address)
            future = pool.map(session.run())
            print("final count of # threads: ",threading.active_count())