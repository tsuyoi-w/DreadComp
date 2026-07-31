#!/usr/bin/env python3

import subprocess
import os
from pathlib import Path
import platform
import shutil

ROOT: Path = Path(__file__).parent.parent
COMPILE_COMMANDS: Path = ROOT / 'build' / 'compile_commands.json'
COMPILE_COMMANDS_ROOT: Path = ROOT / 'compile_commands.json'

#! if you are on WSL and it wont work pass this to True
WSL: bool = True if platform.platform().__contains__('WSL') else False

#! replace with your current Disk
WINDOWS_PATH: str = "D:/"
WSL_PATH: str = '/mnt/d/'

def fixCompileCommandPath():
    with open(COMPILE_COMMANDS, 'r') as f:
        data = f.read()
        data = data.replace(WSL_PATH, WINDOWS_PATH)

    with open(COMPILE_COMMANDS_ROOT, 'w') as f:
        f.write(data)

def main():
    os.remove(COMPILE_COMMANDS_ROOT)

    subprocess.call(['ninja', '-C', './build'])

    if WSL:
        fixCompileCommandPath()
    else:
        shutil.move(COMPILE_COMMANDS, COMPILE_COMMANDS_ROOT)

if __name__ == "__main__":
    main()