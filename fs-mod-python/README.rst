* Control VoIP session flow with Python codes

Install Debian 8.5 and the install FreeSWITCH from official repository with the following commands:

# wget -O - https://files.freeswitch.org/repo/deb/debian/freeswitch_archive_g0.pub | apt-key add -
# echo "deb http://files.freeswitch.org/repo/deb/freeswitch-1.6/ jessie main" > /etc/apt/sources.list.d/freeswitch.list
 
# you may want to populate /etc/freeswitch at this point.
# if /etc/freeswitch does not exist, the standard vanilla configuration is deployed
# apt-get update && apt-get dist-upgrade –y && apt-get install -y freeswitch-meta-all


Install development and pip:
# apt-get install python-dev python-pip –y

After installation try to find freeswitch.py file for API use (This file configured automatically from FreeSWITCH packages. This file will be used as FreeSWITCH library):
root@fspush:~# find / -name freeswitch.py
/usr/share/pyshared/freeswitch.py
/usr/lib/pymodules/python2.7/freeswitch.py


Look at symlink:
# ll /usr/lib/pymodules/python2.7/freeswitch.py
lrwxrwxrwx 1 root root 33 Mar 14 07:31 /usr/lib/pymodules/python2.7/freeswitch.py -> /usr/share/pyshared/freeswitch.py


Uncomment the following line in the /etc/freeswitch/autoload_configs/modules.conf.xml file:
<load module="mod_python"/>

Note: If you want post data to web server then, in the /etc/freeswitch/dialplan/default.xml file add the following lines for the "Local_Extension":
        <action application="curl" data="http://IP.addr.of.server/ post id=${destination_number}" json inline="true"/>
        <action application="set" data="respdata=${curl_response_data}"/>


Create /usr/share/freeswitch/scripts/fs_module.py file and add the following content to this file:
root@fspush:~# cat /usr/share/freeswitch/scripts/fs_module.py
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


In the /etc/freeswitch/dialplan/default.xml file search " Local_Extension" and add the following line in this extension:
<action application="python" data="fs_module"/>


Give permission to write a file:
# chown -R freeswitch:freeswitch /usr/share/freeswitch/scripts/


Restart the service:
# systemctl restart freeswitch

In the fs_cli console check mod_python as following:
freeswitch@fspush> module_exists mod_python
true


Call from extension 1002 to 1009 and look at result in the newfile.txt:
root@fspush:~# cat /usr/share/freeswitch/scripts/newfile.txt
Caller Number is: 1002
Called Number is: 1009


If you uncomment the following lines in the fs_module.py file then, each call will be answered with the hold_music variable:
#    session.answer()
#    session.setHangupHook(hangup_hook)
#    session.setInputCallback(input_callback)
#    session.execute("playback", session.getVariable("hold_music"))


If you want forward calls for selected extension just add the following lines under handler() function(If extension 1002 will call to 1004 then, call will be forwarded to the 1006 and if 1003 call to 1002 it will play music file.):
    if session.getVariable("caller_id_name") == '1002' and session.getVariable("destination_number") == '1004':
        freeswitch.consoleLog('info', 'Caller Number: %s\n' % session.getVariable("caller_id_name"))
        with open('/usr/share/freeswitch/scripts/newfile.txt', 'w') as yaz:
            yaz.write('Caller number is: {0}, Called number is: {1}'.format(session.getVariable("caller_id_name"), session.getVariable("destination_number")))
        session.execute("execute_extension", "'{0}' XML default".format('1006'))
    elif session.getVariable("caller_id_name") == '1003' and session.getVariable("destination_number") == '1002':
        session.answer()
        session.streamFile("/usr/share/freeswitch/sounds/music/8000/partita-no-3-in-e-major-bwv-1006-1-preludio.wav")
    else:
        freeswitch.consoleLog('info', 'Comparing does not success result!!!\n')
        pass

