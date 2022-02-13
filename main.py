"""This file is responsible for running the compiler.
    It contains the main method and all the various flags that can be used."""

import sys
from LexicalAnalysis import lexer


def main(*argv):
    print('Arguments:', argv)


if __name__ == "__main__":
    main(sys.argv)

# Note: I intend to change this structure entirely.
