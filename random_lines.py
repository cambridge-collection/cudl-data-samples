#!/usr/bin/env python3
"""
Usage:
    random_lines [options]

Options:
    -s=SEED
    -n=COUNT
"""

import sys
from random import Random

from docopt import docopt


def main():
    args = docopt(__doc__)

    rand = Random(args['-s'])
    count = 20 if args['-n'] is None else int(args['-n'])
    input_lines = list(sys.stdin)
    lines_indexes = sorted(rand.sample(range(len(input_lines)),
                                       min(count, len(input_lines))))
    for i in lines_indexes:
        print(input_lines[i], end='')


if __name__ == '__main__':
    main()
