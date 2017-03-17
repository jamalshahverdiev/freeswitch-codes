========================================
FreeSWITCH IVR configuration with Python
========================================

* If you want configure your own IVR  then firstly uncomment the following line in the /etc/freeswitch/autoload_configs/modules.conf.xml file::

     <load module="mod_flite"/>

* In the "/etc/freeswitch/dialplan/default" folder create new "welcome.xml" IVR configuration file for the "2920" extension and add the following lines. This configuraions calls "welcome.py" python script file::
     <include>
       <extension name="welcome_ivr">
         <condition field="destination_number" expression="^2920$">
           <action application="python" data="welcome"/>
         </condition>
       </extension>
     </include>


* In the "/usr/share/freeswitch/scripts" folder create python file `welcome.py <https://github.com/jamalshahverdiev/freeswitch-codes/blob/master/fs-ivr-python/welcome.py>`_


* Restart FreeSWITCH server::

     # systemctl restart freeswitch

* At the end just call from sip client to "2920" number and listen Text to Speech.
