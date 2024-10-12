import process_bridge

child = process_bridge.ChildProcess("python test_child.py")
print(f"stdout from child = \"{child.receive()}\"")
print(f"stderr from child = \"{child.receive_err()}\"")
print("sending something to child stdin...")
child.send("something")
print(f"stdout from child = \"{child.receive()}\"")
print(f"child despawned, return code = {child.despawn()}")
print()

#----------------------------------------------------------------------

child = process_bridge.ChildProcess("python test_child.py")
print(f"stdout from child = \"{child.receive()}\"")
print(f"stderr from child = \"{child.receive_err()}\"")
print("sending other things to child stdin...")
child.send("other things")
print(f"stdout from child = \"{child.receive()}\"")
print(f"child waited, return code = {child.wait()}")
print()
