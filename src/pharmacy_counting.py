# this files contains all the functionality to read a file into a list of lists
# then it does a groupby operation and sorts and creates the output
# This might not work fast enough when the input file is large as it runs all
# the mentioned operations in series (no lazy evaluation)
import os
import sys
import itertools
from operator import itemgetter
import csv

file_name = '../insight_testsuite/tests/test_1/input/itcont.txt'


def read_input_to_list(input_file, sep=',', required_cols=None):
    """
    This function reads a text and saves its data in a list
    """
    body = []
    if required_cols is None:
        required_cols = ['id', 'prescriber_last_name', 'prescriber_first_name', 'drug_name', 'drug_cost']
    with open(input_file, 'r') as input_file:
        # this while loop is to skip empty lines at the beginning of the file
        while True:
            input_header = input_file.readline().rstrip().lower().split(sep)
            if input_header != ['']:
                col_index = get_column_index(input_header, required_cols)
                break

        for line in input_file:
            # this if statement skips the empty lines in the input file
            if line.rstrip():
                body.append(change_to_float(itemgetter(*col_index)(line.rstrip().lower().split(sep))))

    return body, required_cols


def change_to_float(input_list):
    """
    Change the content of an iterable to float if valid otherwise keep as it is

    """

    def _floatizer(x):
        """
        Return a float if the item can be converted to float otherwise pass
        """
        try:
            out = float(x)
        except ValueError:
            out = x
        return out

    return [_floatizer(x) for x in input_list]


def group_by_count_sum(input_list, sum_col, *keys):
    """
    This function returns a list of lists of the keys, sum of a column and count based on groupby on the
    input_list
    """
    groups = itertools.groupby(sorted(input_list, key=itemgetter(*keys)), key=itemgetter(*keys))
    return [key_to_list(k) + [sum(i) for i in zip(*[[1, item[sum_col]] for item in g])] for (k, g) in groups]


def group_by_sum(input_list, sum_col, *keys):
    """
    This function returns a list of lists of the keys and count based on groupby on the
    input_list
    """
    groups = itertools.groupby(sorted(input_list, key=itemgetter(*keys)), key=itemgetter(*keys))
    return [key_to_list(k) + [sum(item[sum_col] for item in g)] for (k, g) in groups]


def test_sum(*keys):
    return sum(keys)


def key_to_list(key):
    """
    This function returns a tuple if the key is a string (which means single key has been used only)
    """
    if isinstance(key, str):
        return [key]
    else:
        return list(key)


def get_column_index(ref_list, search_list=None):
    """
    This function returns the indices of the search list within the ref_list, If any of them is not available
    the function print a message
    """
    if search_list is None:
        search_list = ['id', 'prescriber_last_name', 'prescriber_first_name', 'drug_name', 'drug_cost']
    out_list = []
    for val in search_list:
        try:
            out_list.append(ref_list.index(val))
        except ValueError:
            print('{0} is not in the reference list.'.format(val))
            raise
    return out_list


def write_output_to_txt(input_list, output_file, output_header=None):
    """
    This function gets a list of lists and writes each row in a file
    """
    # set the output_header to the defualt output output_header
    if output_header is None:
        output_header = ['drug_name', 'num_prescriber', 'total_cost']

    with open(output_file, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(output_header)
        writer.writerows(input_list)


if __name__ == "__main__":
    body, header = read_input_to_list(file_name)
    output_result = group_by_count_sum(group_by_sum(body, 4, 3, 1, 2), 3, 0)
    write_output_to_txt(output_result,'peyman test1.txt')
    print(body)
    print(header)
    # test = 'peyman'
