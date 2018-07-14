# this files contains all the functionality to read a file do a groupby and sorting and creating an output file
import os
import sys

file_name = '../insight_testsuite/tests/test_1/input/itcont.txt'


def read_input_to_list(file_name):
    """
    This function reads a text and saves its data in a list
    :param file_name: the input file path
    :return: a list of lists with data
    """
    body = []
    default_header = ['id', 'prescriber_last_name', 'prescriber_first_name', 'drug_name', 'drug_cost']
    with open(file_name, 'r') as input_file:
        # this while loop is to skip empty lines at the beginning of the file
        while True:
            input_header = input_file.readline().rstrip().split(',')
            if input_header != ['']:
                break
        # input_header = input_file.readline().rstrip().split(',')
        # This if statement checks the columns names of the input file
        if input_header != default_header:
            print('{} don\'t match following default:'.format(input_header), default_header)
            sys.exit(0)

        for line in input_file:
            # this if statement skips the empty lines in the input file
            if line.rstrip():
                body.append(line.rstrip().split(','))

    return body, default_header


if __name__ == "__main__":
    # print(os.getcwd())
    # print(read_input_to_list(file_name))
    body, header = read_input_to_list(file_name)
    print(body)
    print(header)
    # test = 'peyman'
