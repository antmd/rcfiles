import lldb
import re
import shlex

# This script allows Xcode to selectively ignore Obj-C exceptions
# based on any selector on the NSException instance

def getRegister(target):
    if target.triple.startswith('x86_64'):
        return "rdi"
    elif target.triple.startswith('i386'):
        return "eax"
    elif target.triple.startswith('arm64'):
        return "x0"
    else:
        return "r0"

def callMethodOnException(frame, register, method):
    return frame.EvaluateExpression("(NSString *)[(NSException *)${0} {1}]".format(register, method)).GetObjectDescription()

def continueRunning(debugger):
    debugger.SetAsync(True)
    debugger.HandleCommand("continue")

def writeToResult(result, output):
    result.PutCString(output)
    result.flush()

def filterException(debugger, user_input, result, unused):
    target = debugger.GetSelectedTarget()
    frame = target.GetProcess().GetSelectedThread().GetFrameAtIndex(0)
    filters = shlex.split(user_input)

    if frame.symbol.name == 'objc_exception_throw':
        register = getRegister(target)
        
        for filter in filters:
            method, regexp_str = filter.split(":", 1)
            value = callMethodOnException(frame, register, method)

            if value is None:
                output = "Unable to grab exception from register {0} with method {1}; skipping...".format(register, method)
                result.PutCString(output)
                result.flush()
                continue

            regexp = re.compile(regexp_str)

            if regexp.match(value):
                writeToResult(result, "Skipping exception because exception's {0} ({1}) matches {2}".format(method, value, regexp_str))
                continueRunning(debugger)
                return None
            else:
                writeToResult(result, "Breaking on exception {}".format(value))

        return None

    elif frame.symbol.name == '__cxa_throw':
        frame1 = target.GetProcess().GetSelectedThread().GetFrameAtIndex(1)
        frame1_name = frame1.symbol.name

        for filter in filters:
            if filter in frame1_name:
                writeToResult(result, "Skipping exception because exception {} matches {}".format(frame1_name, filter))
                continueRunning(debugger)
                return None
            else:
                writeToResult(result, "Breaking on exception {}".format(frame1_name))

        return None

    return None


def __lldb_init_module(debugger, unused):
    debugger.HandleCommand('command script add --function ignore_exception.filterException ignore_exception')
