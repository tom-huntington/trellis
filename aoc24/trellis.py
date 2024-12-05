#!/usr/bin/python3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import evaluate_code, print_iterable


# file_name = sys.argv[1]
file_name = "d5"
extension = "in" 
# extension = "ex" 
# extension = sys.argv[2]
base_path = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(base_path, file_name + '.tr')) as f:
    code = f.read()
    file_name = file_name if file_name[-1].isdigit() else file_name[:-1]
    with open(os.path.join(base_path, file_name + '.' + extension)) as f2:
        # arg = f2.read()
        result = evaluate_code(code, [f2])
        globals()['r'] = result
        print_iterable(result)
