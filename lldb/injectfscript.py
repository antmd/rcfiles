import lldb
import re
import shlex

# This script allows Xcode to selectively ignore Obj-C exceptions
# based on any selector on the NSException instance

def injectFscript(debugger, user_input, result, unused):
    target = debugger.GetSelectedTarget()
    frame = target.GetProcess().GetSelectedThread().GetFrameAtIndex(0)

    debugger.HandleCommand("expr (BOOL)[(NSBundle*)[ NSBundle bundleWithPath:@\"/Library/Frameworks/FScript.framework\"] load]")
    debugger.HandleCommand("expr (id)[(id)NSClassFromString(@\"FScriptMenuItem\") insertInMainMenu]")

    return None

def __lldb_init_module(debugger, unused):
    debugger.HandleCommand('command script add --function injectfscript.injectFscript inject_fscript')
