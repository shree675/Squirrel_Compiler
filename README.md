# Squirrel_Compiler

## About
A modern compiler written in python for the Squirrel language created by us. Check [Language Manual](https://github.com/shree675/Squirrel_Compiler/tree/primary/LanguageManual) for more information.

## Features
* Supports three levels of optimization such as elimination of redundant LOAD/STORE operations, repeated and unused labels, redundant goto statements and also performs dead-code elimination.
* Supports multi-dimensional arrays and recursion.
* Supports boolean expressions occurring on the RHS of an equation.
* Supports method overriding.
* Supports implicit and explicit type casting.
* Provides support for compiling multiple *.sq* files in a single command with configurable level of optimization.
* Provides an in-built library called *math.acorn*.
* Provides detailed semantic error messages.

### Project Structure

The project is organized into various folders:

main.py is the starting point for the compilation.

Test cases, Language Manual, Standard Library

The remaining folders correspond to each of the phases of the compilation:
Lexical Analysis, Syntax and Semantic Analysis

### Getting Started

1. Clone the repository in `$ROOT`
2. Open a terminal in the `$ROOT` directory
3. Create a Python virtual environment using
   ```
   $ python -m venv env
   ```
4. Activate the environment using
   - On Windows:
   ```
   $ source env/Scripts/activate
   ```
   - On Mac/Linux:
   ```
   $ source env/bin/activate
   ```
5. Install the requirements using
   ```
   $ pip install -r requirements.txt
   ```
6. Install the local packages using
   ```
   $ pip install -e .
   ```
7. Install SPIM for your operating system to run the output produced

## Contributors
* Debeshee
* Aashrith
* Kranthi
* Shreetesh
