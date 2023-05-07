#Script to generate the template for the stupid test
number_of_lines = int(input("Number of lines of asm code: "))
with open("1.csv", "w") as file1, open("2.csv", "w") as file2, open("3.csv", "w") as file3:
	for i in range(number_of_lines):
		line = i * "* ," + "\n"
		file1.write(line)
		file2.write(line)
		file3.write(line)
