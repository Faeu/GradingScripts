
import os
import csv
import shutil
from grading_module import *

test_dir = 'tests'
sol_dir = 'solutions'
sub_dir = 'submissions'
point_weight = 6
solutions = load_solutions(sol_dir)
tests = load_tests(test_dir)
output_only = True
verbose = False

print_tests(solutions, tests)

with open('results.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['ID', 'Grade'])

    for lab in os.listdir(f'./{sub_dir}'):
        file_info = lab.split('_')
        id = file_info[1] if 'LATE' not in file_info[1] else file_info[2] # print if late
        if '.py' not in lab:
            continue
        print(f'Here is {file_info[0]}\'s lab:')
        grade = grade_script(lab, sub_dir, tests, solutions, output_only)
        if grade == 1:
            print('success')
            csvwriter.writerow([id, point_weight])
            shutil.move(f'./{sub_dir}/{lab}', './correct_submissions')
        else:
            print('failure')
            print('Review:', lab)
        print()
