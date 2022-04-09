
import socket
import json
import csv
import threading

host="127.0.0.1"
print("server is running:", host)
port_http_server=12347
port_order = 12200
read_count=0
read_lock = threading.Lock()
write_lock = threading.Lock()


class Catalog_Service:
	def __init__(self, client_socket, address, port_type):
		self.client_socket = client_socket
		self.address = address
		self.response_sent = False
		self.port_type = port_type

	def run(self):
		global read_count
		while True:
			#if self.response_sent:
			#	break
			print("running catalog service")
			data = self.client_socket.recv(1024).decode()
			if not data:
				break
			print(f"Received {data}")
			if 'Query' in data:
				read_lock.acquire()
				read_count+=1
				if read_count==1:
					write_lock.acquire()
				read_lock.release()
				self.Query(data)
			elif "Buy" in data:
				write_lock.acquire()
				self.Buy(data)	
		self.client_socket.close()
		print(f"Socket with {self.address} closed.")

	def Query(self, data):
		global read_count
		print("inside Query")
		data_entry = data.split()[1]
		el={}
		file = open('database.csv', 'r')
		csvreader = csv.reader(file)
		header = []
		header = next(csvreader)
		dict_from_csv=[]
		with file:
			reader =csv.DictReader(file, fieldnames=('toy_name','price','quantity'))
			for rows in reader:
				dict_from_csv.append(rows)
		for el in dict_from_csv:
			if el['toy_name'] == data_entry:
				break #return the entire object back to http server

		######INSERT FILE READ LOGIC#######
		response = """\HTTP/1.1 {status_code} {status_message} \r\nContent-Type: application/json; \r\ncharset=UTF-8 \r\nContent-Length: {content_length} \r\n{payload} """
		res = el
		payload=json.dumps(res)
		
		self.client_socket.send(response.format(status_code=200,
                                   status_message="OK",
                                   content_length=len(payload),
                                   payload=payload)
                   .encode("utf-8"))
		read_lock.acquire()
		read_count-=1
		if read_count==0:
			write_lock.release()
		read_lock.release()
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
				dict_from_csv.append(rows)
		for element in dict_from_csv:
			print(element['toy_name'])
			if element['toy_name'] == data_entry:
				old_q = int(element['quantity'])
				element['quantity']=int(element['quantity'])-1
				new_q = int(element['quantity'])
				el= element
				self.writer(element, old_q, new_q,"database.csv")
		
		payload = json.dumps(el)
		self.client_socket.send(response.format(status_code=200,
                                   status_message="OK",
                                   content_length=len(payload),
                                   payload=payload)
                   .encode("utf-8"))
		write_lock.release()
		print("Response sent.")
		self.response_sent = True
	
	def writer(self, data, old_q, new_q, filename):
			print("inside update function")
			file = open(filename, "r+")
			replacement=""
			for line in file:
				print("line:", line)
				if data['toy_name'] in line:
					n = data['toy_name'] +"," + data['price'] + "," + str(new_q)+"\n"
					changes = line.replace(line, str(n))
				else:
					changes = line
				replacement = replacement + changes 

			file.close()
			fout = open(filename, "w")
			fout.write(replacement)
			fout.close()

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
