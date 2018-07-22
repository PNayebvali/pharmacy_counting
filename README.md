# Table of Contents
1. [Methodology](README.md#Methodology)
2. [Tests](README.md#Tests)
3. [Additional command line Options](README.md#Additional-command-line-Options)



# Methodology

I have used Python to solve this challenge. The problem asks for a simple group by operation but with native data structures. We can use itertools groupby Methodology that comes standard with python. In this case we need to run the groupby operation on text file fully in memory. Instead I decided to calculate with my own algorithm while reading each line.
I read lines from the file and check to see if that datapoint has unique prescriber and new drug_name. Based on the result I update the output dictionary and unique_id.

# Tests

There are 6 tests to check the code under different scenarios (including the base case of insight). Each test does the following:

* test_1: Base test by insight
* test_2: Data case sensitivity check:  All the float columns are case insensitive
* test_3: Sort check: Tests the sorts and their directions according to the specification
* test_4: Header case sensitivity check and Extra columns: The code is case insensitive in headers and can handle extra columns at the end
* test_5: Multiple extra columns and columns reorder: The code is capable of reading in the a file that has it is column order changed from default. As long as all the columns required for groupby are available, the groupby process should go smoothly
* test_6: Blank lines: All the blank lines at the beginning, in the middle or at the end of the file will be skipped

# Additional command line Options

I have extended the functionality of the code to be usable for different formatting and different columns to run groupby on. Below is the list of options available and a sample command line to run it.

* Help: -h or --help can be added to the command to see the list of positional and optional arguments as follows:
    ```
    $ python3 ./src/pharmacy_counting_lazy.py -h
    ```
    This will show the list of arguments as below:
    ```
    usage: pharmacy_counting_lazy.py [-h] [-sep SEPARATOR] [-k KEY [KEY ...]]
                                 [-u UNIQUE [UNIQUE ...]] [-s SUM [SUM ...]]
                                 [-ignore {0,1}] [-oho {0,1}]
                                 inputFile outputFile

    GroupBy Operation on a text input

    positional arguments:
      inputFile             relative path to the input file
      outputFile            relative path of the output file

    optional arguments:
      -h, --help            show this help message and exit
      -sep SEPARATOR, --separator SEPARATOR
                            the delimiter to be used for parsing
      -k KEY [KEY ...], --key KEY [KEY ...]
                            group by key columns
      -u UNIQUE [UNIQUE ...], --unique UNIQUE [UNIQUE ...]
                            group by unique count columns
      -s SUM [SUM ...], --sum SUM [SUM ...]
                            group by sum aggregation columns
      -ignore {0,1}, --ignore_unique {0,1}
                            True if the count should include all not just unique
                            items
      -oho {0,1}, --output_header_override {0,1}
                            False if generic header is fine
    ```

* Delimiter: If the input file is separated by anything other that comma we can specify that by -sep (--separator) argument:
  ```
  python3 ./src/pharmacy_counting_lazy.py ./input/itcont.txt ./output/top_cost_drug.txt -sep ';'
  ```
* GroupBy Keys: The code by default uses drug_name as the groupby key. If we want to have a different key (or Multiple keys) we can use the -k (--key) argument. In the following code we are giving id as the key. (default for this column is "drug_name")
  ```
  python3 ./src/pharmacy_counting_lazy.py ./input/itcont.txt ./output/top_cost_drug.txt -k id
  ```
* GroupBy unique columns: We can specify the headers for unique count. In this case the count number will show the number of unique occurrence across the specified columns within each key. we can use the optional argument -u (--unique) to set these columns. The command line below sets the unique column to prescriber_last_name. (default is ['prescriber_last_name', 'prescriber_first_name']
  ```
  python3 ./src/pharmacy_counting_lazy.py ./input/itcont.txt ./output/top_cost_drug.txt -u prescriber_last_name
  ```
* GroupBy sum columns: In a similar way we can specify which columns we want sum operation to run on within each group by setting -s (--sum) command line argument. In the command line below we sum both drug_cost and id (I know it doesn't make sense to sum the id's but just for demonstration purposes we use them). default for this argument is drug_cost
  ```
  python3 ./src/pharmacy_counting_lazy.py ./input/itcont.txt ./output/top_cost_drug.txt -s drug_cost id
  ```
* ignore_unique: -ignore (--ignore_unique) If this option is 1 the code will simply give the count of all elements within each group ignoring the specified groupby unique columns. default is 0
  ```
  python3 ./src/pharmacy_counting_lazy.py ./input/itcont.txt ./output/top_cost_drug.txt -ignore 1
  ```
* overriding output header: -oho (--output_header_override) This option sets the default for output header to the one that this challenge asks for. If you want to see the generic output header it should be set to 0. if we change any of the GroupBy columns it makes sense not to override the generic output header to avoid confusion. The command line code will look like this:
  ```
  python3 ./src/pharmacy_counting_lazy.py ./input/itcont.txt ./output/top_cost_drug.txt -ignore 1 -oho 0
  ```
