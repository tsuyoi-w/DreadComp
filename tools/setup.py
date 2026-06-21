#!/usr/bin/env python3

import argparse
import hashlib
import shutil
import os
from pathlib import Path
import subprocess
from typing import Optional
from common import setup_common as setup

TARGET_PATH = setup.get_target_path()
BASE_ELF_PATH = setup.get_target_elf_path()
TARGET_ELF_PATH = setup.get_target_elf_path()

def prepare_executable(original_nso: Optional[Path]):

    COMPRESSED_V100_HASH = "8f0064d97a8b55d6bb681d9ddadea3ece197514c69272cbed334a879a575e851"
    COMPRESSED_V210_HASH = "06872d2061f2529d7cefb7508be2fdaa50b027bad16e238a6414180eae8d3489"
    UNCOMPRESSED_V210_HASH = "c2c8d1184eee861052c6f02c4820b51c1ae289fd7f1920522726c405b5254cd3"

    TARGET_HASH = UNCOMPRESSED_V210_HASH

    if TARGET_PATH.is_file() and hashlib.sha256(TARGET_PATH.read_bytes()).hexdigest() == TARGET_HASH and TARGET_ELF_PATH.is_file():
        print(">>> NSO is already set up")
        return

    if original_nso is None:
        setup.fail("please pass a path to the NSO (refer to the readme for more details)")

    if not original_nso.is_file():
        setup.fail(f"{original_nso} is not a file")

    nso_data = original_nso.read_bytes()
    nso_hash = hashlib.sha256(nso_data).hexdigest()

    if nso_hash == COMPRESSED_V100_HASH:
        print(">>> please use V2.1.0 of the game not 1.0.0")
        return
    
    if nso_hash == UNCOMPRESSED_V210_HASH:
        print(">>> found uncompressed 1.5.0 NSO")
        TARGET_PATH.write_bytes(nso_data)

    elif nso_hash == COMPRESSED_V210_HASH:
        print(">>> found compressed 2.1.0 NSO")
        setup._decompress_nso(original_nso, TARGET_PATH)
    else:
        setup.fail(f"unknown executable: {nso_hash}")

    if not TARGET_PATH.is_file():
        setup.fail("internal error while preparing executable (missing NSO); please report")
    if hashlib.sha256(TARGET_PATH.read_bytes()).hexdigest() != TARGET_HASH:
        setup.fail("internal error while preparing executable (wrong NSO hash); please report")

    setup._convert_nso_to_elf(TARGET_PATH)

    if not TARGET_ELF_PATH.is_file():
        setup.fail("internal error while preparing executable (missing ELF); please report")



def create_build_dir():
    build_dir = setup.ROOT / "build"
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
    args = parser.parse_args()

    setup.install_viking()
    if not args.project_only:
        prepare_executable(args.original_nso)
    setup.set_up_compiler("4.0.1")
    create_build_dir()
    
if __name__ == "__main__":
    main()