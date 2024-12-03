#!/usr/bin/python3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import evaluate_code, print_iterable


file_name = sys.argv[1]
with open(file_name + '.tr') as f:
    code = f.read()
    file_name = file_name if file_name[-1].isdigit() else file_name[:-1]
    with open(file_name + '.' + sys.argv[2]) as f2:
        # arg = f2.read()
        result = evaluate_code(code, [f2])
        print_iterable(result)