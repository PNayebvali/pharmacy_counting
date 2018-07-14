# this files contains all the functionality to read a file do a groupby and sorting and creating an output file
import os

file_name = './insight_testsuite/tests/test_1/input/itcont.txt'


def read_input_to_list(file_name):
    """
    This function reads a text and saves its data in a list
    :param file_name: the input file path
    :return:
    """
    result = []
    with open(file_name, 'r') as input_file:
        result.append(input_file.readline().split())

    return result
