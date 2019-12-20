
import csv
import os
import shutil
import sys

import yaml
import colorama
from colorama import Fore, Style

import grading_module as gm

with open("base_config.yaml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

dir = cfg['dir']
methods = cfg['methods']
output_only = cfg['output_only']
check_file = cfg['check_file']
modify = cfg['modify']  # 1 is a function 2 is modify tests for output test anything else is regular output
temp_point = input('Points> ')
if temp_point != '':
    cfg['point_weight'] = int(temp_point)
    with open('base_config.yaml', 'w') as outfile:
        yaml.dump(cfg, outfile)
point_weight = cfg['point_weight']


gm.validate_dirs(dir)
solutions = gm.load_f_solutions(dir['sol'], output_only=output_only) if modify == 1 else gm.load_solutions(dir['sol'])
tests = gm.load_f_tests(dir['test']) if modify == 1 else gm.load_tests(dir['test'])
file_sol = gm.load_solutions(dir['sol_out']) if check_file else []
verbose = False
num_correct = 0
sys.path.insert(1, f"./{dir['sub']}")
colorama.init()
print(Style.BRIGHT)

gm.print_tests(solutions, tests)

with open('results.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['ID', 'Grade'])
    for lab in os.listdir(f"./{dir['sub']}"):
        file_info = lab.split('_')
        if '.py' not in lab:
            continue
        id = file_info[1] if 'LATE' not in file_info[1] else file_info[2]  # print if late
        print(Fore.WHITE, f'Here is {file_info[0]}\'s lab:', sep='')
        grade = gm.grade_script(lab, dir['sub'], tests, solutions, output_only, modify=modify, methods=methods)
        if check_file:
            grade = (gm.file_check(file_info[0], id, file_sol, verbose) + grade) / 2
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
