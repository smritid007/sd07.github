import csv
def writer(data, filename):
    print("inside update function")
    with open(filename, 'r') as f:
        header=f.readlines()[0]
        print(header)
    with open(filename, 'r') as f:
        last_line = f.readlines()[-1]
        print(last_line)
    
    with open(filename, 'a') as f:
        writer = csv.writer(f)
        if header!=last_line:
            t=last_line.split(',')
            fields=[int(t[0])+1,t[1],int(t[2])]
            writer.writerow(fields)
        else:
            writer.writerow([0,data,2])
writer("Tux","file.csv")