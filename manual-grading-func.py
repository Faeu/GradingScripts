import os
import subprocess
import sys
import shutil
import yaml
import colorama
from colorama import Style, Fore, Back
import grading_module as gm


with open("base_config.yaml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

dir = cfg['dir']
methods = cfg['methods']
output_only = cfg['output_only']
check_file = cfg['check_file']
modify = cfg['modify']  # 1 is a function  2 is modify tests for output test  anything else is regular output
editor = cfg['editor']

gm.validate_dirs(dir)
solutions = gm.load_f_solutions(dir['sol'])
tests = gm.load_f_tests(dir['test'])
file_sol = gm.load_solutions(dir['sol_out'])
verbose = gm.load_f_solutions(dir['sol'])
target_letter = ''
sys.path.insert(1, f"./{dir['sub']}")

colorama.init()
print(Style.BRIGHT)

gm.print_tests(solutions, tests)
print(Fore.WHITE)

for lab in os.listdir(f"./{dir['sub']}"):
    file_info = lab.split('_')
    if len(file_info) < 2 or '.py' not in lab:
        continue
    if target_letter != '' and file_info[0][0] < target_letter:
        continue
    target_letter = ''
    id = file_info[1] if 'late' not in file_info[1] else file_info[2]
    if 'late' in file_info[1]:
        print('----------LATE LAB----------')
    print(Fore.GREEN, '###################################### NEW LAB ########################################', Fore.WHITE, sep='')
    print(Style.NORMAL, Back.WHITE, Fore.BLACK, f'{file_info[0]}\'s lab #ID: {id}', Back.RESET, Style.BRIGHT, '\n', sep='')
    try:
        temp_grade = 'r'
        repeat = False
        while temp_grade == 'r':
            gm.grade_script(lab, dir['sub'], tests, solutions, output_only, verbose, modify=modify, methods=methods, repeat=repeat)
            if check_file:
                grade = gm.file_check(file_info[0], id, file_sol, verbose)
            temp_grade = 'h'
            repeat = False
            print(Style.NORMAL, Back.WHITE, Fore.BLACK, f'{file_info[0]}\'s lab #ID: {id}', Fore.WHITE, Back.RESET, Style.BRIGHT, '\n', sep='')
            while temp_grade == 'h':
                print('Enter S, R, M, Q, O, H for Help, or nothing to move on.')
                temp_grade = input('Option> ').lower()
                if temp_grade == '':
                    continue
                elif temp_grade == 'q':
                    print('Exiting')
                    sys.exit()
                elif temp_grade == 'm':
                    shutil.move(f"./{dir['sub']}/{lab}", dir['grad'])
                elif temp_grade == 's':  # Create list of skipped?
                    get_letter = input('Enter first letter of last name: ')
                elif temp_grade == 'o':
                    subprocess.run(f"{editor} \"./{dir['sub']}/{lab}\"", shell=True)
                    temp_grade = 'h'
                elif temp_grade == 'r':
                    print('Repeating...')
                    repeat = True
                else:
                    print("""Options:
                    \n - S to start from a different last name.
                    \n - R to repeat the last lab.
                    \n - M to move last lab to graded folder.
                    \n - Q to quit.
                    \n - O to open last lab in text editor, configurable in config file.
                    \n - H to repeat this message.\n""")
                    temp_grade = 'h'
    except Exception as e:
        print(repr(e))
        print('Error occured, exiting')
        sys.exit()
    print()
