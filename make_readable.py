#Script to put spaces in the right places in a csv
INPUT_FILENAME = input("CSV input file: ")
OUTPUT_FILENAME = input("Output file (will be created): ")
if OUTPUT_FILENAME == "":
	OUTPUT_FILENAME = "output.csv"
with open(INPUT_FILENAME, "r") as input_file, open(OUTPUT_FILENAME, "w") as output_file:
	lines = input_file.readlines()
	for line in lines:
		input_line = line.replace("\n", "").split(",")
		output_line = line.replace("\n", "").split(",")
		for i in range(len(input_line)):
			stage = input_line[i]
			if len(stage) == 1:
				output_line[i] = stage + " "
		output_file.write(",".join(output_line) + "\n")
