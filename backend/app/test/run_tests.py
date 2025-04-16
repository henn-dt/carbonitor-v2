# app/test/run_tests.py
import os
import sys
import unittest

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

if __name__ == '__main__':
    
    test_directory = ['category']

    for dir in test_directory:
        # Find all test files in the folders listed in test_directory, which should be subfolder of where this file is located.
        test_dir = os.path.join(project_root, dir)
        test_suite = unittest.TestLoader().discover(test_dir, pattern='test_*.py')
    
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(test_suite)