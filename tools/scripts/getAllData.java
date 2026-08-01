//Get all symbol and filter it into different csv file
//@author DisabledMallis
//@category Symbol
//@keybinding
//@menupath
//@toolbar

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Iterator;

import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.AddressSetView;
import ghidra.program.model.data.AbstractStringDataType;
import ghidra.program.model.listing.Data;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionManager;
import ghidra.program.model.listing.Program;
import ghidra.program.model.symbol.Symbol;
import ghidra.program.model.symbol.SymbolTable;
import ghidra.program.model.symbol.SymbolType;
import ghidra.program.util.DefinedDataIterator;

public class getAllData extends GhidraScript {

    final String fn_path = "D:/dev/C/Decomp/MetroidDread/DreadComp/data/function.csv";
    final String str_path = "D:/dev/C/Decomp/MetroidDread/DreadComp/data/string.csv";
    final String sym_path = "D:/dev/C/Decomp/MetroidDread/DreadComp/data/symbol.csv";
    Boolean fn = true;
    String fn_str = "Address,Quality,Size,Name\n";
    Boolean str = false;
    String str_str = "";
    Boolean sym = false;
    String sym_str = "";

    public void run() throws Exception {
        Program current = getCurrentProgram();
        FunctionManager fnmngr = current.getFunctionManager();
        SymbolTable sym_table = current.getSymbolTable();

        if (fn) {
            for (Function func : fnmngr.getFunctions(true)) {
                if (func.isThunk() || func.isExternal()) {
                    continue; 
                }
                AddressSetView body = func.getBody();

                String adrr = body.getMinAddress().toString();

                String size = Long.toString(body.getNumAddresses());

                // String namespace = (!func.getParentNamespace().toString().equals("Global"))
                //         ? func.getParentNamespace().toString() + "::"
                //         : "";

                String row = "0x" + adrr + ",U," + size + "," + '\n';
                fn_str += row;
            }
            Files.writeString(Path.of(fn_path), fn_str);
        }

        Iterator<Data> it = DefinedDataIterator.byDataType(
                currentProgram,
                dt -> dt instanceof AbstractStringDataType);

        if (str) {
            while (it.hasNext()) {
                Data data = it.next();
                String addr = data.getAddress().toString();
                String name = data.getValue().toString();
                String row = addr + ",\"" + name + "\"\n";
                str_str += row;
            }
            Files.writeString(Path.of(str_path), str_str);
        }

        if (sym) {
            for (Symbol symbol : sym_table.getAllSymbols(true)) {

                if (symbol.getSymbolType() != SymbolType.FUNCTION
                        && symbol.getSymbolType() != SymbolType.GLOBAL_VAR)
                    continue;

                String addr = symbol.getAddress().toString();
                String name = symbol.getName();

                String row = addr + "," + name + '\n';
                sym_str += row;
            }
            Files.writeString(Path.of(sym_path), sym_str);
        }
    }
}
