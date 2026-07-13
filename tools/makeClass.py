#!/usr/bin/env python3

import csv
from pathlib import Path
from capstone import * 
import subprocess as sp
import os

ROOT = Path(__file__).parent.parent

FN_PATH = ROOT / 'data' / 'rom_extract.csv'

BUILD = ROOT / 'build' / 'src'
INC_PATH = ROOT / 'includes'
SRC_PATH = ROOT / 'src'

CODE = Path("./data/main.nso").read_bytes()


md = Cs(CS_ARCH_ARM64, CS_MODE_ARM) 
md.skipdata = True

deleteSrc = False
generateSourceAndHeader = False

other_class_fn_name: list[str] = []
fn_index: int = 0

class Function:
    def __init__(self, adress: int, size: int, symbol: str, already_exists: bool, index: int) -> None:
        index = symbol.split('::').__len__() - 1
        self.namespace = symbol.split('::')[0]
        self.name = symbol.split('::')[index]
        self.adress = adress
        self.size = size
        self.asm_name = self.name
        if self.name.startswith('~'):
            self.asm_name = '"' + self.name + '"'
        if already_exists:
            self.asm_name += '_' + str(index)
 
ns_index = 0
FunctionList = [[] for _ in range(999)]
old_namespace = ""
with open(FN_PATH, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[3] == 'true':
            symbol = row[2]
            if not symbol.split('::')[0] ==  old_namespace and not old_namespace == "":
                ns_index += 1
            adress = int(row[0], 16)
            size = int(row[1], 16)
            already_exists: bool = False
            for fname in other_class_fn_name:
                if symbol.split('::')[symbol.split('::').__len__() - 1] == fname:
                    already_exists = True
            FunctionList[ns_index].append(Function(adress, size, symbol, already_exists, fn_index))
            other_class_fn_name.append(symbol.split('::')[symbol.split('::').__len__() - 1])
            old_namespace = symbol.split('::')[0]


AsmFile: list[Path] = []
header_str: str = ""
src_str: str = ""
func_str: str = ""
namespace: str = ""

create_class = False

func: list[list[str]] = ['.section .text']

index = 0
for namespace_l in FunctionList:
    if namespace_l == []:
        continue
    for fn in namespace_l:
        if not create_class:
            header_str = f"#pragma once\nclass {fn.namespace}" + "{\n"
            src_str = f'#include "{fn.namespace}.h"\n'
            namespace = fn.namespace
            create_class = True

        #! READ CODE IN THE .NSO 
        data = CODE[fn.adress:fn.adress + fn.size]

        #! CLEAR PATH IF THEY EXISTS
        if Path(BUILD / str(fn.namespace+'.s')).exists():
            os.remove(BUILD / str(fn.namespace+'.s'))
        if Path(BUILD / str(fn.namespace+'.o')).exists():
            os.remove(BUILD / str(fn.namespace+'.o'))
        if Path(INC_PATH / str(fn.namespace+'.h')).exists():
            os.remove(INC_PATH / str(fn.namespace+'.h'))
        if Path(SRC_PATH / str(fn.namespace+'.cpp')).exists():
            os.remove(SRC_PATH / str(fn.namespace+'.cpp'))

        #! CREATE ASM FILE
        func.append(f'\n\n.global {fn.asm_name}\n\n{fn.asm_name}:\n')
        for i in md.disasm(data, fn.adress):
            func.append(f"\t{i.mnemonic} {i.op_str}\n")
        
        #! CREATE HEADER FILE
        if fn.name == fn.namespace or fn.name == '~' + fn.namespace:
            header_str += f'\n\t{fn.name}();'
        elif fn.name.startswith('vfunc'):
            header_str += f'\n\tvirtual void {fn.name}();'
        else:
            header_str += f'\n\tvoid {fn.name}();'

        #! CREATE SOURCE FILE
        if fn.name == fn.namespace or fn.name == '~' + fn.namespace:
            src_str += f'\n {fn.namespace}::{fn.name}()' + '{}'
        else:
            src_str += f'void {fn.namespace}::{fn.name}()' + '{}'

    #! WRITE FN and COMPILE ASM
    func_str = "".join(func)
    func_str = func_str.replace('#', "")
    with open(BUILD / str(namespace+'.s'), 'w') as f:
        f.write(func_str)

    sp.run(['aarch64-linux-gnu-as', BUILD / str(namespace+'.s'), "-o", BUILD / str(namespace+'.o')])

    #! WRITE HEADER 
    header_str += '\n};'
    with open(INC_PATH / str(namespace+'.h'), 'w') as f:
        f.write(header_str)

    #! WRITE SOURCE
    with open(SRC_PATH / str(namespace+'.cpp'), 'w') as f:
        f.write(src_str)

    index += 1
    header_str: str = ""
    src_str: str = ""
    func_str: str = ""
    namespace: str = ""

    create_class = False

    func: list[list[str]] = ['.section .text']