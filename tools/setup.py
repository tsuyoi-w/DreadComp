#!/usr/bin/env python3

import argparse
import hashlib
from pathlib import Path
import subprocess
from typing import Optional
from pathlib import Path
import subprocess
import tarfile
import sys
import tempfile
import urllib.request
from clean import clean

from common.setup_common import install_viking, _convert_nso_to_elf, _decompress_nso, set_up_compiler

ROOT = Path(__file__).parent.parent
TARGET_PATH = ROOT / 'data' / 'main.nso'
TARGET_ELF_PATH = ROOT / 'data' / 'main.elf'
TOOL_ROOT = ROOT / 'toolchain'

def prepare_executable(original_nso: Optional[Path]):

    COMPRESSED_V100_HASH = "8f0064d97a8b55d6bb681d9ddadea3ece197514c69272cbed334a879a575e851"
    COMPRESSED_V210_HASH = "06872d2061f2529d7cefb7508be2fdaa50b027bad16e238a6414180eae8d3489"
    UNCOMPRESSED_V210_HASH = "c2c8d1184eee861052c6f02c4820b51c1ae289fd7f1920522726c405b5254cd3"

    TARGET_HASH = UNCOMPRESSED_V210_HASH

    if TARGET_PATH.is_file() and hashlib.sha256(TARGET_PATH.read_bytes()).hexdigest() == TARGET_HASH and TARGET_ELF_PATH.is_file():
        print(">>> NSO is already set up")
        return

    if original_nso is None:
        original_nso: Path = ROOT / 'Extract' / 'main'

    if not original_nso.is_file():
        fail(f"{original_nso} is not a file")

    nso_data = original_nso.read_bytes()
    nso_hash = hashlib.sha256(nso_data).hexdigest()

    if nso_hash == COMPRESSED_V100_HASH:
        print(">>> please use V2.1.0 of the game not 1.0.0")
        return
    
    if nso_hash == UNCOMPRESSED_V210_HASH:
        print(">>> found uncompressed 2.1.0 NSO")
        TARGET_PATH.write_bytes(nso_data)

    elif nso_hash == COMPRESSED_V210_HASH:
        print(">>> found compressed 2.1.0 NSO")
        _decompress_nso(original_nso, TARGET_PATH)
    else:
        fail(f"unknown executable: {nso_hash}")

    if not TARGET_PATH.is_file():
        fail("internal error while preparing executable (missing NSO); please report")
    if hashlib.sha256(TARGET_PATH.read_bytes()).hexdigest() != TARGET_HASH:
        fail("internal error while preparing executable (wrong NSO hash); please report")

    _convert_nso_to_elf(TARGET_PATH)

    if not TARGET_ELF_PATH.is_file():
        fail("internal error while preparing executable (missing ELF); please report")

def fail(error: str):
    print(">>> " + error)
    sys.exit(1)

def get_build_dir():
    return ROOT / "build"

def create_build_dir():
    build_dir = ROOT / "build"
    if build_dir.is_dir():
        print(">>> build directory already exists: nothing to do")
        return

    subprocess.check_call(
        "cmake -GNinja -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_TOOLCHAIN_FILE=toolchain/ToolchainNX64.cmake -DCMAKE_CXX_COMPILER_LAUNCHER=ccache -B build/".split(" "))
    print(">>> created build directory")

def main():
    parser = argparse.ArgumentParser(
        "setup.py", description="Set up the Metroid dread decompilation project")
    parser.add_argument("original_nso", type=Path,
                        help="Path to the original NSO (2.1.0, compressed or not)", nargs="?")
    parser.add_argument("--project-only", action="store_true",
                    help="Disable original NSO setup")
    parser.add_argument("--clean", action="store_true",
                    help="Disable original NSO setup")
    parser.add_argument("--clang", action="store_true",
                        help="For github actions")
    args = parser.parse_args()

    if args.clean:
        clean()

    if args.clang:
        set_up_compiler("9.0.0")
        return

    if not args.project_only:
        prepare_executable(args.original_nso)
    set_up_compiler("9.0.0")
    install_viking()
    create_build_dir()
    
if __name__ == "__main__":
    main()