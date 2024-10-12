import sys
import os
import subprocess

# ------------------------------------------------------------------------------

class ReturnCode(int):
    pass

class OsPipe(int):
    pass

# ------------------------------------------------------------------------------

def generic_receive(pipe: OsPipe) -> str:
    buffer = os.read(pipe, 1).decode()
    while ('\n' != buffer[-1]):
        buffer += os.read(pipe, 1).decode()
    return buffer.strip()

# ------------------------------------------------------------------------------

class ParentProcess:

    def __init__(self) -> None:
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

    handle = None
    stdin = None
    stdout = None
    stderr = None

    def __init__(self, command: str) -> None:
        
        (stdin_r, stdin_w) = os.pipe()
        os.set_inheritable(stdin_r, True)
        self.stdin = stdin_w

        (stdout_r, stdout_w) = os.pipe()
        self.stdout = stdout_r
        os.set_inheritable(stdout_w, True)
        
        (stderr_r, stderr_w) = os.pipe()
        self.stderr = stderr_r
        os.set_inheritable(stderr_w, True)

        self.handle = subprocess.Popen(
            args=command,
            stdin= stdin_r,
            stdout=stdout_w,
            stderr=stderr_w,
            shell=True
        )
        
    def despawn(self) -> ReturnCode:
        self.handle.terminate()
        self.handle.wait()
        return self.handle.returncode

    def wait(self) -> ReturnCode:
        self.handle.wait()
        return self.handle.returncode

    def send(self, message: str) -> None:
        os.write(self.stdin, f"{message}{os.linesep}".encode())

    def receive(self) -> str :
        return generic_receive(self.stdout)

    def receive_err(self) -> str :
        return generic_receive(self.stderr)

# ------------------------------------------------------------------------------