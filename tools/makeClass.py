#!/usr/bin/env python3

import csv
from pathlib import Path
from capstone import * 
import subprocess as sp
import os
import objdiff as obj

ROOT = Path(__file__).parent.parent

FN_PATH = ROOT / 'data' / 'function.csv'

BUILD = ROOT / 'build' / 'src'
INC_PATH = ROOT / 'includes'
SRC_PATH = ROOT / 'src'
BUILD_DCP = ROOT / 'build' / 'CMakeFiles' / 'dread.dir' / 'src'

CODE = Path("./data/main.nso").read_bytes()

md = Cs(CS_ARCH_ARM64, CS_MODE_ARM) 
md.skipdata = True

generateSourceAndHeader = False

other_class_fn_name: list[str] = []
fn_index: int = 0

class Function:
    def __init__(self, adress: int, size: int, symbol: str, index: int) -> None:
        index = symbol.split('::').__len__() - 1
        self.namespace = symbol.split('::')[0]
        self.name = symbol.split('::')[index].split('(')[0]
        self.parameters = ')' if symbol.split('::')[index].split(',').__len__() <= 1 else symbol.split('::')[index].split('(')[1].split(',', 1)[1].replace('ulong', 'unsigned long')
        self.adress = adress
        self.size = size
        self.asm_name = self.name
        self.asm_name = '"' + self.name + "(" + self.parameters + '"'
 
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
genhppandcpp = True
index = 0
write = True

for namespace_l in FunctionList:
    if namespace_l == []:
        continue
    Demangleds : list[str] = []
    for fn in namespace_l:
        if not create_class:
            header_str = f"#pragma once\n class ActorUnk_002" + "{};" + f"\nclass {fn.namespace}" + "{\n"
            src_str = f'#include <{fn.namespace}.h>\n'
            namespace = fn.namespace
            create_class = True

        #! READ CODE IN THE .NSO 
        data = CODE[fn.adress:fn.adress + fn.size]

        #! CLEAR PATH IF THEY EXISTS
        if Path(BUILD / str(fn.namespace+'.s')).exists():
            os.remove(BUILD / str(fn.namespace+'.s'))
        if Path(BUILD / str(fn.namespace+'.o')).exists():
            os.remove(BUILD / str(fn.namespace+'.o'))

        #! CREATE ASM FILE
        func.append(f'\n\n.global {fn.asm_name}\n\n{fn.asm_name}:\n')
        for i in md.disasm(data, fn.adress):
            func.append(f"\t{i.mnemonic} {i.op_str}\n")
        Demangleds.append(fn.asm_name.replace('"', ''))
        if genhppandcpp:
        #! CREATE HEADER FILE
            if fn.name == fn.namespace or fn.name == '~' + fn.namespace:
                header_str += f'\n\t{fn.name}({fn.parameters};'
            elif fn.name.startswith('vfunc'):
                header_str += f'\n\tvirtual void {fn.name}({fn.parameters};'
            else:
                header_str += f'\n\tvoid {fn.name}({fn.parameters};'

            #! CREATE SOURCE FILE
            if fn.name == fn.namespace or fn.name == '~' + fn.namespace:
                src_str += f'\n {fn.namespace}::{fn.name}({fn.parameters}' + '{}'
            else:
                src_str += f'void {fn.namespace}::{fn.name}({fn.parameters}' + '{}'

    #! WRITE FN and COMPILE ASM
    func_str = "".join(func)
    func_str = func_str.replace('#', "")
    with open(BUILD / str(namespace+'.s'), 'w') as f:
        f.write(func_str)

    sp.run(['aarch64-linux-gnu-as', BUILD / str(namespace+'.s'), "-o", BUILD / str(namespace+'.o')])

    if Path(INC_PATH / str(fn.namespace+'.h')).exists():
            genhppandcpp = False
    if Path(SRC_PATH / str(fn.namespace+'.cpp')).exists():
            genhppandcpp = False

    if genhppandcpp:
        #! WRITE HEADER 
        header_str += '\n};'
        with open(INC_PATH / str(namespace+'.h'), 'w') as f:
            f.write(header_str)

        #! WRITE SOURCE
        with open(SRC_PATH / str(namespace+'.cpp'), 'w') as f:
            f.write(src_str)

        sp.run(['ninja', "-C", ROOT / 'build'])
        demangled_list = obj.demangle(Path(BUILD_DCP / str(namespace+'.cpp.obj')))
        obj.generate_objdiff_config(Demangleds, demangled_list)

    index += 1
    header_str: str = ""
    src_str: str = ""
    func_str: str = ""
    namespace: str = ""

    create_class = False

    func: list[list[str]] = ['.section .text']