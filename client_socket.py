import socket
import json
import random
import sys

def main(argv):
    target_host= "127.0.0.1"
    target_port= 8080

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    client.connect((target_host,target_port)) 
    toy="Tux"
    toy_name={"name":"Tux"}
    jsonObj = json.dumps(toy_name)
    buy_request={"name":"Tux", "quantity": "1"}
    jsonObj_buy = json.dumps(buy_request)
    while True:
        #print(i)
        request = "GET /products/%s HTTP/1.1\r\nHost:%s\r\nContent-Type: application/json\r\nContent-Length: 47\r\n\r\n %s" %(toy,target_host, jsonObj)
        client.send(request.encode())  
        response = client.recv(4096) 
        json_temp = response.splitlines()[-1]
        json_temp = json.loads(json_temp)
        print(json_temp)

        if int(json_temp['data']['quantity'])>0:
            cmp = random.uniform(0,1)
            print(cmp)

            if cmp < float(argv[1]):
                request = 'POST / HTTP/1.1\r\nHost: %s\r\nContent-Type: application/json\r\nContent-Length: 47\r\n\r\n %s' %(target_host, jsonObj_buy)
                client.send(request.encode())  
                response = client.recv(4096) 
                response = response.decode('utf-8')
                print ("this is the final output after buying ", response)
        print("end of for")
if __name__=="__main__":
    main(sys.argv)
