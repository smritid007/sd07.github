import concurrent.futures
import socket
import logging
import json
import csv
import threading
import shutil


logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s',)                       #for debugging
#connection establishment
# s=socket.socket()
host="127.0.0.1"
print("host is :", host)
port_http_server=12347
port_order = 12200
# s.bind((host,port))
# s.listen(5)

class Catalog_Service:
	def __init__(self, client_socket, address, port_type):
		self.client_socket = client_socket
		self.address = address
		self.response_sent = False
		self.port_type = port_type

	def run(self):
		while True:
			if self.response_sent:
				break
			print("running catalog service")
			data = self.client_socket.recv(1024).decode()
			print(f"Received {data}")
			'''if(self.port_type == 12347):
				self.Query(data)
			elif(self.port_type == 12200):
				self.Buy(data)'''
			if 'Query' in data:
				self.Query(data)
			elif "Buy" in data:
				self.Buy(data)	
		self.client_socket.close()
		print(f"Socket with {self.address} closed.")

	def Query(self, data):
		print("inside Query")
		data_entry = data.split()[1]
		el={}
		file = open('database.csv', 'r')
		csvreader = csv.reader(file)
		header = []
		header = next(csvreader)
		dict_from_csv=[]
		with file:
			reader =csv.DictReader(file, fieldnames=('toy_name','price','Quantity'))
			for rows in reader:
				dict_from_csv.append(rows)
		for el in dict_from_csv:
			if el['toy_name'] == data_entry:
				break #return the entire object back to http server

		######INSERT FILE READ LOGIC#######
		response = """\HTTP/1.1 {status_code} {status_message} Content-Type: application/json; charset=UTF-8 Content-Length: {content_length} {payload} """
		res = el
		payload=json.dumps(res)
		print("Sending from catalog")
		print(payload)
		
		self.client_socket.send(response.format(status_code=200,
                                   status_message="OK",
                                   content_length=len(payload),
                                   payload=payload)
                   .encode("utf-8"))
		print("Response sent.")
		self.response_sent = True

	def Buy(self, data):
		response = """\HTTP/1.1 {status_code} {status_message} Content-Type: application/json; charset=UTF-8 Content-Length: {content_length} {payload} """
		data_entry = data.split()[1]
		element={}
		el={}
		file = open('database.csv', 'r')
		csvreader = csv.reader(file)
		header = []
		header = next(csvreader)
		dict_from_csv=[]
		with file:
			reader =csv.DictReader(file, fieldnames=('toy_name','price','quantity'))
			for rows in reader:
				print(rows)
				dict_from_csv.append(rows)
		for element in dict_from_csv:
			print(element['toy_name'])
			if element['toy_name'] == data_entry:
				print("element", element)
				old_q = int(element['quantity'])
				print("old_q:", old_q)
				element['quantity']=int(element['quantity'])-1
				new_q = int(element['quantity'])
				print("new quantity:", new_q)
				el= element
				print("el", el)
				self.writer(element, old_q, new_q,"database.csv")

		payload = json.dumps(el)
		self.client_socket.send(response.format(status_code=200,
                                   status_message="OK",
                                   content_length=len(payload),
                                   payload=payload)
                   .encode("utf-8"))
		print("Response sent.")
		self.response_sent = True
	
		#shutil.move(tempfile.name, filename)
	def writer(self, data, old_q, new_q, filename):
			print("inside update function")
			file = open(filename, "r+")
			replacement=""
			for line in file:
				print(line)
				if data['toy_name'] in line:
					old = data['toy_name'] + ","+ data['price'] + "," + str(old_q)
					n = data['toy_name'] + ","+ data['price'] + "," + str(new_q)
					changes = line.replace(old, n)
				else:
					changes = line
				replacement = replacement + changes 

			file.close()
			fout = open(filename, "w")
			fout.write(replacement)
			fout.close()
'''def main():

	#To listen to HTTP server for Query requests
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock1:
		sock1.bind((host, port_http_server))
		sock1.listen(10)
		print("Server listening on port", port_http_server)
		while True:
			conn1, addr1 = sock1.accept()
			print("connection from http_server")
			catalog_service = Catalog_Service(conn1, addr1, port_http_server)
			t1 = threading.Thread(target=catalog_service.run)
			t1.start()
		print("Server shutting down")
	with socket.socket(socket.AF_INET, socket.SOCK_STEAM) as sock2:
		sock2.bind((host, port_order))
		sock2.listen(10)
		print("Server listening on port", port_order)
		while True:
			conn2, addr2 = sock2.accept()
			catalog_service = Catalog_Service(conn2, addr2, port_order)
			t2 = threading.Thread(target=catalog_service.run)
			t2.start()
		print("Server shutting down")
		
'''
def main():
	sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock1.bind((host, port_http_server))
	sock1.listen(10)
	while True:
		conn2, addr2 = sock1.accept()
		catalog_service = Catalog_Service(conn2, addr2, port_order)
		t2 = threading.Thread(target=catalog_service.run)
		t2.start()
	print("Server shutting down")
	

if __name__ == '__main__':
    main()
