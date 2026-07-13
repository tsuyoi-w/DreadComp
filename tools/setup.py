#!/usr/bin/env python3

import argparse
import hashlib
from pathlib import Path
import subprocess
from typing import Optional
import platform
from pathlib import Path
import subprocess
import tarfile
import sys
import tempfile
import urllib.request
from clean import clean
import objdiff as obj

ROOT = Path(__file__).parent.parent
TARGET_PATH = ROOT / 'data' / 'main.nso'
TARGET_ELF_PATH = ROOT / 'data' / 'main.elf'
TOOL_ROOT = ROOT / 'toolchain'

SYSTEM = 'linux' if platform.system() == 'Linux' else 'macos' 

def _convert_nso_to_elf(nso_path: Path, elf_out_path = TARGET_ELF_PATH, uncompressed_nso_out_path = TARGET_PATH):
    NX2ELF = TOOL_ROOT / 'nx-decomp-tools-binaries' / SYSTEM / 'nx2elf'
    print(">>>> converting NSO to ELF...")
    command = [NX2ELF, str(nso_path), "--export-elf", elf_out_path];
    if uncompressed_nso_out_path is not None:
        command.append("--export-uncompressed")
        command.append(uncompressed_nso_out_path)
    subprocess.check_call(command)

def _decompress_nso(nso_path: Path, dest_path: Path):
    HACTOOL = TOOL_ROOT / 'nx-decomp-tools-binaries' / SYSTEM / 'hactool'
    print(">>>> decompressing NSO...")
    subprocess.check_call([HACTOOL, "-tnso",
                           "--uncompressed=" + str(dest_path), str(nso_path)])

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

def create_build_dir():
    build_dir = ROOT / "build"
    if build_dir.is_dir():
        print(">>> build directory already exists: nothing to do")
        return

    subprocess.check_call(
        "cmake -GNinja -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_TOOLCHAIN_FILE=toolchain/ToolchainNX64.cmake -DCMAKE_CXX_COMPILER_LAUNCHER=ccache -B build/".split(" "))
    print(">>> created build directory")

def set_up_compiler(version):
    compiler_dir = ROOT / "toolchain" / ("clang-"+version)
    if compiler_dir.is_dir():
        print(">>> clang is already set up: nothing to do")
        return

    system = platform.system()
    machine = platform.machine()

    if version == "9.0.0":
        builds = {
            # Linux
            ("Linux", "x86_64"): {
                "url": "https://releases.llvm.org/9.0.0/clang+llvm-9.0.0-x86_64-linux-gnu-ubuntu-18.04.tar.xz",
                "dir_name": "clang+llvm-9.0.0-x86_64-linux-gnu-ubuntu-18.04",
            },
            ("Linux", "aarch64"): {
                "url": "https://releases.llvm.org/9.0.0/clang+llvm-9.0.0-aarch64-linux-gnu.tar.xz",
                "dir_name": "clang+llvm-9.0.0-aarch64-linux-gnu",
            },

            # macOS
            ("Darwin", "x86_64"): {
                "url": "https://releases.llvm.org/9.0.0/clang+llvm-9.0.0-x86_64-darwin-apple.tar.xz",
                "dir_name": "clang+llvm-9.0.0-x86_64-apple-darwin",
            }
        }
    elif version == "10.0.0":
        builds = {
            # Linux
            ("Linux", "x86_64"): {
                "url": "https://github.com/llvm/llvm-project/releases/download/llvmorg-10.0.0/clang+llvm-10.0.0-x86_64-linux-gnu-ubuntu-18.04.tar.xz",
                "dir_name": "clang+llvm-10.0.0-x86_64-linux-gnu-ubuntu-18.04",
            },
            ("Linux", "aarch64"): {
                "url": "https://github.com/llvm/llvm-project/releases/download/llvmorg-10.0.0/clang+llvm-10.0.0-aarch64-linux-gnu.tar.xz",
                "dir_name": "clang+llvm-10.0.0-aarch64-linux-gnu",
            },

            # macOS
            ("Darwin", "x86_64"): {
                "url": "https://github.com/llvm/llvm-project/releases/download/llvmorg-10.0.0/clang+llvm-10.0.0-x86_64-apple-darwin.tar.xz",
                "dir_name": "clang+llvm-10.0.0-x86_64-apple-darwin",
            }
        }
    elif version == "11.0.0":
        builds = {
            # Linux
            ("Linux", "x86_64"): {
                "url": "https://github.com/llvm/llvm-project/releases/download/llvmorg-11.0.0/clang+llvm-11.0.0-x86_64-linux-gnu-ubuntu-20.04.tar.xz",
                "dir_name": "clang+llvm-11.0.0-x86_64-linux-gnu-ubuntu-20.04",
            },
            ("Linux", "aarch64"): {
                "url": "https://github.com/llvm/llvm-project/releases/download/llvmorg-11.0.0/clang+llvm-11.0.0-aarch64-linux-gnu.tar.xz",
                "dir_name": "clang+llvm-11.0.0-aarch64-linux-gnu",
            },

            # macOS
            ("Darwin", "x86_64"): {
                "url": "https://github.com/llvm/llvm-project/releases/download/llvmorg-11.0.0/clang+llvm-11.0.0-x86_64-apple-darwin.tar.xz",
                "dir_name": "clang+llvm-11.0.0-x86_64-apple-darwin",
            }
        }
    else:
        builds = {}

    build_info = builds.get((system, machine))
    if build_info is None:
        fail(
            f"unknown platform: {platform.platform()} - {version} (please report if you are on Linux and macOS)")

    url: str = build_info["url"]
    dir_name: str = build_info["dir_name"]

    print(f">>> downloading Clang from {url}...")
    with tempfile.TemporaryDirectory() as tmpdir:
        path = tmpdir + "/" + url.split("/")[-1]
        urllib.request.urlretrieve(url, path)

        print(f">>> extracting Clang...")
        with tarfile.open(path) as f:
            f.extractall(compiler_dir.parent)
            (compiler_dir.parent / dir_name).rename(compiler_dir)

    print(">>> successfully set up Clang")

def main():
    parser = argparse.ArgumentParser(
        "setup.py", description="Set up the Metroid dread decompilation project")
    parser.add_argument("original_nso", type=Path,
                        help="Path to the original NSO (2.1.0, compressed or not)", nargs="?")
    parser.add_argument("--project-only", action="store_true",
                    help="Disable original NSO setup")
    parser.add_argument("--build-only", action="store_true",
                    help="Disable original NSO setup")
    parser.add_argument("--clean", action="store_true",
                    help="Disable original NSO setup")
    args = parser.parse_args()

    config: obj.ProjectConfig = obj.ProjectConfig()

    if args.clean:
        clean()

    if not args.build_only:
        #TODO: obj.generate_objdiff_config()
        if not args.project_only:
            prepare_executable(args.original_nso)
        set_up_compiler("9.0.0")
    create_build_dir()
    
if __name__ == "__main__":
    main()