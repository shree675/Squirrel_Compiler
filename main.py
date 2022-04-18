"""This file is responsible for running the compiler.
    It contains the main method and all the various flags that can be used."""

"""
Multiple files can be compiled at once. Any argument with <filename>.sq will be compiled.

Flags:
1. -p : To save the preprocessed file as preprocessed_<filename>.sq
2. -i : To save the intermediate code as intermediate_<filename>.sq
3. -O1 : To optimize compilation on level 1
4. -O2 : To optimize compilation on level 2
5. -O3 : To optimize compilation on level 3 (default)"""

""" 
Command to run the compiler
python3 main.py [-flags] <filename1>.sq <filename2>.sq ... <filenameN>.sq """

# think about what names to save output file with - lets go with <original filename>.asm or filename.s




import sys
from Preprocessing import preprocessor
from LexicalAnalysis import lexer
from SyntaxAnalysis import parser as Parser
from CodeGeneration import CodeGen
def compile(filename, optimization_level, save_preprocessed_file, save_intermediate_code):
    print(
        f"Compiling {filename} (with optimization level: {optimization_level})")
    with open(filename, "r") as f:
        inputFile = f.read()
    pre = preprocessor.Preprocessor()
    preprcessed_output = pre.preprocess(
        filename, inputFile, save=save_preprocessed_file)

    lex = lexer.Lexer()
    tokens = lex.tokenize(preprcessed_output)
    parser = Parser.Parser()
    if save_intermediate_code:
        parser.output_file = "./Output/" + \
            filename.split("/")[-1].replace(".sq", ".tac")

    # code_generator = CodeGeneration.CodeGeneration()
    # target_code = code_generator.generate_target_code(parser.parse(tokens), optimization_level)

    intermediate_code = parser.parse(tokens)
    symbol_table = parser.symbol_table
    code_generator = CodeGen.CodeGen()
    target_code = code_generator.generate_target_code(
        intermediate_code, symbol_table, optimization_level)

    output_file_path = "./Output/" + \
        filename.split("/")[-1].replace(".sq", ".asm")

    f = open(output_file_path, "w")
    f.write(target_code)
    f.close()


def main(*argv):
    #print('Arguments:', argv[0])
    argv = argv[0]
    optimization_level = 3
    if '-O1' in argv:
        optimization_level = 1
    elif '-O2' in argv:
        optimization_level = 2
    elif '-O3' in argv:
        optimization_level = 3
    #print("Optimizatioin level = ", optimization_level)

    save_preprocessed_file = False
    save_intermediate_code = False
    if '-p' in argv:
        save_preprocessed_file = True
        #print("Need to save preprocessed file.")
    if '-i' in argv:
        save_intermediate_code = True
        #print("Need to save intermediate code file.")

    for arg in argv:
        if arg.endswith('.sq'):
            filename = arg
            #print("Name of the file being compiled = ", filename)
            # print("Compiling...")
            compile(filename, optimization_level,
                    save_preprocessed_file, save_intermediate_code)


if __name__ == "__main__":
    #print("printing sys.argv", sys.argv)
    main(sys.argv)
