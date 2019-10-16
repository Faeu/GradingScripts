import os
import importlib
import subprocess
import sys
import re
import colorama
from colorama import Fore, Back, Style


def grade_script(python_file, sub_dir, tests, solutions, output_only, verbose=None):
    succ = trials = 0
    for i, test in enumerate(tests):
        trials += 1
        try:
            answer = get_result(f'python "./{sub_dir}/{python_file}"', output_only, test)
            if verbose:
                print(Fore.RED, "TEST ", i+1, Fore.WHITE, sep='')
                print(">>>>>>>>>>>> LAB OUTPUT <<<<<<<<<<<<", Fore.GREEN, sep='')
                print(answer)
                print(Fore.WHITE, ">>>>>>>>>> END LAB OUTPUT <<<<<<<<<<", sep='')
                print("========= EXPECTED OUTPUT =========", Fore.CYAN, sep='')
                print(verbose[i])
                print(Fore.WHITE, "======= END EXPECTED OUTPUT =======\n", sep='')
                continue
        except Exception as e:
            print(repr(e))
            return 1;
        solution = solutions[trials-1]
        succ += check_answer(generalize_output(answer), solution)
    print(succ/trials)
    return succ/trials

def get_result(file_name, output_only, test_case=None):
    try:
        result = subprocess.Popen(file_name, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        r_sout, r_err = result.communicate(test_case, timeout=8)
    except subprocess.TimeoutExpired:
        result.kill()
        return("Infinite loop or took too long.")
    if output_only:
        return extract_output(r_sout)
    return r_sout

def extract_output(stream):
    stream = stream.upper() + '\n'
    output = []
    while 'OUTPUT' in stream:
        s_index = stream.find('OUTPUT')
        l_index = stream.find('\n', s_index)
        output.append(stream[s_index:l_index].strip())
        stream = stream[l_index:]
    return output

def generalize_output(lst):
    regex = re.compile('[^\w]')
    new_lst = [regex.sub("", line) for line in lst]
    return new_lst

def validate_dirs(dir):
    for key, value in dir.items():
        if not os.path.exists(value):
            print('Creating directory:', value)
            os.makedirs(value)


def load_solutions(sol_dir):
    return [generalize_output([line.upper().strip() for line in open(f'./{sol_dir}/{sol}', 'r')]) for sol in os.listdir(sol_dir)]

def load_readable_solutions(sol_dir):
    return [open(f'./{sol_dir}/{sol}', 'r').read() for sol in os.listdir(sol_dir)]

def load_tests(test_dir):
    return ["".join([line for line in open(f'./{test_dir}/{test}', 'r')]) for test in os.listdir(test_dir)]

def print_tests(solutions, tests):
    for i, sol in enumerate(solutions):
        print(Fore.RED, f'Test{i} ', tests[i].strip(), sep='')
        print(Fore.BLUE, f'Solution{i} ', sol, sep='')
        print()

def check_answer(answer, solution):
    if len(answer) < len(solution):
        return 0
    for i, sol in enumerate(solution):
        if sol != answer[i]:
            print('failure')
            print(Fore.GREEN, '### Expected: ', sol, sep='')
            print(Fore.RED, '### Received: ', answer[i], Fore.WHITE, sep='')
            return 0
    return 1
