import os
import importlib
import subprocess
import sys
import csv
import time
import colorama
from colorama import Fore, Back, Style

def run_script(python_file, output_only):
    out_stream = subprocess.PIPE if output_only else None
    if len(tests) < 1:
        print(get_result(f"python3 \"./{dir['sub']}/{python_file}\"", None, out_stream))
    else:
        for i, test in enumerate(tests):
            try:
                print(Fore.RED, "TEST ", i+1, Fore.WHITE, sep='')
                print(">>>>>>>>>>>> LAB OUTPUT <<<<<<<<<<<<", Fore.GREEN, sep='')
                answer = get_result(f"python3 \"./{dir['sub']}/{python_file}\"", test, out_stream)
                print(Fore.WHITE, ">>>>>>>>>> END LAB OUTPUT <<<<<<<<<<")
                print("========= EXPECTED OUTPUT =========", Fore.CYAN, sep='')
                print(solutions_r[i])
                print(Fore.WHITE, "======= END EXPECTED OUTPUT =======\n", sep='')
            except Exception as e:
                print(repr(e))
                return 1;



def get_result(file_name, test_case=None, out_stream=subprocess.PIPE):
    try:
        result = subprocess.Popen(file_name, shell=True, stdin=subprocess.PIPE, stdout=out_stream)
        test_case = test_case.encode('utf8')
        # test_case = bytearray[test_case, 'utf8']
        r_sout, r_err = result.communicate(test_case, timeout=8)
    except subprocess.TimeoutExpired:
        result.kill()
        return("Infinite loop or took too long.")
    if out_stream:
        return extract_output(r_sout)
    return ('')

def extract_output(stream):
    output = []
    while 'OUTPUT' in stream:
        s_index = stream.find('OUTPUT')
        l_index = stream.find('\n', s_index)
        output.append(stream[s_index:l_index].strip())
        stream = stream[l_index:]
    return output

def load_solutions(sol_dir):
    return [[line.strip() for line in open(f'./{sol_dir}/{sol}', 'r')] for sol in os.listdir(sol_dir)]

def load_readable_solutions(sol_dir):
    return [open(f'./{sol_dir}/{sol}', 'r').read() for sol in os.listdir(sol_dir)]

def load_tests(test_dir):
    return ["".join([line for line in open(f'./{test_dir}/{test}', 'r')]) for test in os.listdir(dir['test'])]


dir = {
    'test' : 'tests',
    'sol' : 'solutions',
    'sub' : 'submissions',
    'cor' : 'correct_submissions'
}
point_weight = 4
solutions = load_solutions(dir['sol'])
tests = load_tests(dir['test'])
solutions_r = load_readable_solutions(dir['sol'])
output_only = False
verbose = True
colorama.init()
print(Style.BRIGHT, Fore.RED)

for test in tests:
    print(test)
print(Fore.BLUE)
for sol in solutions:
    print(sol)

with open('results.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['ID', 'Grade', 'Comments'])
    sub_list = os.listdir(f"./{dir['sub']}")
    sub_list.sort()

    for lab in sub_list:
        file_info = lab.split('_')
        id = file_info[1] if 'late' not in file_info[1] else file_info[2]
        if 'late' in file_info[1]:
            print('----------LATE LAB----------')
        if '.py' not in lab:
            continue
        print(Fore.GREEN, '###################################### NEW LAB ########################################', Fore.WHITE, sep='')
        print(Style.NORMAL, Back.WHITE, Fore.BLACK, f'{file_info[0]}\'s lab:', Back.RESET, Style.BRIGHT, '\n', sep='')
        try:
            run_script(lab, output_only)
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
