import os
import sys

try:
    user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
except KeyError:
    user_paths = []

print("PYTHONPATH: ", user_paths)
print("sys.path: ", sys.path)