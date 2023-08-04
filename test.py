import sys
import os
from pathlib import Path

print(f'sys.argv[0]: {os.path.dirname(sys.argv[0])}')
print(f'__file__: {os.path.dirname(__file__)}')
print(f'os.getcwd(): {os.getcwd()}')

test_dir = 'test_dir'
cwd = os.path.dirname(sys.argv[0])
test_path = os.path.join(cwd, test_dir)

print(f'creating directory \'{test_path}\'...')
Path(test_dir).mkdir(exist_ok=True)

data_dir = os.path.join(cwd, 'test_dir')
file_path = os.path.join(data_dir, 'test.txt')

print('creating test.txt...')
with open(file_path, 'w') as f:
    f.write('hello world')
