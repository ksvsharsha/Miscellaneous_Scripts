from csv import reader, writer
import ntpath
import os.path
import re
import os
import traceback
import sys


class License_Checker:

    @staticmethod
    def read_input_file():
        try:
            # input_file = input('Enter the input file name with full path :')
            # input_row_no = input('Enter the column no to work on:')
            # valid_licenses_file_path = input('Enter the valid licenses file name with full path :')
            # valid_licenses_row_no = input('Enter the column no to work on:')
            input_file = "D:\Miscellaneous_Scripts\License_Checker\Sample-Input-File-3.csv"
            input_row_no = "2"
            valid_licenses_file_path = "D:\Miscellaneous_Scripts\License_Checker\Approved-List-of-Licenses.csv"
            valid_licenses_row_no = "1"
            valid_licenses_list = []

            with open(valid_licenses_file_path, 'r') as read_obj_valid_licenses:
                if os.path.splitext(ntpath.basename(input_file))[1] == '.csv':
                    csv_tsv_reader_valid_licenses = reader(read_obj_valid_licenses)
                elif os.path.splitext(ntpath.basename(input_file))[1] == '.tsv':
                    csv_tsv_reader_valid_licenses = reader(read_obj_valid_licenses, '\t')
                for each_valid_license in csv_tsv_reader_valid_licenses:
                    valid_licenses_list.append(each_valid_license[int(valid_licenses_row_no)-1])

            input_file_path = ntpath.split(input_file)[0]
            input_file_ext = os.path.splitext(ntpath.basename(input_file))[1]
            output_file = f'{input_file_path}\\output'
            is_csv = True
            if input_file_ext == '.csv':
                output_file = f'{output_file}.csv'
                if os.path.exists(output_file):
                    os.remove(output_file)
            elif input_file_ext == '.tsv':
                is_csv = False
                output_file = f'{output_file}.tsv'
                if os.path.exists(output_file):
                    os.remove(output_file)

            with open(input_file, 'r') as read_obj_input_file, \
                    open(output_file, 'w', newline='') as write_obj_output_file:
                if is_csv:
                    csv_tsv_reader_file = reader(read_obj_input_file)
                    csv_tsv_writer_file = writer(write_obj_output_file)
                else:
                    csv_tsv_reader_file = reader(read_obj_input_file, '\t')
                    csv_tsv_writer_file = writer(write_obj_output_file, '\t')

                for each_input in csv_tsv_reader_file:
                    error_msg = 'Valid License'
                    licenses_list = []
                    licenses_list_unsorted = []
                    str_list = re.split(r'(.*?)(\(.*?\))', each_input[int(input_row_no)-1])
                    list_without_empty_strings = list(filter(None, str_list))
                    for each_str in list_without_empty_strings:

                        if '&' in each_str and ('(' in each_str or ')' in each_str):
                            print('Brackets () present in & separators')
                            error_msg = 'Brackets-() are not allowed when licenses are separated by &'

                        elif '|' in each_str and ('(' not in each_str and ')' not in each_str):
                            print('Brackets () not present in| separator')
                            error_msg = 'Brackets should be enclosed at both ends for pipe(|) separator'

                        elif ('&' in each_str or '|' not in each_str) and ('(' not in each_str and ')' not in each_str):
                            licenses_and = list(filter(None, each_str.split('&')))
                            licenses_and_without_chars = []
                            licenses_and_without_chars_unsorted = []
                            for elem in licenses_and:
                                if elem in valid_licenses_list:
                                    elem = re.sub(r'[^a-z|^A-Z]', '', elem)
                                    licenses_and_without_chars.append(elem)
                                else:
                                    error_msg = 'License not present in License List'
                                    print('License not present in Approved License List')
                            licenses_and_without_chars_unsorted.extend(licenses_and_without_chars)
                            licenses_and_without_chars.sort()

                            if licenses_and_without_chars != licenses_and_without_chars_unsorted:
                                print('Inner and list not sorted')
                                error_msg = 'Alphabetical order not followed'
                            else:
                                licenses_list.extend(licenses_and_without_chars_unsorted)

                        elif ('|' in each_str or '&' not in each_str) and ('(' in each_str and ')' in each_str):
                            licenses_or = each_str.replace('(', '').replace(')', '').split('|')
                            licenses_or_without_chars = []
                            licenses_or_without_chars_unsorted = []
                            for elem in licenses_or:
                                if elem in valid_licenses_list:
                                    elem = re.sub(r'[^a-z|^A-Z]', '', elem)
                                    licenses_or_without_chars.append(elem)
                                else:
                                    error_msg = 'License not present in Approved License List'
                                    print('License not present in Approved License List')
                            licenses_or_without_chars_unsorted.extend(licenses_or_without_chars)
                            licenses_or_without_chars.sort()

                            if licenses_or_without_chars != licenses_or_without_chars_unsorted:
                                error_msg = 'Alphabetical order not followed'
                                print('Alphabetical order not followed')
                            else:
                                licenses_list.extend(licenses_or_without_chars_unsorted)

                    licenses_list_unsorted.extend(licenses_list)
                    licenses_list.sort()

                    if licenses_list != licenses_list_unsorted:
                        print('Alphabetical order not followed')
                        error_msg = 'Alphabetical order not followed'

                    output_row = []
                    output_row.extend(each_input)
                    output_row.append(error_msg)
                    csv_tsv_writer_file.writerow(output_row)

                read_obj_input_file.close()
                read_obj_valid_licenses.close()
                write_obj_output_file.close()
            return
        except Exception:
            read_obj_input_file.close()
            read_obj_valid_licenses.close()
            write_obj_output_file.close()
            traceback.print_exc(limit=1, file=sys.stdout)


License_Checker.read_input_file()
