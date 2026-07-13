//Generates a structure for the vtable
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
import ghidra.program.model.listing.Parameter;
import ghidra.program.model.listing.Program;

public class getAllData extends GhidraScript {

    final String ex_rom_path = "\\\\wsl.localhost\\DreadComp\\home\\dreadcomp\\projects\\Metroid\\DreadComp\\data\\rom_extract.csv";
    Boolean ex_rom = true;
    String ex_rom_str = "";


    String targetNS = "ActorUnk_001";
	public void run() throws Exception {
        Program current = getCurrentProgram();
        FunctionManager fnmngr = current.getFunctionManager();

		if(ex_rom)
        {
            for (Function func : fnmngr.getFunctions(true))
            {
                AddressSetView body = func.getBody();

                Long base_addr = Long.parseLong(body.getMinAddress().toString(), 16);
                Long real_addr = (base_addr - 0x7100000000L) + 0x100;
                String adrr = Long.toHexString(real_addr);

                String size = Long.toHexString(body.getNumAddresses());

                String namespace = (!func.getParentNamespace().toString().equals("Global")) ? func.getParentNamespace().toString() + "::" : "";
                String target = (func.getParentNamespace().toString().equals(targetNS)) ? ",true" : ",false";
                String parameter = "(";
                int i = 1;
                for(Parameter pm : func.getParameters())
                {
                    String virgule = (func.getParameterCount() == i) ? "" : ",";
                    parameter += pm.getDataType() + " param_" + i + virgule;
                    i++;
                }

                String row = adrr + "," + size + ",\"" + namespace + func.getName() + parameter + ")\"" + target + '\n';
                ex_rom_str+=row;
            }
            Files.writeString(Path.of(ex_rom_path), ex_rom_str);       
        }

    }
}