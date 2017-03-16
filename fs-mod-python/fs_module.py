import freeswitch

"""
FreeSWITCH's mod_python usage examples.

This module uses the default names looked up by mod_python, but most of
these names can be overridden using <modname>::<function> when calling
the module from FreeSWITCH.

"""


def handler(session, args):
    """
    'handler' is the default function name for apps.

    It can be overridden with <modname>::<function>

    `session` is a session object
    `args` is a string with all the args passed after the module name

    """
    freeswitch.consoleLog('info', 'Answering call from Python.\n')
    freeswitch.consoleLog('info', 'Arguments: %s\n' % args)
    freeswitch.consoleLog('info', 'Caller Number: %s\n' % session.getVariable("caller_id_name"))
    freeswitch.consoleLog('info', 'Caller Destionation Number: %s\n' % session.getVariable("destination_number"))

    with open('/usr/share/freeswitch/scripts/newfile.txt', 'w') as yaz:
        yaz.write('Caller Number is: ' + session.getVariable("caller_id_name") + '\n')
    with open('/usr/share/freeswitch/scripts/newfile.txt', 'a') as yaz:
        yaz.write('Called Number is: ' + session.getVariable("destination_number") + '\n')

#    session.answer()
#    session.setHangupHook(hangup_hook)
#    session.setInputCallback(input_callback)
#    session.execute("playback", session.getVariable("hold_music"))

def hangup_hook(session, what, args=''):
    """
    Must be explicitly set up with session.setHangupHook(hangup_hook).

    `session` is a session object.
    `what` is "hangup" or "transfer".
    `args` is populated if you pass extra args to session.setInputCallback().

    """
    freeswitch.consoleLog("info", "hangup hook for '%s'\n" % what)


def input_callback(session, what, obj, args=''):
    """
    Must be explicitly set up with session.setInputCallback(input_callback).

    `session` is a session object.
    `what` is "dtmf" or "event".
    `obj` is a dtmf object or an event object depending on the 'what' var.
    `args` is populated if you pass extra args to session.setInputCallback().

    """
    if (what == "dtmf"):
        freeswitch.consoleLog("info", what + " " + obj.digit + "\n")
    else:
        freeswitch.consoleLog("info", what + " " + obj.serialize() + "\n")
    return "pause"


def fsapi(session, stream, env, args):
    """
    Handles API calls (from fs_cli, dialplan HTTP, etc.).

    Default name is 'fsapi', but it can be overridden with <modname>::<function>

    `session` is a session object when called from the dial plan or the
              string "na" when not.
    `stream` is a switch_stream. Anything written with stream.write() is
             returned to the caller.
    `env` is a switch_event.
    `args` is a string with all the args passed after the module name.

    """
    if args:
        stream.write("fsapi called with no arguments.\n")
    else:
        stream.write("fsapi called with these arguments: %s\n" % args)
    stream.write(env.serialize())


def runtime(args):
    """
    Run a function in a thread (eg.: when called from fs_cli `pyrun`).

    `args` is a string with all the args passed after the module name.

    """
    print args + "\n"


def xml_fetch(params):
    """
    Bind to an XML lookup.

    `params` is a switch_event with all the relevant data about what is being
             searched for in the XML registry.

    """
    xml = '''
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<document type="freeswitch/xml">
  <section name="dialplan" description="RE Dial Plan For FreeSWITCH">
    <context name="default">
      <extension name="generated">
        <condition>
         <action application="answer"/>
         <action application="playback" data="${hold_music}"/>
        </condition>
      </extension>
    </context>
  </section>
</document>
'''

    return xml

