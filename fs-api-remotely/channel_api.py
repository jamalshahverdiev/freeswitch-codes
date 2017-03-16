#!/usr/bin/env python2.7
from optparse import OptionParser
import sys
import ESL

def main(argv):
    parser = OptionParser()
    parser.add_option('-a', '--auth', dest='auth', default='ClueCon', help='ESL password')
    parser.add_option('-s', '--server', dest='server', default='10.50.3.114', help='FreeSWITCH server IP address')
    parser.add_option('-p', '--port', dest='port', default='8021', help='FreeSWITCH server event socket port')
    parser.add_option('-c', '--command', dest='command', default='status', help='command to run, surround multi-word commands in ""s')

    (options, args) = parser.parse_args()

    con = ESL.ESLconnection(options.server, options.port, options.auth)

    if not con.connected():
        print('Not Connected')
        sys.exit(2)
    else:
        uuid = con.api("create_uuid").getBody()
        print(uuid)
        print('-----------------------')
        print(con.events("plain", "all"))
        print('-----------------------')

    print('######################################')
    print(con.socketDescriptor())
    print(con.connected())
    #print(con.send('$command'))
    print(con.getInfo())
    print('######################################')
    #print(con.events("plain", "all"))
    print(con.recvEvent())
    print('######################################')
    # Run command
    e = con.api(options.command)
    command = 'shift'
    args = ' '.join(argv)
    b = con.bgapi(command, args, uuid)
    print(b)
    if e:
#        print(e.serialize())
        print(e.getHeader('1e4ae024-972f-4f72-a3fd-15713d9847b2'))
        print('********************************************')
        print(e.getBody())
        print(e.getType())
        print(e.firstHeader())
        print(e.nextHeader())

if __name__ == '__main__':
    main(sys.argv[1:])

