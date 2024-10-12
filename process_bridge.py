import sys
import os
import subprocess

# ------------------------------------------------------------------------------

class ReturnCode(int):
    pass

class OsPipe(int):
    pass

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

    handle: subprocess.Popen = None
    stdin: OsPipe = None
    stdout: OsPipe = None
    stderr: OsPipe = None
    buffer: str = ""

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
        return self.generic_receive(self.stdout)

    def receive_err(self) -> str :
        return self.generic_receive(self.stderr)
    
    def generic_receive(self, pipe: OsPipe) -> str:

        while not os.linesep in self.buffer:
            self.buffer += os.read(pipe, 1024).decode()
        
        position = self.buffer.find(os.linesep)        
        output = self.buffer[:position]        
        self.buffer = self.buffer[position + len(os.linesep):]
        return output
        
# ------------------------------------------------------------------------------