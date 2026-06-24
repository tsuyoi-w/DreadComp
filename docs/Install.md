# Install

**If you're on windows please use WSL**

## dependencies

You'll need the following programming tools:

- Python with pip
- Ninja
- Cmake
- ccache
- xdelta3
- Clang

you can install those dependencies by running :

```shell
sudo apt install python3 ninja-build cmake ccache xdelta3 clang libssl-dev pkg-config
```

You also need:

- A rust toolchain ([follow the instructions here](https://rust-lang.org/tools/install/))
- The following python module: capstone colorama cxxfilt pyelftools ansiwrap watchdog python-Levenshtein toml

install them by running:

```shell
pip install -r requirements.txt
```

## Dump the game

Next, you'll need to acquire the **original 2.1.0** main **NSO executable**.

- To dump it from a Switch, follow the instructions on the wiki (I suggest putting it in game/)
- You do not need to dump the entire game (RomFS + ExeFS + DLC). Just dumping the 2.1.0 ExeFS is sufficient
- The decompressed 2.1.0 NSO has the following SHA256 hash: c2c8d1184eee861052c6f02c4820b51c1ae289fd7f1920522726c405b5254cd3

## Setup the repo

Now we need the repo you can clone by running:

```shell
git clone https://github.com/tsuyoi-w/DreadComp --recursive

# If you using SSH

git clone git@github.com:tsuyoi-w/DreadComp.git --recursive

# if you already clone the repo without submodules run this command
git submodule update --init --recursive
```

Now you can run the setup.py:

```shell
tools/setup.py # <path to the 'main' file>
```

This will:

- convert the executable if necessary
- set up Clang by downloading it from the official LLVM website
- create a build directory in build/

If something goes wrong, follow the instructions given to you by the script

## Build

To start the build run:

```shell
ninja -C build
```

It probably won’t be necessary in the future (!soon). I plan to make an objdiff that will build alone the changes by saving

## Setup ghidra

you can follow [ghidra setup](ghidra.md) guide

## Setup VScode

You'll need the following extensions:

- python
- ASM Code Lens
- Clangd or C/C++ Extension pack
- Clang-Format

i also suggest:

- Todo Tree
- Better Comments
- A theme you like (i use tokyo night or dark 2026)

Next you need some settings you can do it by copy/pasting both .json to a .vscode folder

## Contributing

A work in progress, but [CONTRIBUTING.md](Contributing.md) has guidelines for how to contribute to the project
