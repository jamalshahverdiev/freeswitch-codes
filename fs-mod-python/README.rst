===========================================
Control VoIP session flow with Python codes
===========================================

* Install Debian 8.5 and the install FreeSWITCH from official repository with the following commands::

     # wget -O - https://files.freeswitch.org/repo/deb/debian/freeswitch_archive_g0.pub | apt-key add -
     # echo "deb http://files.freeswitch.org/repo/deb/freeswitch-1.6/ jessie main" > /etc/apt/sources.list.d/freeswitch.list
     # apt-get update && apt-get dist-upgrade -y && apt-get install -y freeswitch-meta-all


* Install Python development and pip packages::

     # apt-get install python-dev python-pip -y

* After installation try to find `freeswitch.py <https://github.com/jamalshahverdiev/freeswitch-codes/blob/master/fs-mod-python/freeswitch.py>`_ file for API use (This file configured automatically from FreeSWITCH packages. This file will be used as FreeSWITCH library)::

     root@fspush:~# find / -name freeswitch.py
     /usr/share/pyshared/freeswitch.py
     /usr/lib/pymodules/python2.7/freeswitch.py

* Look at symlink::

     # ll /usr/lib/pymodules/python2.7/freeswitch.py
     lrwxrwxrwx 1 root root 33 Mar 14 07:31 /usr/lib/pymodules/python2.7/freeswitch.py -> /usr/share/pyshared/freeswitch.py

* Uncomment the following line in the "/etc/freeswitch/autoload_configs/modules.conf.xml" file::

     <load module="mod_python"/>

* Note: If you want post data to web server then, in the "/etc/freeswitch/dialplan/default.xml" file add the following lines for the "Local_Extension"::

        <action application="curl" data="http://IP.addr.of.server/ post id=${destination_number}" json inline="true"/>
        <action application="set" data="respdata=${curl_response_data}"/>


* In the "/usr/share/freeswitch/scripts" folder create python file `fs_module.py <https://github.com/jamalshahverdiev/freeswitch-codes/blob/master/fs-mod-python/fs_module.py>`_

* In the "/etc/freeswitch/dialplan/default.xml" file search "Local_Extension" and add the following line to this extension::

     <action application="python" data="fs_module"/>


* Give permission to write a file::

     # chown -R freeswitch:freeswitch /usr/share/freeswitch/scripts/


* Restart the service::

     # systemctl restart freeswitch

* In the fs_cli console check mod_python as following::

     freeswitch@fspush> module_exists mod_python
     true


* Call from extension 1002 to 1009 and look at result in the "newfile.txt" file::

     root@fspush:~# cat /usr/share/freeswitch/scripts/newfile.txt
     Caller Number is: 1002
     Called Number is: 1009


* If you uncomment the following lines in the "fs_module.py" file then, each call will be answered with the "hold_music" variable::

     #session.answer()
     #session.setHangupHook(hangup_hook)
     #session.setInputCallback(input_callback)
     #session.execute("playback", session.getVariable("hold_music"))


* If you want forward calls for selected extension just add the following lines under "handler()" function(If extension "1002" will call to "1004" then, call will be forwarded to the "1006" and if "1003" call to "1002" it will play music file)::

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

