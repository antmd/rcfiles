import lldb

def GetFirstArgumentAsValue(target, frame):
    if not target or not frame:
        return None
    # Note: I assume the PC is at the first instruction of the function, before the stack and registers have been modified.
    if target.triple.startswith('x86_64'):
        return frame.regs[0].GetChildMemberWithName("rdi")
    elif target.triple.startswith('i386'):
        espValue = frame.regs[0].GetChildMemberWithName("esp")
        address = espValue.GetValueAsUnsigned() + target.addr_size
        return espValue.CreateValueFromAddress('arg0', address, target.FindFirstType('id'))
    else:
        return frame.regs[0].GetChildMemberWithName("r0")

def command(debugger, user_input, result, unused):
    target = debugger.GetSelectedTarget()
    if not target:
        result.PutCString('Not in a valid state to use this command.')
        return None
    frame = target.GetProcess().GetSelectedThread().GetFrameAtIndex(0)
    description = GetFirstArgumentAsValue(target, frame).GetObjectDescription()
    if description is None:
        output = "I couldn't get the description of the exception being thrown."
    else:
        output = "Description of exception being thrown: " + repr(description)
    result.PutCString(output)
    return None

def __lldb_init_module(debugger, unused):
    debugger.HandleCommand('command script add --function sniff_objc_exception_throw.command sniff_objc_exception_throw')
    print 'The "sniff_objc_exception_throw" command has been installed. Use if stopped on first instruction of objc_exception_throw.'
