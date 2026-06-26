#!/usr/bin/env python3

import csv
from pathlib import Path
from capstone import * 
import subprocess as sp
import os

ROOT = Path(__file__).parent.parent
BUILD = ROOT / 'build' / 'src'

CODE = Path("./data/main.nso").read_bytes()

func: list[str] = ['\n\n.global {name}\n\n{name}:\n']

md = Cs(CS_ARCH_ARM64, CS_MODE_ARM) 
md.skipdata = True

delete = False
class Function:
    def __init__(self, adress: int, size: int, symbol: str) -> None:
        index = symbol.split('::').__len__() - 1
        self.namespace = symbol.split('::')[0]
        self.name = symbol.split('::')[index]
        self.adress = adress
        self.size = size

FunctionList: list[Function] = [] 
with open(ROOT / 'data/rom_extract.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[3] == 'true':
            adress = int(row[0], 16)
            size = int(row[1], 16)
            symbol = row[2]
            FunctionList.append(Function(adress, size, symbol))

AsmFile: list[Path] = []
for fn in FunctionList:
    func_str: str = ""
    data = CODE[fn.adress:fn.adress + fn.size]
    if Path(BUILD / str(fn.namespace+'.s')).exists():
        with open(BUILD / str(fn.namespace+'.s'), 'r') as f:
            func_str = f.read()
    else:
        func.append('.section .text')
        func.reverse()
        AsmFile.append(BUILD / str(fn.namespace+'.s'))
    for i in md.disasm(data, fn.adress):
        func.append(f"\t{i.mnemonic} {i.op_str}\n")
    copy = "".join(func)
    func_str += copy
    func_str = func_str.replace('{name}', fn.name)
    func_str = func_str.replace('#', "")
    func = ['\n.global {name}\n{name}:\n']
    with open(BUILD / str(fn.namespace+'.s'), 'w') as f:
        f.write(func_str)

    sp.run(['aarch64-linux-gnu-as', BUILD / str(fn.namespace+'.s'), "-o", BUILD / str(fn.namespace+'.o')])

    if delete:
        for file in AsmFile:
            os.remove(file)
