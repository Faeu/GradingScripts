
import sys
import yaml
import io
import contextlib
from grading_module import load_methods, load_f_tests


def prepare(python_file, tests, sol_dir, output_only=None):
    env = load_methods(python_file, methods, subm=False)
    with open(f'./{sol_dir}/solution', 'w') as output_file:
        output_file.write(f"type{delimiter}res\n")  # Change delimeter
        for test in tests:
            try:
                f = io.StringIO()
                obj_type = 'str'
                print('TEST', test)
                with contextlib.redirect_stdout(f):
                    answer = eval(f'module.{test}', {'__builtins__': None}, env)
                    obj_type = type(answer).__name__
                if output_only or obj_type == 'NoneType':
                    answer = repr(f.getvalue().strip())
                    obj_type = 'print'
                output_file.write(f"{obj_type}{delimiter}{answer}\n")
            except Exception as e:
                print(repr(e))


with open("base_config.yaml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

dir = cfg['dir']
methods = cfg['methods']
output_only = cfg['output_only']
tests = load_f_tests(dir['test'])
python_file = sys.argv[1].replace(".\\", "")  # Clipping off slash
cfg['solution_script'] = python_file
delimiter = '`'

with open('base_config.yaml', 'w') as outfile:
    yaml.dump(cfg, outfile)

prepare(python_file, tests, dir['sol'], output_only=output_only)
