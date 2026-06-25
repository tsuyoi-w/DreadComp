#!/usr/bin/env python3

import csv
from pathlib import Path
from capstone import *
import subprocess as sp

ROOT = Path(__file__).parent.parent
BUILD = ROOT / 'build' / 'src'

CODE = Path("./data/main.nso").read_bytes()

func: list[str] = ['.section .text\n.global {name}\n\n{name}:\n']

md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True

class Function:
    def __init__(self, adress: int, size: int, symbol: str) -> None:
        self.namespace = symbol.split('::')[0]
        self.name = symbol.split('::')[1]
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

for fn in FunctionList:
    data = CODE[fn.adress:fn.adress + size]
    for i in md.disasm(data, fn.adress):
        func.append(f"\t{i.mnemonic} {i.op_str}\n")
    func_str: str = "".join(func)
    func_str = func_str.replace('{name}', fn.name)
    func_str = func_str.replace('#', "")
    with open(BUILD / str(fn.namespace+'.s'), 'w') as f:
        f.write(func_str)
    
    sp.run(['aarch64-linux-gnu-as', BUILD / str(fn.namespace+'.s'), "-o", BUILD / str(fn.namespace+'.o')])

