#!/usr/bin/env python3

import json
import math
import os
import sys
from pathlib import Path
from typing import (
    IO,
    Any,
    Callable,
    Dict,
    List,
    Optional,
    TypedDict,
)

Library = Dict[str, Any]
PrecompiledHeader = Dict[str, Any]

ROOT = Path(__file__).parent.parent

SOURCE_PATH: Path = Path('../src')
BUILD_PATH: Path = Path('CMakeFiles/dread.dir/src')
TARGET_PATH: Path = Path('src')


class Object:
    def __init__(self, base_path: str, completed: bool) -> None:
        self.src_path: Path = SOURCE_PATH / str(base_path+".cpp")
        self.asm_path: Optional[Path] = BUILD_PATH / str(base_path + ".cpp.obj")
        self.target_asm_path: Optional[Path] = str(base_path + '.o')
        
        self.name = self.getName()
        self.completed = completed
    
    def getName(self):
        splitstr: list[str] = str(self.src_path).split("/")
        splitstr.reverse()
        return splitstr[0].split('.')[0]

#* "main": Object("main", False) or if the file is in folder Object("Actor/main", False)
Object_List: Dict[str, Object] = {"main": Object("main", False)}
class ProjectConfig:
    def __init__(self) -> None:
        # Paths
        self.build_dir: Path = BUILD_PATH # Output build files
        self.src_dir: Path = SOURCE_PATH  # C/C++/asm source files
        self.asm_dir: Optional[Path] = TARGET_PATH

    def validate(self) -> None:
        required_attrs = [
            "build_dir",
            "src_dir"
        ]
        for attr in required_attrs:
            if getattr(self, attr) is None:
                sys.exit(f"ProjectConfig.{attr} missing")


def file_is_asm(path: Path) -> bool:
    return path.suffix.lower() == ".s"


def file_is_c(path: Path) -> bool:
    return path.suffix.lower() == ".c"


def file_is_cpp(path: Path) -> bool:
    return path.suffix.lower() in (".cc", ".cp", ".cpp", ".cxx", ".pch++")


def file_is_c_cpp(path: Path) -> bool:
    return file_is_c(path) or file_is_cpp(path)

_listdir_cache = {}

def check_path_case(path: Path):
    parts = path.parts
    if path.is_absolute():
        curr = Path(parts[0])
        start = 1
    else:
        curr = Path(".")
        start = 0

    for part in parts[start:]:
        if curr in _listdir_cache:
            entries = _listdir_cache[curr]
        else:
            try:
                entries = os.listdir(curr)
            except (FileNotFoundError, PermissionError):
                sys.exit(f"Cannot access: {curr}")
            _listdir_cache[curr] = entries

        for entry in entries:
            if entry.lower() == part.lower():
                curr = curr / entry
                break
        else:
            sys.exit(f"Cannot resolve: {path}")

    if path != curr:
        print(f"⚠️  Case mismatch: expected={path} actual={curr}")

# Generate objdiff.json
def generate_objdiff_config() -> None:
    # Load existing objdiff.json
    existing_units = {}
    if Path(ROOT / "build/objdiff.json").is_file():
        with open("build/objdiff.json", "r", encoding="utf-8") as r:
            existing_config = json.load(r)
            existing_units = {unit["name"]: unit for unit in existing_config["units"]}

    objdiff_config: Dict[str, Any] = {
        "custom_make": "ninja",
        "target_dir": TARGET_PATH,
        "base_dir": 'build',
        "build_base": True,
        "build_target": False,
        "watch_patterns": [
            "*.c",
            "*.cc",
            "*.cp",
            "*.cpp",
            "*.cxx",
            "*.c++",
            "*.h",
            "*.hh",
            "*.hp",
            "*.hpp",
            "*.hxx",
            "*.h++",
            "*.pch",
            "*.pch++",
            "*.inc",
            "*.py",
            "*.yml",
            "*.txt",
            "*.json",
        ],
        "units": [],
    }

    def add_unit(
        build_obj: Object
    ) -> None:
        obj_path, obj_name, target_path = build_obj.asm_path, build_obj.name, build_obj.target_asm_path
        unit_config: Dict[str, Any] = {
            "name": obj_name,
            "target_path": target_path,
            "base_path": obj_path,
            "scratch": {
                "platform": "switch",
                "compiler": "clang-8.0.0",
                "ctx_path": ".",
                "build_ctx": False
            },
            "metadata": {
                "complete": False,
                "reverse_fn_order": False,
                "source_path": build_obj.src_path
            }
        }

        # Preserve existing symbol mappings
        existing_unit = existing_units.get(obj_name)
        if existing_unit is not None:
            unit_config["symbol_mappings"] = existing_unit.get("symbol_mappings")

        obj = Object_List.get(build_obj.name)
        if obj is None:
            objdiff_config["units"].append(unit_config)
            return

        src_exists = obj.src_path is not None and obj.src_path.exists()
        if src_exists:
            unit_config["base_path"] = obj.src_obj_path
            unit_config["metadata"]["source_path"] = obj.src_path

        objdiff_config["units"].append(unit_config)

    for obj in Object_List:
        add_unit(Object_List[obj])

    def cleandict(d):
        if isinstance(d, dict):
            return {k: cleandict(v) for k, v in d.items() if v is not None}
        elif isinstance(d, list):
            return [cleandict(v) for v in d]
        else:
            return d

    # Write objdiff.json
    with open(ROOT / 'build' / 'objdiff.json', "w", encoding="utf-8") as w:

        def unix_path(input: Any) -> str:
            return str(input).replace(os.sep, "/") if input else ""

        json.dump(cleandict(objdiff_config), w, indent=2, default=unix_path)

if __name__ == '__main__':
    generate_objdiff_config()