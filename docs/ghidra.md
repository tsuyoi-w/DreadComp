# Ghidra setup

[ghidra]: https://github.com/NationalSecurityAgency/ghidra/releases/tag/Ghidra_12.1.2_build
[switch]: https://github.com/borntohonk/Switch-Ghidra-Guides

## Install requirement

You'll need the following program:

- Install JDK 21 64-bit
- Download [Ghidra 12.1.2][ghidra]
- Extract the Ghidra release file
  - **NOTE:** Do not extract on top of an existing installation
- Follow this and build the [switch-loader][switch]

## Setup

Launch Ghidra: ./ghidraRun (ghidraRun.bat for Windows) \
or PyGhidra: ./support/pyghidraRun (support\pyghidraRun.bat for Windows)

Now we need to install the switch-loader extensions:

- Go to FIle > install extensions
- Click on **Add Extension**
- Choose the extension zip file
- check the box and restart

Now you can press i or file > import file and import the main.nso.
Dont change the default import options.
After importation launch the file and click on yes for analyze, Dont forgot do select (Switch) IPC Analyzer and Analyze (this can take a while, just wait)
