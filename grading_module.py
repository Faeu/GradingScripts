import os
import importlib
import subprocess
import csv
import io
import contextlib
import re
from colorama import Fore


def grade_script(python_file, sub_dir, tests, solutions, output_only, verbose=None, modify=None, methods=None, repeat=False):
    succ = trials = 0
    answer = 0
    env = load_methods(python_file, methods, repeat=repeat)
    if not env:
        return -1
    for i, test in enumerate(tests):
        trials += 1
        try:
            if modify == 1:
                answer = func_result(test, env, output_only, verbose)
            else:
                if modify == 2:
                    test = modify_test(test, len(tests))
                answer = get_result(f'py "./{sub_dir}/{python_file}"', output_only, test)
                answer = generalize_output(answer)
            if verbose:
                if methods:
                    verbose_lab_output(answer, verbose[i], test)
                else:
                    verbose_lab_output(answer, verbose[i], i)
                continue
        except Exception as e:
            print(repr(e))
            continue

        solution = solutions[trials - 1]
        succ += check_answer(answer, solution)
    print(succ / trials)
    return succ / trials


def get_result(file_name, output_only, test_case=None):
    try:
        result = subprocess.run(file_name, input=test_case, stdout=subprocess.PIPE, timeout=8, text=True)
    except subprocess.TimeoutExpired:
        return("Infinite loop or took too long.")
    if output_only:
        return extract_output(result.stdout)
    return result.stdout


def func_result(test, env, output_only, verbose):
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        answer = [eval(f'module.{test}', {'__builtins__': None}, env)]
    if output_only or (answer[0] is None and f.getvalue() != ""):
        answer = [f.getvalue().strip()]
        if not verbose:
            answer = generalize_output(answer)
    return answer


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
    regex = re.compile(r'[^\w]')
    new_lst = [regex.sub("", line) for line in lst]
    return new_lst


def verbose_lab_output(res, exp, i):
    if type(exp) == list and len(exp) == 1:
        res = res[0]
        exp = exp[0]
    print(Fore.RED, "TEST ", i, Fore.WHITE, sep='')
    print(">>>>>>>>>>>> LAB OUTPUT <<<<<<<<<<<<", Fore.GREEN, sep='')
    print(res)
    print(Fore.WHITE, ">>>>>>>>>> END LAB OUTPUT <<<<<<<<<<", sep='')
    print("========= EXPECTED OUTPUT =========", Fore.CYAN, sep='')
    print(exp)
    print(Fore.WHITE, "======= END EXPECTED OUTPUT =======\n", sep='')


def import_method(file_name, method):
    module = importlib.__import__(file_name[:-3], fromlist=method)
    return module


def validate_dirs(dir):
    for value in dir.values():
        if not os.path.exists(value):
            print('Creating directory:', value)
            os.makedirs(value)


def load_methods(python_file, methods, subm=True, repeat=False):
    if methods:
        try:
            module = import_method(python_file, methods)
            if repeat:
                importlib.reload(module)
            if subm:
                file_info = python_file.split('_')
                id = file_info[1] if 'LATE' not in file_info[1] else file_info[2]
                name = file_info[0]
                env = load_environment(module, name, id)
            else:
                env = load_environment(module)
            env['module'] = module
            return env
        except Exception as e:
            print(repr(e))
            print('Failed loading environment')
            return {}
    return {}


def gen_n(sz):
    n = 0
    while n < sz:
        yield n % 500
        n += 1


def load_solutions(sol_dir):
    return [generalize_output([line.upper().strip() for line in open(f'./{sol_dir}/{sol}', 'r')]) for sol in os.listdir(sol_dir)]


def load_readable_solutions(sol_dir):
    return [open(f'./{sol_dir}/{sol}', 'r').read() for sol in os.listdir(sol_dir)]


def load_tests(test_dir):
    return ["".join([line for line in open(f'./{test_dir}/{test}', 'r')]) for test in os.listdir(test_dir)]


def load_f_tests(test_dir):
    return [line.strip() for line in open(f'./{test_dir}/{os.listdir(test_dir)[0]}')]


def load_environment(module, name=None, n=None):
    load_file = './inputs/load_file.txt'
    if not os.path.isfile(load_file):
        return {}
    with open(load_file) as loadfile:
        if not n:
            n = next(gen)
        var_seq = eval(loadfile.readline(), {}, {})
        method_seq = eval(loadfile.readline(), {}, {})  # Suggested that these methods are used from solution file
        temp_params = {x: getattr(module, x, lambda z: z) for x in method_seq}
        temp_params['id'] = n
        temp_params['name'] = name
        l_params = {}
        for i, row in enumerate(loadfile):
            l_params[var_seq[i]] = eval(row, {}, temp_params)
        return l_params


def file_check(name, id, file_sol, verbose=False):
    n = '{n}'
    if verbose:
        print(Fore.YELLOW, '******** TESTING FILES *********', Fore.WHITE, sep='')
    output_base = f'./outputs/{name}_{id}_output_file_{n}.txt'
    grade = check_files(file_sol, output_base)
    if grade == 1:
        print(Fore.CYAN, "Files are good.", Fore.WHITE, sep='')
    if verbose:
        print(Fore.YELLOW, '******* END FILE TESTING *******', Fore.WHITE, sep='')
    return grade


def load_f_solutions(sol_dir, output_only=False):
    sol = []
    sol_file = os.listdir(sol_dir)[0]
    with open(f"./{sol_dir}/{sol_file}") as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter='`')
        for row in csvreader:
            if row['type'] == 'str':
                sol.append([row['res']])
            elif row['type'] == 'NoneType' or row['type'] == 'list' or row['type'] == 'print':
                sol.append([eval(row['res'], {}, {})])
            else:
                sol.append([eval(f"{ row['type'] }( { row['res'] } )", {}, {})])
        if output_only:
            sol = list(map(generalize_output, sol))
        return sol


def check_files(solution, file_base):
    try:
        num = len(solution)
        answer = [generalize_output([line.upper().strip() for line in open(file_base.format(n=n), 'r')]) for n in range(num)]
    except Exception as e:
        print(repr(e))
        return 0
    return check_answer(answer, solution)


def modify_test(test, num_tests):
    n = next(gen)
    test = test.replace('.csv', f'{n}.csv', 1)  # Make the first line (file), slightly different for each lab
    return test


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


gen = gen_n(10000)
