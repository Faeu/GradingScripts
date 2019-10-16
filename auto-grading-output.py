
import os
import csv
import shutil
from grading_module import *

dir = {
    'test' : 'tests',
    'sol' : 'solutions',
    'sub' : 'submissions',
    'cor' : 'correct_submissions'
}
validate_dirs(dir)
point_weight = 6
solutions = load_solutions(dir['sol'])
tests = load_tests(dir['test'])
output_only = True
verbose = False
num_correct = 0
colorama.init()
print(Style.BRIGHT)

print_tests(solutions, tests)

with open('results.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['ID', 'Grade'])

    for lab in os.listdir(f"./{dir['sub']}"):
        file_info = lab.split('_')
        id = file_info[1] if 'LATE' not in file_info[1] else file_info[2] # print if late
        if '.py' not in lab:
            continue
        print(f'Here is {file_info[0]}\'s lab:')
        grade = grade_script(lab, dir['sub'], tests, solutions, output_only)
        if grade == 1:
            print('success')
            num_correct += 1
            csvwriter.writerow([id, point_weight])
            shutil.move(f"./{dir['sub']}/{lab}", dir['cor'])
        else:
            print('failure')
            print('Review:', lab)
        print()

print('Correct Submissions:', num_correct)
