//Get all symbol and filter it into different csv file
//@author DisabledMallis
//@category Symbol
//@keybinding
//@menupath
//@toolbar

import java.nio.file.Files;
import java.nio.file.Path;

import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.AddressSetView;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionManager;
import ghidra.program.model.listing.Program;

public class getAllData extends GhidraScript {

    final String fn_path = "\\\\wsl.localhost\\DreadComp\\home\\dreadcomp\\projects\\Metroid\\DreadComp\\data\\function.csv";
    final String str_path = "\\\\wsl.localhost\\DreadComp\\home\\dreadcomp\\projects\\Metroid\\DreadComp\\data\\string.csv";
    final String sym_path = "\\\\wsl.localhost\\DreadComp\\home\\dreadcomp\\projects\\Metroid\\DreadComp\\data\\symbol.csv";
    Boolean fn = true;
    String fn_str = "";
    Boolean str = true;
    String str_str = "";
    Boolean sym = true;
    String sym_str = "";

    public void run() throws Exception {
        Program current = getCurrentProgram();
        FunctionManager fnmngr = current.getFunctionManager();

        if (fn) {
            for (Function func : fnmngr.getFunctions(true)) {
                AddressSetView body = func.getBody();

                Long base_addr = Long.parseLong(body.getMinAddress().toString(), 16);
                String adrr = Long.toHexString(base_addr);

                String size = Long.toHexString(body.getNumAddresses());

                String namespace = (!func.getParentNamespace().toString().equals("Global"))
                        ? func.getParentNamespace().toString() + "::"
                        : "";

                String row = adrr + "," + size + "," + namespace + func.getName() + '\n';
                fn_str += row;
            }
            Files.writeString(Path.of(fn_path), fn_str);
        }

    }
}
