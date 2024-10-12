import sys
import os
import threading
import subprocess

# ------------------------------------------------------------------------------

class ReturnCode(int):
    pass

class OsPipe(int):
    pass

# ------------------------------------------------------------------------------

def run(command: str, stdin: OsPipe, stdout: OsPipe, stderr: OsPipe) -> None:
    subprocess.run(
        args=command,
        stdin=stdin, stdout=stdout, stderr=stderr,
        shell=True, text=True)

def generic_receive(pipe: OsPipe) -> str:
    buffer = os.read(pipe, 1).decode()
    while ('\n' != buffer[-1]):
        buffer += os.read(pipe, 1).decode()
    return buffer.strip()

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

    thread_handle = None
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
        
        self.thread_handle = threading.Thread(
            target=run,
            args=[command, stdin_r, stdout_w, stderr_w],
            daemon=True
            )
        self.thread_handle.start()

    def despawn(self) -> ReturnCode:
        raise Exception('This method is not implemented.')

    def wait(self) -> ReturnCode:
        raise Exception('This method is not implemented.')

    def send(self, message: str) -> None:
        os.write(self.stdin, f"{message}\n".encode())

    def receive(self) -> str :
        return generic_receive(self.stdout)

    def receive_err(self) -> str :
        return generic_receive(self.stderr)

# ------------------------------------------------------------------------------