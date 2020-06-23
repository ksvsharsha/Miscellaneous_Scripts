from csv import reader
import re

input_file_path = input('Enter the required file name :') # DQ-1009 - Invalid-URL-Npm.csv
with open('output.csv', mode='w', newline='') as output_file:
    with open(input_file_path, 'r') as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
            lst = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", str(row))
            if len(lst) > 0:
                output_file.write('{}\n'.format(lst[0]))
        print('\nOutput file written to output.csv')
