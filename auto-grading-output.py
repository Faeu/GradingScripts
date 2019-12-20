
import os
import csv
import shutil
import yaml
import colorama
from colorama import Style, Fore
import grading_module as gm

with open("base_config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

dir = cfg['dir']
methods = cfg['methods']
output_only = cfg['output_only']
check_file = cfg['check_file']
modify = cfg['modify']  # 1 is a function 2 is modify tests for output test anything else is regular output
temp_point = input('Points> ')
if temp_point != '':
    cfg['point_weight'] = int(temp_point)
    with open('base_config.yml', 'w') as outfile:
        yaml.dump(cfg, outfile)
point_weight = cfg['point_weight']

gm.validate_dirs(dir)
solutions = gm.load_solutions(dir['sol'])
tests = gm.load_tests(dir['test'])
num_correct = 0
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
        grade = gm.grade_script(lab, dir['sub'], tests, solutions, output_only, modify=modify)
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
