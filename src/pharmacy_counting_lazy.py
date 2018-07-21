# this files contains all the functionality to read a file into a list of lists
# then it does a groupby operation and sorts and creates the output
# This might not work fast enough when the input file is large as it runs all
# the mentioned operations in series (no lazy evaluation)
import os
import sys
import itertools
from operator import itemgetter, add
from collections import namedtuple
import csv

file_name = '/Users/Peyman/Documents/Programming/Python/Codes/pharmacy_counting/insight_testsuite/tests/test_1/input/itcont.txt'

# column names defined in the name scope of the main module
default_col_names = ['id', 'prescriber_last_name', 'prescriber_first_name', 'drug_name', 'drug_cost']


def _get_column_index(ref_list, search_list):
    """
    This function returns the indices of the search list within the ref_list, If any of them is not available
    raise a value error

    """
    out_list = []
    for val in search_list:
        try:
            out_list.append(ref_list.index(val))
        except ValueError:
            print('{0} is not in the reference list.'.format(val))
            raise
    return out_list


def header_index(file, ref_col, sep=','):
    """
    from a file object output the indices of reference header
    """
    while True:
        input_header = file.readline().rstrip().lower().split(sep)
        if input_header != ['']:
            col_index = _get_column_index(input_header, ref_col)
            break
    return col_index


def group_by_aggregator(input_file, sep=',', group_by_key=('drug_name',),
                        group_by_unique_col=('prescriber_first_name', 'prescriber_last_name'),
                        group_by_sum_col=('drug_cost',), ignore_unique=False):
    """
    This function reads line from a file  and returns a grouped by output list of lists as stated in the challenge
    :param input_file: the file path to the input file
    :param sep: the separator. defaults to ','
    :param group_by_key: tuple of columns that we want to group by
    :param group_by_unique_col: tuple of columns that should be unique for count aggregation
    :param group_by_sum_col: tuple of columns to for sum aggregation
    :param ignore_unique: specifies if we should count unique values or all values
    :return: a proper header and a list of lists that includes the resulting group by operation needed
    """
    # Argument Type checks
    if not (isinstance(group_by_key, tuple) and isinstance(group_by_unique_col, tuple) and isinstance(group_by_sum_col,
                                                                                                      tuple)):
        raise TypeError('All the group by columns should be tuple')
    # Argument Value checks
    if len(group_by_key) == 0:
        raise ValueError('There should be at least 1 column to group the result by')
    elif len(group_by_sum_col) == 0:
        raise ValueError('There should be at least 1 column for sum aggregation')
    elif len(group_by_unique_col) == 0 and ignore_unique is False:
        raise ValueError('There should be at least 1 column for unique count  aggregation if ignore_unique is False')

    ref_cols = [x.lower() for x in group_by_key + group_by_unique_col + group_by_sum_col]
    unique_dict = {}
    output_dict = {}
    Header = namedtuple('Header', ref_cols)
    with open(input_file, 'r') as input_file:
        # index of the ref_cols in the input file header. raises error if not all exist
        col_index = header_index(input_file, ref_cols)
        for line in input_file:
            # if statement skips the empty lines in the input file
            if line.rstrip():
                cur_line = Header(*itemgetter(*col_index)(line.rstrip().lower().split(sep)))
                drug_name = cur_line.drug_name.lower()
                drug_cost = float(cur_line.drug_cost)
                unique_id = '-'.join([x.lower() for x in
                                      [cur_line.drug_name, cur_line.prescriber_first_name,
                                       cur_line.prescriber_last_name]])
                # this line checks to see if the new line includes unique prescriber
                is_unique = 0 if unique_id in unique_dict.keys() else 1
                output_dict[drug_name] = list(map(add, output_dict.get(drug_name, [0, 0]), [is_unique, drug_cost]))
                unique_dict[unique_id] = unique_dict.get(unique_id, 0) + 1

    return [], [[k] + v for k, v in output_dict.items()]


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
    write_output_to_txt(output_result, 'peyman test1.txt')
    print(body)
    print(header)
    # test = 'peyman'
