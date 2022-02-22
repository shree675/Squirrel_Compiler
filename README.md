# Squirrel_Compiler

### Project Structure
The project is organized into various folders:

main.py is the starting point for the compilation. 

Test cases, Language Manual, Standard Library

The remaining folders correspond to each of the phases of the compilation:
Lexical Analysis, Syntax and Semantic Analysis

### Getting Started
1. Clone the repository in ```$ROOT```
2. Open a terminal in the ```$ROOT``` directory
3. Create a Python virual environment using 
   ```
   python -m venv env
   ```
4. Activate the environment using 
   + On Windows:
   ```
   source env/Scripts/activate
   ```
   + On Mac/Linux:
   ```
   source env/bin/activate
   ``` 
5. Install the requirements using
   ```
   pip install -r requirements.txt
   ```
6. Install the local packages using
   ```
   pip install -e .
   ```