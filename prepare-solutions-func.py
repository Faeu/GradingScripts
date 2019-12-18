
import os
import importlib
import subprocess
import sys
import yaml
from grading_module import *

def prepare(python_file, tests, sol_dir, output_only=None):
    module = import_method(python_file, methods)
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


with open("base_config.yaml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

dir = cfg['dir']
methods = cfg['methods']
output_only = cfg['output_only']
tests = load_f_tests(dir['test'])
python_file = sys.argv[1][2:]
cfg['solution_script'] = python_file

with open('base_config.yaml', 'w') as outfile:
    yaml.dump(cfg, outfile)

prepare(python_file, tests, dir['sol'])
