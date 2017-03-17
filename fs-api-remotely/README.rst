====================================
Control FreeSWITCH with API remotely
====================================

* In the python code worked server install needed libraries::
      
     # python -m pip install esl
     # python -m pip install FreeSWITCH-ESL-Python

* Create script with `channel_api.py <https://github.com/jamalshahverdiev/freeswitch-codes/blob/master/fs-api-remotely/channel_api.py>`_

* Add the following lines to the "/etc/freeswitch/autoload_configs/acl.conf.xml" file in the FreeSWITCH server(10.50.63.228 IP is place from where "channel_api.py" code is connecting to the FreeSWITCH server)::
     
     <list name="loopback.auto" default="allow">
        <node type="allow" cidr="10.50.63.228/32"/>
     </list>

* At the end restart FreeSWITCH server::
     
     # systemctl restart freeswitch


* If you want to see the channel variables just create "`getvars.sh <https://github.com/jamalshahverdiev/freeswitch-codes/blob/master/fs-api-remotely/getvars.sh>`_ " script in the FreeSWITCH server and execute it(Don't forget minimum one call must be present at script using time).

* Result of this code will be as following::
     
     root@fspush:~# ./getvars.sh
     Variable name is: uuid
     Result is: 3e88b243-50ad-4845-94ce-a6d6a647fec1

     Variable name is: direction
     Result is: inbound

     Variable name is: presence_id
     Result is: 1002@10.50.3.114

     Variable name is: accountcode
     Result is: 1002

     Variable name is: call_uuid
     Result is: 3e88b243-50ad-4845-94ce-a6d6a647fec1

     Variable name is: hostname
     Result is: fspush


Break selected UUID::

     freeswitch@fspush> uuid_break 3e88b243-50ad-4845-94ce-a6d6a647fec1 all

Check UUID if exists::

     freeswitch@fspush> uuid_exists 3e88b243-50ad-4845-94ce-a6d6a647fec1
     true

Print all channel variables for selected UUID::
     
     freeswitch@fspush> uuid_dump 3e88b243-50ad-4845-94ce-a6d6a647fec1

