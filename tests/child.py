import os
tests_folder_path = os.path.dirname(os.path.realpath(__file__))
main_folder_path = os.path.dirname(tests_folder_path)

# ------------------------------------------------------------------------------

import sys
sys.path.append(main_folder_path)

import process_bridge

# ------------------------------------------------------------------------------

import time
import sys

# ------------------------------------------------------------------------------

parent = process_bridge.ParentProcess()
parent.send('this is stdout')
parent.send_err('this is stderr')
user_input = parent.receive()
parent.send(f'user input = \'{user_input}\'')
time.sleep(1.0)
parent.send('finishing')
sys.exit(12)

# ------------------------------------------------------------------------------
