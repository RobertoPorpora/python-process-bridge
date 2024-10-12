import os
tests_folder_path = os.path.dirname(os.path.realpath(__file__))
main_folder_path = os.path.dirname(tests_folder_path)

# ------------------------------------------------------------------------------

import subprocess

subprocess.run(['python', '-m', 'unittest'], cwd=tests_folder_path)

# ------------------------------------------------------------------------------
