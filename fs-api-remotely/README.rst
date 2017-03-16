====================================
Control FreeSWITCH with API remotely
====================================

* In the python code worked server install needed libraries::
      
     # python -m pip install esl
     # python -m pip install FreeSWITCH-ESL-Python

* Create script with `channel_api.py <https://github.com/jamalshahverdiev/freeswitch-codes/blob/master/fs-api-remotely/channel_api.py>`_

* Add the following lines to the "/etc/freeswitch/autoload_configs/acl.conf.xml" file in the FreeSWITCH server(10.50.63.228 IP is place from where channel_api.py code is connecting to the FreeSWITCH server)::
     
     <list name="loopback.auto" default="allow">
        <node type="allow" cidr="10.50.63.228/32"/>
     </list>

* At the end restart FreeSWITCH server::
     
     # systemctl restart freeswitch


* If you want to see the channel variables just create getvars.sh script in the FreeSWITCH server and add the following lines to this script(Don't forget minimum one call must be present at script using time)::
     
     #!/usr/bin/env bash

     # show channels - Show online channels
     vars="uuid direction created created_epoch name state cid_name cid_num ip_addr dest application application_data dialplan context read_codec read_rate read_bit_rate write_codec write_rate write_bit_rate secure hostname presence_id presence_data accountcode callstate callee_name callee_num callee_direction call_uuid sent_callee_name sent_callee_num initial_cid_name initial_cid_num initial_ip_addr initial_dest initial_dialplan initial_context"

     # show calls - Show real calls
     vars2="uuid direction created created_epoch name state cid_name cid_num ip_addr dest presence_id presence_data accountcode callstate callee_name callee_num callee_direction call_uuid hostname sent_callee_name sent_callee_num b_uuid b_direction b_created b_created_epoch b_name b_state b_cid_name b_cid_num b_ip_addr b_dest b_presence_id b_presence_data b_accountcode b_callstate b_callee_name b_callee_num b_callee_direction b_sent_callee_name b_sent_callee_num call_created_epoch"

     uuid=`fs_cli -x 'show channels' | grep inbound | cut -f1 -d','`
     undef="_undef_"
     #for var in `echo $vars`
     for var in `echo $vars2`
     do
        newvar=`fs_cli -x "uuid_getvar $uuid $var"`
        if [ "$undef" != "$newvar" ]
        then
            echo ""
            echo Variable name is: $var
            echo Result is: $newvar
        fi
     done


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

