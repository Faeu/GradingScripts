import os
import importlib
import subprocess
import sys
import csv
import time
from grading_module import *


test_dir = 'tests'
sol_dir = 'solutions'
sub_dir = 'submissions'
point_weight = 4
solutions = load_solutions(sol_dir)
tests = load_tests(test_dir)
verbose = load_readable_solutions(sol_dir)
output_only = False

print_tests(solutions, tests)

with open('results.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['ID', 'Grade', 'Comments'])

    for lab in os.listdir(f'./{sub_dir}'):
        file_info = lab.split('_')
        id = file_info[1] if 'late' not in file_info[1] else file_info[2]
        if 'late' in file_info[1]:
            print('----------LATE LAB----------')
        if '.py' not in lab:
            continue
        print('###################################### NEW LAB ########################################')
        print(f'Here is {file_info[0]}\'s lab:')
        try:
            grade_script(lab, sub_dir, tests, solutions, output_only, verbose)
            time.sleep(.5);
            temp_grade = input('Grade> ')
            if temp_grade.lower() == 's' or temp_grade == '': # Create list of skipped?
                continue
            if temp_grade.lower() == 'q':
                break
            grade = int(temp_grade)
            comments = input('Comments> ')
        except Exception as e:
            print(repr(e))
            print('Error occured saving csv.')
            sys.exit()
        print('Writing to CSV...')
        csvwriter.writerow([id, grade, comments])
        print()
