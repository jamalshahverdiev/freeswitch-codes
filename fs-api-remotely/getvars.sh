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
