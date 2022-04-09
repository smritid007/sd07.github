import socket
import json

def main():
    target_host= "127.0.0.1"
    target_port= 8080

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    client.connect((target_host,target_port)) 

    toy_name={"name":"Tux"}
    jsonObj = json.dumps(toy_name)
    while True:
        request = "GET /products/%s HTTP/1.1\r\nHost:%s\r\nContent-Type: application/json\r\nContent-Length: 47\r\n\r\n %s" %(toy_name,target_host, jsonObj)
        client.send(request.encode())  
        
        # receive some data 
        response = client.recv(4096) 
        http_response = repr(response)
        print ("this is the response for get",http_response) 
    

main()