#!/usr/bin/env python3

#!##
#! this script delete all file/folder create by setup.py script 
#! use this only if you have an issue,
#! with --clean args in args in setup.py
#! or if there are big update of repo
#!##

import os 
import shutil
from pathlib import Path

ROOT: Path = Path(__file__).parent.parent
Path_array: list[Path] = [
    ROOT / 'build',
    ROOT / 'data' / 'main.nso',
    ROOT / 'data' / 'main.elf',
    ROOT / 'toolchain' / 'clang-10.0.0'
]

def clean():
    for x in Path_array:
        if x.is_file():
            os.remove(x)
            continue
        if x.is_dir():
            shutil.rmtree(x)

if __name__ == "__main__":
    clean()