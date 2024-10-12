# Python Process Bridge

**Python Process Bridge** is a lightweight Python library for inter-process communication (IPC) between a parent and child process. This library allows the parent process to send and receive messages via standard input and output streams, and control the child process, including spawning, waiting, and terminating the child process.

## Features

- **Parent Process Management**: Send messages to and receive messages from child processes through standard I/O.
- **Child Process Control**: Spawn child processes, send input, receive output and error messages, and manage process termination.
- **Customizable Communication**: Flexibility to send and receive custom messages in real-time between processes.

## Folder Structure

```
python-process-bridge/
│
├── process_bridge.py           # Main library for process communication
├── README.md                   # Project documentation (this file)
└── tests/                      # Unit tests and example usage
    ├── child.py                # Simulated child process for testing
    ├── run_all_tests.py        # Script to run all tests
    └── test_process_bridge.py  # Unit tests for process_bridge.py
```

## Installation

Clone this repository to your local machine:

```bash
git clone <repository_url>
```

There are no external dependencies for this project, as it only uses Python's standard library.

## Usage

To use the library, you need to create a parent and child process and manage communication between them.

### Example

Here's a basic example of how to use the library:

```python
from process_bridge import ParentProcess, ChildProcess

# Create a parent process
parent = ParentProcess()

# Create a child process that runs a command
child = ChildProcess("python child_script.py")

# Parent sends a message to child
parent.send("Hello from parent")

# Child receives and responds
print(child.receive())         # Output from child's stdout
print(child.receive_err())     # Output from child's stderr

# Clean up
child.despawn()
```

For more examples, see the tests provided in the `tests/` folder.

## Running Tests

Unit tests are provided to ensure the library functions as expected. To run the tests, use the following command:

```bash
python tests/run_all_tests.py
```

This will execute the unit tests defined in `test_process_bridge.py`, which include:

- **`test_despawned`**: Tests the process communication and ensures the child process can be despawned correctly.
- **`test_waited`**: Tests the child process waiting mechanism and verifies the expected behavior after process completion.

## How It Works

### Parent Process (`ParentProcess`)
- The `ParentProcess` class provides methods to send and receive messages via `stdin`, `stdout`, and `stderr`.
  - `send(message)`: Sends a message to the child process via `stdout`.
  - `send_err(message)`: Sends a message to the child process via `stderr`.
  - `receive()`: Reads a message from `stdin`.

### Child Process (`ChildProcess`)
- The `ChildProcess` class manages the spawning, input/output interaction, and termination of the child process.
  - `send(message)`: Sends input to the child process via `stdin`.
  - `receive()`: Reads the child process's output from `stdout`.
  - `receive_err()`: Reads the child process's error output from `stderr`.
  - `despawn()`: Terminates the child process and returns the return code.
  - `wait()`: Waits for the child process to complete and returns the return code.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request for any bug fixes or enhancements.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
