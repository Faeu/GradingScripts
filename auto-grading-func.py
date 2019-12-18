
import os
import importlib
import subprocess
import sys
import csv

def grade_script(python_file):
    succ = 0
    trials = 0
    for test in os.listdir(test_dir):
        trials += 1
        lst = loadcsv(f'./{test_dir}/{test}')
        try:
            script = import_method(python_file, method_name)
            answer = script(lst[:-1], lst[-1])
        except Exception as e:
            print(repr(e))
            return 0
        solution = solutions[trials-1]
        succ += check_answer(answer, solution[0])
    return succ/trials

def loadcsv(path):
    with open(path) as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
            lst = []
            for row in csvreader:
                lst.extend(map(int,row))
            return lst

def import_method(file_name, method):
    module = importlib.__import__(file_name[:-3], fromlist=[method])
    return getattr(module, method)

def load_solutions(sol_dir):
    solutions = []
    for sol in os.listdir(sol_dir):
        f = open(f'./{sol_dir}/{sol}', 'r')
        solutions.append(f.readlines())
    return solutions

def check_answer(answer, solution):
    if isinstance(answer, list):
        if len(answer) < len(solution):
            return 0
        for i, sol in enumerate(solution):
            # print(repr(answer[i]))
            # print(repr(sol))
            if sol not in answer[i]:
                return 0
        return 1
    else:
        return 1 if str(answer) in solution else 0


test_dir = 'tests'
sol_dir = 'solutions'
method_name = 'recursive_sum_odd'
point_weight = 4
solutions = load_solutions(sol_dir)
sys.path.insert(0, './submissions/')

for sol in solutions:
    print(sol)

with open('results.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['ID', 'Grade'])

    for lab in os.listdir('./submissions'):
        file_info = lab.split('_')
        id = file_info[1] if 'late' not in file_info[1] else file_info[2]
        # print(lab)
        if '.py' not in lab:
            continue
        grade = grade_script(lab) * point_weight
        if grade != 0:
            print('success')
            csvwriter.writerow([id, grade])
        else:
            print('failure')
            print('Review:', lab)
        print()
        # input()
