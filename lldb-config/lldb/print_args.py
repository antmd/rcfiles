import sys
sys.path.append('/Users/ant/rcfiles/lldb')
import lldb
import lldbutil
from collections import OrderedDict
import commands
import optparse
import shlex
import re

args2reg=OrderedDict()
args2reg["self"] = "rdi"
args2reg["arg1"] = "rdx"
args2reg["arg2"] = "rcx"
args2reg["arg3"] = "r8"
args2reg["arg4"] = "r9"

def GetPrintExpr(name):
    return "(NSString*)[(id)${} description]".format(args2reg[name])

def GetArguments(target, frame):
    id_type = target.FindFirstType('NSObject').GetPointerType()

    args=OrderedDict()
    if not target or not frame:
        return None
    # Note: I assume the PC is at the first instruction of the function, before the stack and registers have been modified.
    if target.triple.startswith('x86_64'):
        regs = frame.regs[0]
        for name in args2reg:
            args[name] = regs.GetChildMemberWithName(args2reg[name]).Cast(id_type)
        return args

def args_command(debugger, user_input, result, unused):
    target = debugger.GetSelectedTarget()
    if not target:
        result.PutCString('Not in a valid state to use this command.')
        return None
    frame = target.GetProcess().GetSelectedThread().GetFrameAtIndex(0)
    args = GetArguments(target, frame)
    for name,val in args.items():
        print >>result, "{} = {}".format(name,val)
    return None

def arg_command(debugger, command, result, unused):
    command_args = shlex.split(command)
    arg_name = command_args[0] # command not included - args start at '0'
    target = debugger.GetSelectedTarget()
    if not target:
        result.PutCString('Not in a valid state to use this command.')
        return None
    frame = target.GetProcess().GetSelectedThread().GetFrameAtIndex(0)
    args = GetArguments(target, frame)
    arg_val = args[arg_name]
    desc = frame.EvaluateExpression(GetPrintExpr(arg_name))
    desc = re.sub(r'^\([^\)]+\)\s*', r'', str(desc))
    print >>result, desc


    return None

def __lldb_init_module(debugger, unused):
    debugger.HandleCommand('command script add --function print_args.args_command print_args')
    debugger.HandleCommand('command script add --function print_args.arg_command print_arg')
    print 'The "print_args" command has been installed.'
