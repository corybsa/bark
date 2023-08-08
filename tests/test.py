import sys
import os
from pathlib import Path


def create_file(prop, value):
    print(f'{prop}: {os.path.dirname(value)}')
    test_dir = f'test_{prop}_dir'
    cwd = os.path.dirname(value)
    test_path = os.path.join(cwd, test_dir)

    print(f'creating directory \'{test_path}\'...')
    Path(test_dir).mkdir(exist_ok=True)

    file_path = os.path.join(test_path, 'test.txt')

    print(f'creating file \'{file_path}\'...')
    with open(file_path, 'w') as f:
        f.write('hello world')


if __name__ == '__main__':
    create_file('sys.argv[0]', sys.argv[0])
