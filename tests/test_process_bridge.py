import os
tests_folder_path = os.path.dirname(os.path.realpath(__file__))
main_folder_path = os.path.dirname(tests_folder_path)
child_path = os.path.join(tests_folder_path, 'child.py')

# ------------------------------------------------------------------------------

import sys
sys.path.append(main_folder_path)

import process_bridge

# ------------------------------------------------------------------------------

import unittest

# ------------------------------------------------------------------------------

import time

def timer_reset() -> float:
    return time.time()

def timer_elapsed(timer: float) -> float:
    return (timer_reset() - timer)

# ------------------------------------------------------------------------------

class TestProcessBridge(unittest.TestCase):
    def test_despawned(self):
        child = process_bridge.ChildProcess(f"python {child_path}")
        self.assertEqual("this is stdout", child.receive())
        self.assertEqual("this is stderr", child.receive_err())
        timer = time.time()
        child.send("something")
        self.assertEqual("user input = \'something\'", child.receive())
        self.assertNotEqual(12, child.despawn())
        self.assertLess(timer_elapsed(timer), 1.0)

    def test_waited(self):
        child = process_bridge.ChildProcess(f"python {child_path}")
        self.assertEqual("this is stdout", child.receive())
        self.assertEqual("this is stderr", child.receive_err())
        timer = time.time()
        child.send("other things")
        self.assertEqual("user input = \'other things\'", child.receive())
        self.assertEqual(12, child.wait())
        self.assertGreaterEqual(timer_elapsed(timer), 1.0)

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()