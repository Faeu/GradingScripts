
import os
import importlib
import subprocess
import sys
from grading_module import *

def prepare(python_file, tests, sol_dir, output_only=None):
    module = import_method(python_file, method_name)
    env = load_environment(module)
    env['module'] = module
    with open(f'./{sol_dir}/solution', 'w') as output_file:
        output_file.write("type:res\n")
        for test in tests:
            try:
                f = io.StringIO()
                obj_type = 'str'
                print(test)
                with contextlib.redirect_stdout(f):
                    answer = eval(f'module.{test}', {'__builtins__': None}, env)
                    print(answer)
                    obj_type = type(answer).__name__
                if output_only:
                    answer = f.getvalue()
                output_file.write(f"{obj_type}:{str(answer)}\n")
            except Exception as e:
                print(repr(e))

dir = {
    'test' : 'tests',
    'sol' : 'solutions',
    'sub' : 'submissions',
    'cor' : 'correct_submissions'
}
tests = load_f_tests(dir['test'])
print(tests)
method_name = ['clean_words', 'read_file', 'write_file']
python_file = sys.argv[1]
output_only = False

prepare(python_file, tests, dir['sol'])
