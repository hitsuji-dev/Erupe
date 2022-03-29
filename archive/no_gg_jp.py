"""
A simple gameguard disabler for Monster Hunter Frontier (JP).

Requires Python3.7 and frida (via pip: `py -3 -m pip install frida`).

Usage:
    1. Place script in the same folder as you mhf.exe.
    2. Open a cmd prompt as admin and run the script, it will spawn the game launcher with the gameguard init patched out.
    3. Leave running until you are entirely in-game, as it has to patch both mhf.exe AND mhfo.dll after they unpack.
"""

import frida
import time
import sys

def main():
    executable_name = "mhf.exe"
    pID = frida.spawn(executable_name)
    session = frida.attach(pID)

    script = session.create_script("""

    /*
    Interceptor.attach(Module.findExportByName("ws2_32.dll", "gethostbyname"), {
        onEnter: function(args) {
            var name = args[0];
            console.log("gethostbyname");
            console.log(name.readCString());
        },
        onLeave: function(retval) {
            
            console.log("OnLeave", retval);
            console.log(hexdump(retval, {
                offset: 0,
                length: 64,
            }));
            console.log("h_name" + retval.readPointer().readCString());
            console.log("h_aliases_start" + retval.add(4).readPointer());
            
            console.log("h_addrtype" + retval.add(8).readU16());
            console.log("h_length" + retval.add(10).readU16());
            
            console.log("ip ptr 0 " + retval.add(12).readPointer().add(0).readU32());
            console.log("ip ptr 1 " + retval.add(12).readPointer().add(4).readU32());
            console.log("ip " + retval.add(12).readPointer().add(0).readPointer().readU32());
            
            retval.add(12).readPointer().readPointer().writeU32(16777343);
            retval.add(12).readPointer().add(4).writeU32(0);

            console.log("ip ptr 0 " + retval.add(12).readPointer().add(0).readU32());
            console.log("ip ptr 1 " + retval.add(12).readPointer().add(4).readU32());
            console.log("ip " + retval.add(12).readPointer().add(0).readPointer().readU32());

        }
    });
    */

    // Wait for ASProtect to unpack.
    // mhf.exe calls GetCommandLineA near it's entrypoint before WinMain, so it will be one of the first few calls.
    var mhfGetCommandLineAHook = Interceptor.attach(Module.findExportByName("kernel32.dll", "GetCommandLineA"), {
        onEnter: function(args){
            try{
                var mhfMod = Process.getModuleByName('mhf.exe');
                var ggInitFuncResults = Memory.scanSync(mhfMod.base, mhfMod.size, "55 8B EC 81 EC 04 01 00 00");
                if(ggInitFuncResults.length < 1) {
                    //console.log("Failed to find gameguard init function");
                    return;
                } else {

                    console.log("Found GG init function in mhf.exe. Patching...");

                    var ggInitFunc = ggInitFuncResults[0].address;
                    Memory.patchCode(ggInitFunc, 64, function (code) {
                        var cw = new X86Writer(code, { pc: ggInitFunc });
                        cw.putMovRegU32('eax', 1);
                        cw.putRet();
                        cw.flush();
                    });

                    console.log("Patch complete.");
                    mhfGetCommandLineAHook.detach();
                }
            } catch(e){
            }
        }
    });

    // Waits for the mhfo.dll module to be loaded and unpacked.
    // this works by hooking user32.dll$RegisterClassExA and waiting for
    // the mhfo.dll module to register the " M H F " class.
    var mhfoRegisterClassExAHook = Interceptor.attach(Module.findExportByName("user32.dll", "RegisterClassExA"), {
        onEnter: function(args) {
            var wndClassExA = args[0];
            var lpszClassName = wndClassExA.add(0x28).readPointer();
            var classNameStr = lpszClassName.readCString();
            var match = classNameStr == " M H F ";
            if(match) {
                console.log("mhfo(-hd).dll unpacked.");
                try {
                  console.log("try to find standard dll")
                  var mhfoMod = Process.getModuleByName('mhfo.dll');
                }
                catch(err) {
                  console.log("try to find hd dll")
                  var mhfoMod = Process.getModuleByName('mhfo-hd.dll');
                }
                var ggCheckFuncResults = Memory.scanSync(mhfoMod.base, mhfoMod.size, "A1 ?? ?? ?? ?? 48 A3 ?? ?? ?? ?? 85 C0 7F 32");
                if(ggCheckFuncResults.length >= 1) {
                    console.log("Found GG check function in mhfo(-hd).dll Patching...");

                    var ggCheckFunc = ggCheckFuncResults[0].address;
                    Memory.patchCode(ggCheckFunc, 64, function (code) {
                        var cw = new X86Writer(code, { pc: ggCheckFunc });
                        cw.putMovRegU32('eax', 1);
                        cw.putRet();
                        cw.flush();
                    });

                    console.log("Patch complete.");
                    console.log("All patches are complete, you can now exit this frida script.");
                    mhfoRegisterClassExAHook.detach();
                }

            }
        }
    });
    
""")
    def on_message(message, data):
        print("[{}] => {}".format(message, data))

    script.on('message', on_message)
    script.load()
    
    frida.resume(pID)

    print("[!] Ctrl+D on UNIX, Ctrl+Z on Windows/cmd.exe to detach from instrumented program.\n\n")
    sys.stdin.read()
    session.detach()

if __name__ == '__main__':
    main()