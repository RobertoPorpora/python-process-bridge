import process_bridge

child = process_bridge.ChildProcess("python test_child.py")

print(f"stdout from child = \"{child.receive()}\"")

print(f"stderr from child = \"{child.receive_err()}\"")

print("sendin something to child stdin...")
child.send("something")

print(f"stdout from child = \"{child.receive()}\"")

