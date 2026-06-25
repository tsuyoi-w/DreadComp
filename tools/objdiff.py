#!/usr/bin/env python3

###
# decomp-toolkit project generator
# Generates build.ninja and objdiff.json.
#
# This generator is intentionally project-agnostic
# and shared between multiple projects. Any configuration
# specific to a project should be added to `configure.py`.
#
# If changes are made, please submit a PR to
# https://github.com/encounter/dtk-template
###

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

SOURCE_PATH: Path = '../src'
BUILD_PATH: Path = 'CMakeFiles/dread.dir/src' 
TARGET_PATH: Path = 'src'


class Object:
    def __init__(self, src_path: Path, name: str, completed: bool) -> None:
        self.name = name
        self.completed = completed

        self.src_path: Path = Path(src_path)
        self.asm_path: Optional[Path] = BUILD_PATH + "/" + str(src_path).replace('.cpp', '.cpp.obj')
        self.target_asm_path: Optional[Path] = TARGET_PATH + "/" + str(src_path).replace('.cpp', '.o')

    # def resolve(self, config: "ProjectConfig", lib: Library) -> "Object":
    #     # Use object options, then library options
    #     obj = Object(self.completed, self.name, **lib)
    #     for key, value in self.options.items():
    #         if value is not None or key not in obj.options:
    #             obj.options[key] = value

    #     # Use default options from config
    #     def set_default(key: str, value: Any) -> None:
    #         if obj.options[key] is None:
    #             obj.options[key] = value

    #     set_default("add_to_all", True)
    #     set_default("asflags", config.asflags)
    #     set_default("asm_dir", config.asm_dir)
    #     set_default("extab_padding", None)
    #     set_default("scratch_preset_id", config.scratch_preset_id)
    #     set_default("shift_jis", config.shift_jis)
    #     set_default("src_dir", config.src_dir)

    #     # Resolve paths
    #     build_dir = config.out_path()
    #     obj.src_path = Path(obj.options["src_dir"]) / obj.options["source"]
    #     if obj.options["asm_dir"] is not None:
    #         obj.asm_path = (
    #             Path(obj.options["asm_dir"]) / obj.options["source"]
    #         ).with_suffix(".s")
    #     base_name = Path(self.name).with_suffix("")
    #     obj.src_obj_path = build_dir / "src" / f"{base_name}.o"
    #     obj.asm_obj_path = build_dir / "mod" / f"{base_name}.o"
    #     obj.ctx_path = build_dir / "src" / f"{base_name}.ctx"
    #     return obj
    
#! EXEMPLE: "main": Object("src/main.cpp", "Main", False)

Object_List: Dict[str, Object] = {
    'main': Object('noerror.cpp', 'Main',False)
}

class ProjectConfig:
    def __init__(self) -> None:
        # Paths
        self.build_dir: Path = BUILD_PATH # Output build files
        self.src_dir: Path = SOURCE_PATH  # C/C++/asm source files
        self.asm_dir: Optional[Path] = TARGET_PATH

        # Tooling
        self.binutils_tag: Optional[str] = None  # Git tag
        self.binutils_path: Optional[Path] = None  # If None, download
        self.dtk_tag: Optional[str] = None  # Git tag
        self.dtk_path: Optional[Path] = None  # If None, download
        self.compilers_tag: Optional[str] = None  # 1
        self.compilers_path: Optional[Path] = None  # If None, download
        self.wibo_tag: Optional[str] = None  # Git tag
        self.wrapper: Optional[Path] = None  # If None, download wibo on Linux
        self.sjiswrap_tag: Optional[str] = None  # Git tag
        self.sjiswrap_path: Optional[Path] = None  # If None, download
        self.ninja_path: Optional[Path] = None  # If None, use system PATH
        self.objdiff_tag: Optional[str] = None  # Git tag
        self.objdiff_path: Optional[Path] = None  # If None, download

        # Project config
        self.non_matching: bool = False
        self.build_rels: bool = True  # Build REL files
        self.generate_map: bool = False  # Generate map file(s)
        self.asflags: Optional[List[str]] = None  # Assembler flags
        self.precompiled_headers: Optional[List[PrecompiledHeader]] = (
            None  # List of precompiled headers
        )
        self.warn_missing_config: bool = False  # Warn on missing unit configuration
        self.warn_missing_source: bool = False  # Warn on missing source file
        self.rel_strip_partial: bool = True  # Generate PLFs with -strip_partial
        self.rel_empty_file: Optional[str] = (
            None  # Object name for generating empty RELs
        )
        self.shift_jis = (
            True  # Convert source files from UTF-8 to Shift JIS automatically
        )
        self.reconfig_deps: Optional[List[Path]] = (
            None  # Additional re-configuration dependency files
        )
        self.custom_build_rules: Optional[List[Dict[str, Any]]] = (
            None  # Custom ninja build rules
        )
        self.custom_build_steps: Optional[Dict[str, List[Dict[str, Any]]]] = (
            None  # Custom build steps, types are ["pre-compile", "post-compile", "post-link", "post-build"]
        )
        self.generate_compile_commands: bool = (
            True  # Generate compile_commands.json for clangd
        )
        self.extra_clang_flags: List[str] = []  # Extra flags for clangd
        self.scratch_preset_id: Optional[int] = (
            None  # Default decomp.me preset ID for scratches
        )
        self.link_order_callback: Optional[Callable[[int, List[str]], List[str]]] = (
            None  # Callback to add/remove/reorder units within a module
        )
        self.context_exclude_globs: List[
            str
        ] = []  # Globs to exclude from context files
        self.context_defines: List[
            str
        ] = []  # Macros to define at the top of context files

        # Progress output and report.json config
        self.progress = True  # Enable report.json generation and CLI progress output
        self.progress_each_module: bool = (
            False  # Include individual modules, disable for large numbers of modules
        ) # Additional categories
        self.progress_report_args: Optional[List[str]] = (
            None  # Flags to `objdiff-cli report generate`
        )

        # Progress fancy printing
        self.progress_use_fancy: bool = False
        self.progress_code_fancy_frac: int = 0
        self.progress_code_fancy_item: str = ""
        self.progress_data_fancy_frac: int = 0
        self.progress_data_fancy_item: str = ""

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


def make_flags_str(flags: Optional[List[str]]) -> str:
    if flags is None:
        return ""
    return " ".join(flags)

# Unit configuration
class BuildConfigUnit(TypedDict):
    object: Optional[str]
    name: str
    autogenerated: bool


# Module configuration
class BuildConfigModule(TypedDict):
    name: str
    module_id: int
    ldscript: str
    entry: str
    units: List[BuildConfigUnit]


# Module link configuration
class BuildConfigLink(TypedDict):
    modules: List[str]


# Build configuration generated by decomp-toolkit
class BuildConfig(BuildConfigModule):
    version: str
    modules: List[BuildConfigModule]
    links: List[BuildConfigLink]

# Generate objdiff.json
def generate_objdiff_config(
    config: ProjectConfig,
) -> None:
    # Load existing objdiff.json
    existing_units = {}
    if Path(ROOT / "build/objdiff.json").is_file():
        with open("build/objdiff.json", "r", encoding="utf-8") as r:
            existing_config = json.load(r)
            existing_units = {unit["name"]: unit for unit in existing_config["units"]}

    if config.ninja_path:
        ninja = str(config.ninja_path.absolute())
    else:
        ninja = "ninja"

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
                "reverse_fn_order": False
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

        # Filter out include directories
        def keep_flag(flag):
            return (
                not flag.startswith("-i ")
                and not flag.startswith("-i-")
                and not flag.startswith("-I ")
                and not flag.startswith("-I+")
                and not flag.startswith("-I-")
            )

        
        objdiff_config["units"].append(unit_config)

    for obj in Object_List:
        print(Object_List)
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

# Print progress information from objdiff report
def calculate_progress(config: ProjectConfig) -> None:
    config.validate()
    out_path = config.out_path()
    report_path = out_path / "report.json"
    if not report_path.is_file():
        sys.exit(f"Report file {report_path} does not exist")

    report_data: Dict[str, Any] = {}
    with open(report_path, "r", encoding="utf-8") as f:
        report_data = json.load(f)

    # Convert string numbers (u64) to int
    def convert_numbers(data: Dict[str, Any]) -> None:
        for key, value in data.items():
            if isinstance(value, str) and value.isdigit():
                data[key] = int(value)

    convert_numbers(report_data["measures"])

    # Output to GitHub Actions job summary, if available
    summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    summary_file: Optional[IO[str]] = None
    if summary_path:
        summary_file = open(summary_path, "a", encoding="utf-8")
        summary_file.write("```\n")

    def progress_print(s: str) -> None:
        print(s)
        if summary_file:
            summary_file.write(s + "\n")

    # Print human-readable progress
    progress_print("Progress:")

    if config.progress_use_fancy:
        measures = report_data["measures"]
        total_code = measures.get("total_code", 0)
        total_data = measures.get("total_data", 0)
        if total_code == 0 or total_data == 0:
            return
        code_frac = measures.get("complete_code", 0) / total_code
        data_frac = measures.get("complete_data", 0) / total_data

        progress_print(
            "\nYou have {} out of {} {} and {} out of {} {}.".format(
                math.floor(code_frac * config.progress_code_fancy_frac),
                config.progress_code_fancy_frac,
                config.progress_code_fancy_item,
                math.floor(data_frac * config.progress_data_fancy_frac),
                config.progress_data_fancy_frac,
                config.progress_data_fancy_item,
            )
        )


test: ProjectConfig = ProjectConfig()

if __name__ == '__main__':
    generate_objdiff_config(test)