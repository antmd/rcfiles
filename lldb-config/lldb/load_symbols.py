#!/usr/bin/python

#----------------------------------------------------------------------
# Be sure to add the python path that points to the LLDB shared library.
#
# # To use this in the embedded python interpreter using "lldb" just
# import it with the full path using the "command script import"
# command
#   (lldb) command script import /path/to/cmdtemplate.py
#----------------------------------------------------------------------

import lldb
import commands
import optparse
import shlex
import glob
from os import path

def load_symbols_options():
    usage = "usage: %prog [options]"
    description='''This command adds symbols using all files in the supplied directory, with '.dwarf' extension
'''
    parser = optparse.OptionParser(description=description, prog='load_symbols',usage=usage)
    return parser

def load_symbols_command(debugger, command, result, dict):
    # Use the Shell Lexer to properly parse up command options just like a
    # shell would
    command_args = shlex.split(command)
    parser = load_symbols_options()
    try:
        (options, args) = parser.parse_args(command_args)
    except:
        # if you don't handle exceptions, passing an incorrect argument to the OptionParser will cause LLDB to exit
        # (courtesy of OptParse dealing with argument errors by throwing SystemExit)
        result.SetError ("option parsing failed")
        return

    # in a command - the lldb.* convenience variables are not to be used
    # and their values (if any) are undefined
    # this is the best practice to access those objects from within a command
    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    thread = process.GetSelectedThread()
    frame = thread.GetSelectedFrame()

    for sym_path in args:
        sym_path = path.expanduser(sym_path)
        if path.isdir(sym_path):
            dwarf_files=glob.glob(path.join(sym_path,'*.dwarf'))
            if dwarf_files:
                for dwarf_file in dwarf_files:
                    debugger.HandleCommand('target symbols add {}'.format(dwarf_file))
                    print "Added symbols from {}".format(dwarf_file)
            else:
                print "No dwarf files in {}".format(sym_path)

        else:
            print "ignoring non-directory {}".format(sym_path)


def __lldb_init_module (debugger, dict):
    # This initializer is being run from LLDB in the embedded command interpreter
    # Make the options so we can generate the help text for the new LLDB
    # command line command prior to registering it with LLDB below
    parser = load_symbols_options()
    load_symbols_command.__doc__ = parser.format_help()
    # Add any commands contained in this module to LLDB
    debugger.HandleCommand('command script add -f load_symbols.load_symbols_command load_symbols')
    print 'The "load_symbols" command has been installed'

