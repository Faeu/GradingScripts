
import os
import importlib
import subprocess
import sys
import csv

def prepare(python_file, test_dir, sol_dir):
     for test in os.listdir(test_dir):
        lst = loadcsv(f'./{test_dir}/{test}')
        try:
            script = import_method(python_file, method_name)
            answer = script(lst[:-1], lst[-1])
            with open(f'./{sol_dir}/{test}', 'w') as f:
                f.write(str(answer))
        except Exception as e:
            print(repr(e))

def loadcsv(path):
    with open(path) as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
            lst = []
            for row in csvreader:
                lst.extend(map(int,row))
            return lst

def import_method(file_name, method):
    module = importlib.__import__(file_name[:-3].strip('.\\'), fromlist=[method])
    return getattr(module, method)


method_name = 'recursive_sum_odd'
prepare(sys.argv[1], sys.argv[2], sys.argv[3])