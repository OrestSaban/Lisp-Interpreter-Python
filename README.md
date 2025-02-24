# Lisp Interpreter in Python

A simple Lisp interpreter written in Python. This project implements a basic interpreter for the Lisp programming language, supporting common operations, expressions, and functions. The interpreter uses a custom-built parser and evaluator to process Lisp expressions.

## Features

- Tokenization of Lisp source code
- Expression parsing and evaluation
- Support for basic operations: arithmetic, list manipulation, logical operations
- Functions for handling environment, including `define` and lambda functions
- Built-in functions from Python's `math` module and common Lisp functions
- Error handling with a custom error function

## Getting Started

### Prerequisites

- Python 3.x
- No additional libraries are required, as the project uses only built-in Python libraries.

### Installation

1. Clone the repository:

    ```bash
    [git clone https://github.com/OrestSaban/lisp-interpreter-python.git
    cd lisp-interpreter-python
    ```

2. You can now run the interpreter with any Lisp source code.

### Running the Interpreter

Run the interpreter using the following command:

```bash
python3 compiler.py path_to_lisp_file.lisp
