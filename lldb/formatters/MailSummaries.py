
import lldb
import math
 
def message_summary(valueObject, dictionary):

    target = valueObject.GetTarget();
    
    # Lookup MCMessage* type
    message_type = target.FindFirstType('MCMessage').GetPointerType()

    msgObject = valueObject.Cast(message_type)
    subject_ivar = msgObject.GetChildMemberWithName('_subject',lldb.eDynamicCanRunTarget)
    sender_ivar = msgObject.GetChildMemberWithName('_sender',lldb.eDynamicCanRunTarget)
    
    # grab the raw data from those instance variables
    subject = subject_ivar.GetSummary().lstrip("@")
    sender = sender_ivar.GetSummary().lstrip("@")

    retval = "Subject = " + str(subject) + ", From = " + str(sender)

    if (valueObject.GetTypeName().startswith("MFMessageThread")):
        message_type = target.FindFirstType('MFMessageThread').GetPointerType()
        threadObject = valueObject.Cast(message_type)
        messages_ivar = threadObject.GetChildMemberWithName('_filteredMessages',lldb.eDynamicCanRunTarget)
        messages = messages_ivar.GetSummary().lstrip("@")
        retval += ", messages = " + str(messages)

    return retval
 

# this is a special funtion, which if exists, will be called by LLDB when this script is imported.
def __lldb_init_module(debugger, dict):
    
    # automatically add our summaries when the script is imported.
    debugger.HandleCommand('type summary add MFLibraryMessage -F MailSummaries.message_summary')
    debugger.HandleCommand('type summary add MFMessageThread -F MailSummaries.message_summary')
