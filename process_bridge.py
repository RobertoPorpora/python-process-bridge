import sys
import os

# ------------------------------------------------------------------------------

class ReturnCode(int):
    pass

# ------------------------------------------------------------------------------

class ParentProcess:

    def __init__(self) -> None:
        # sys.stdin = os.fdopen(sys.stdin.fileno(), 'r', buffering=0)
        # sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=0)
        # sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', buffering=0)
        pass
    
    def send(self, message: str) -> None:
        sys.stdout.write(message + os.linesep)
        sys.stdout.flush()

    def send_err(self, message: str) -> None:
        sys.stderr.write(message + os.linesep)
        sys.stderr.flush()

    def receive(self) -> str :
        return sys.stdin.readline().strip()

# ------------------------------------------------------------------------------

class ChildProcess:

    def __init__(command: str) -> None:
        raise Exception('This method is not implemented.')

    def despawn(self) -> ReturnCode:
        raise Exception('This method is not implemented.')

    def wait(self) -> ReturnCode:
        raise Exception('This method is not implemented.')

    def send(self, message: str) -> None:
        raise Exception('This method is not implemented.')

    def receive(self) -> str :
        raise Exception('This method is not implemented.')

    def receive_err(self) -> str :
        raise Exception('This method is not implemented.')

# ------------------------------------------------------------------------------