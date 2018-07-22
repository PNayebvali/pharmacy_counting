import sys
from operator import itemgetter, add
from collections import namedtuple, Counter
from AuxFunctions import *


# file_name = '/Users/Peyman/Documents/Programming/Python/Codes/pharmacy_counting/insight_testsuite/' \
#             'tests/test_1/input/itcont.txt'

# input_file = sys.argv[1]
# output_file = sys.argv[2]


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
    len_k = len(group_by_key)
    len_u = len(group_by_unique_col)
    len_s = len(group_by_sum_col)
    if len_k == 0:
        raise ValueError('There should be at least 1 column to group the result by')
    elif len_s == 0:
        raise ValueError('There should be at least 1 column for sum aggregation')
    elif len_u == 0 and ignore_unique is False:
        raise ValueError('There should be at least 1 column for unique count aggregation if ignore_unique is False')

    ref_cols = [x.lower() for x in group_by_key + group_by_unique_col + group_by_sum_col]
    count_dict = Counter(ref_cols)
    for k, v in count_dict.items():
        if v != 1:
            print(
                'There should be no duplicates between key,unique count and sum columns for group by operation.\n'
                '{} is duplicate'.format(k))
            quit()
    output_header = ['key_' + str(group_by_key)] + [
        'group_count' if ignore_unique else 'num_unique_' + str(group_by_unique_col)] + ['Total_' + str(x) for x in
                                                                                         group_by_sum_col]
    unique_dict = {}
    output_dict = {}
    Header = namedtuple('Header', ref_cols)
    with open(input_file, 'r') as input_file:
        # index of the ref_cols in the input file header. raises error if not all exist
        col_index = header_index(input_file, ref_cols, sep=sep)
        for line in input_file:
            # if statement skips the empty lines in the input file
            if line.rstrip():
                cur_line = Header(*itemgetter(*col_index)(line.rstrip().upper().split(sep)))
                key_col = tuple(cur_line[:len_k])
                unique_col = tuple(cur_line[len_k:(len_k + len_u)])
                try:
                    sum_col = tuple(int(round(float(cur_line[x]))) for x in range(len_k + len_u, len(ref_cols)))
                except ValueError:
                    print(
                        'Sum columns should be float. at least one of {} is not a float number'.format(
                            cur_line[(len_k + len_u):]))
                    quit()

                unique_id = '-'.join(key_col + unique_col)
                # this line checks to see if the new line includes unique identifier
                is_unique = 0 + ignore_unique if unique_id in unique_dict.keys() else 1
                output_dict[key_col] = tuple(
                    map(add, output_dict.get(key_col, (0,) * (len_s + 1)), (is_unique,) + sum_col))
                unique_dict[unique_id] = unique_dict.get(unique_id, 0) + 1

    return output_header, [k + v for k, v in output_dict.items()]


# if __name__ == "__main__":
#     # reading the command line arguments
#     input_file = '../input/itcont.txt'
#     output_file = '../output/peyman_check.txt'
#     header, body = group_by_aggregator(input_file, group_by_key=('prescriber_last_name',))
#     body_sorted = multiple_sort(body, (2, 0), (0, 1))
#     write_output_to_txt(body_sorted, output_file)
#     test = 'Pey'

if __name__ == "__main__":
    # reading the command line arguments
    args = terminal_parser()
    input_file = args.inputFile
    output_file = args.outputFile
    separator = args.separator
    key_cols = tuple(args.key)
    unique_cols = tuple(args.unique)
    sum_cols = tuple(args.sum)
    ignore_unique = bool(args.ignore_unique)
    header_override = bool(args.output_header_override)

    for k, v in args._get_kwargs():
        if v is not None:
            print(k, v)
    header, body = group_by_aggregator(input_file, sep=separator, group_by_key=key_cols,
                                       group_by_unique_col=unique_cols, group_by_sum_col=sum_cols,
                                       ignore_unique=ignore_unique)
    body_sorted = multiple_sort(body, (2, 0), (0, 1))
    write_output_to_txt(body_sorted, output_file, header, output_header_override=header_override)
