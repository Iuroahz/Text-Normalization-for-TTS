# list of file names to be combined
file_names = ['data_1.txt', 'data_6.txt', 'data_11.txt', 'data_16.txt', 'data_21.txt']

# open the output file for writing
with open('train_data.txt', 'w') as outfile:

    # iterate through each file
    for file_name in file_names:

        # open the file for reading
        with open(file_name, 'r') as infile:

            # read the entire contents of the file
            contents = infile.read()

            # write the contents to the output file
            outfile.write(contents)

