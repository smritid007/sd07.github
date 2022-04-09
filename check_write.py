import csv
# opening the file in read mode
file = open("daba1.csv", "r+")
replacement=""
# using the for loop
for line in file:
	print(line)
	if 'Tux' in line:
		#line.replace("")
		changes = line.replace('"Tux","15.99","10"', '"Tux","15.99","10000000"')
	else:
		changes = line
	replacement = replacement + changes + "\n"

file.close()
# opening the file in write mode
fout = open("daba1.csv", "w")
fout.write(replacement)
fout.close()

	

