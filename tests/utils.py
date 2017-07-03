import sys
import os

def get_file(filename):
    working_path = sys.modules[__name__].__file__
    working_dir = os.path.dirname(working_path)
    return f'{working_dir}/test_files/{filename}'
