Hidden listening sip clients with SPY module


Add the following lines to the "/etc/freeswitch/dialplan/default.xml" file before "Local_Extension":
    <extension name="user_spy">
      <condition field="destination_number" expression="^\*0(\d{4})$">
        <action application="answer"/>
        <action application="userspy" data="$1@${domain_name}"/>
      </condition>
    </extension>


Uncomment the following line in the '/etc/freeswitch/autoload_configs/modules.conf.xml' file:
<load module="mod_spy"/>


At the end restart freeswitch with the following command:
# systemctl restart freeswitch


Just call to *01003 number to listen caller_ID 1003.

