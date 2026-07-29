//Get all symbol and filter it into different csv file
//@author DisabledMallis
//@category Symbol
//@keybinding
//@menupath
//@toolbar

import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionManager;
import ghidra.program.model.listing.Program;

public class Debug extends GhidraScript {

    final String fn_path = "\\\\wsl.localhost\\DreadComp\\home\\dreadcomp\\projects\\Metroid\\DreadComp\\data\\function.csv";
    final String str_path = "\\\\wsl.localhost\\DreadComp\\home\\dreadcomp\\projects\\Metroid\\DreadComp\\data\\string.csv";
    final String sym_path = "\\\\wsl.localhost\\DreadComp\\home\\dreadcomp\\projects\\Metroid\\DreadComp\\data\\symbol.csv";
    Boolean fn = true;
    String fn_str = "Address,Quality,Size,Name\n";
    Boolean str = true;
    String str_str = "";
    Boolean sym = false;
    String sym_str = "";

    public void run() throws Exception {
        Program current = getCurrentProgram();
        FunctionManager fnmngr = current.getFunctionManager();

        Function addr = fnmngr.getFunctionAt(current.getAddressFactory().getAddress("0x7100150da0"));

        println(addr.getBody().getNumAddresses() + " -> " + addr.getBody().getMinAddress() + " -> " + addr.getBody().getMaxAddress());
    }
}
