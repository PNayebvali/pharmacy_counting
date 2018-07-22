from operator import itemgetter
import csv
import argparse


def _get_column_index(ref_list, search_list):
    """
    This function returns the indices of the search list within the ref_list, If any of them is not available
    raise a value error

    """
    ref_list = [x.lower() for x in ref_list]
    out_list = []
    for val in search_list:
        try:
            out_list.append(ref_list.index(val))
        except ValueError:
            print('{0} is not in the reference list. Make sure all the groupby columns are present'.format(val))
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


def multiple_sort(input_list, key=set(), ascending=set()):
    """
    sort the a list of iterables on multiple "positional" indexes with different directions

    :param input_list: the list of iterables to be sorted
    :param key: the index iterable
    :param ascending: the direction iterable
    :return: sorted list

    """
    inner_list = input_list[:]
    try:
        len_key = len(key)
    except TypeError:
        print('Both key and ascending arguments should be iterables.')
        return None
    try:
        len_order = len(ascending)
    except TypeError:
        print('Both key and ascending arguments should be iterables.')
        return None
    if len_key != len_order:
        print('key argument and ascending argument MUST be of the same size')
        return None
    if len_order == 0:
        return sorted(input_list)
    for s in reversed(range(len_order)):
        inner_list = sorted(inner_list, key=itemgetter(key[s]), reverse=1 - ascending[s])
    return inner_list


def write_output_to_txt(input_list, output_file,output_header, output_header_override=True):
    """
    This function gets a list of lists and writes each row in a file
    """
    # set the output_header to the default output output_header
    if output_header_override is True:
        output_header = ['drug_name', 'num_prescriber', 'total_cost']

    with open(output_file, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(output_header)
        writer.writerows(input_list)


def terminal_parser():
    parser = argparse.ArgumentParser(description='GroupBy Operation on a text input')
    parser.add_argument('inputFile', type=str, help='relative path to the input file')
    parser.add_argument('outputFile', type=str, help='relative path of the output file')
    parser.add_argument('-sep', '--separator', type=str, help='the delimiter to be used for parsing', default=',')
    parser.add_argument('-k', '--key', type=str, help='group by key columns', nargs='+', default=['drug_name'])
    parser.add_argument('-u', '--unique', type=str, help='group by unique count columns', nargs='+',
                        default=['prescriber_last_name', 'prescriber_first_name'])
    parser.add_argument('-s', '--sum', type=str, help='group by sum aggregation columns', nargs='+',
                        default=['drug_cost'])
    parser.add_argument('-ignore', '--ignore_unique', type=int, choices=[0, 1],
                        help='True if the count should include all not just unique items', default=0)
    parser.add_argument('-oho', '--output_header_override', type=int, choices=[0, 1],
                        help='False if generic header is fine', default=1)
    return parser.parse_args()


if __name__ == '__main__':
    args = terminal_parser()
    for k, v in args._get_kwargs():
        if v is not None:
            print(k, v)
