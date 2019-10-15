
import os
import importlib
import subprocess
import sys
import csv

def prepare(python_file, test_dir='tests', sol_dir='solutions'):
     for test in os.listdir(test_dir):
        out = open(f'./{sol_dir}/{test}', 'w')
        test_case = open(f'./{test_dir}/{test}', 'r')
        result = subprocess.Popen(f'py {python_file}', stdin=test_case, stdout=subprocess.PIPE, text=True)
        extract_output(out, result.stdout)
        out.close()

def extract_output(f, stream):
    for line in stream:
            if 'OUTPUT' in line:
                s_index = line.find('OUTPUT')
                l_index = line.find('\n', s_index)
                # print(repr(line[s_index:l_index]))
                f.write(line[s_index:l_index].strip() + '\n')

prepare(sys.argv[1])
