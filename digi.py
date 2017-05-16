#!/usr/bin/env python3
import logging
import shutil
import telnetlib
import re
import time
import sys
import os
import getopt
from optparse import OptionParser


# Define the logging module
############################################################################################################
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s  %(levelname)-6s %(message)s',
                datefmt='%m-%d-%Y %H:%M:%S',
                filename='/tmp/digi-port-server.log',
                filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s  %(levelname)-6s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
############################################################################################################
def functionCheck():
    # Connect to ....
    tn = telnetlib.Telnet('192.168.254.254',23)
    #tn.set_debuglevel(2) # Debug mode
    # username / password
#login: root
#password:
#> help

    tn.expect([re.compile(b"login: "),])
    tn.write("root".encode('ascii') + b"\r\n")
    tn.expect([re.compile(b"password: "),])
    tn.write("dbps".encode('ascii') + b"\r\n")
    time.sleep(.5)
    # Settings
    cmd_list = ('show config','show line','show profile')
    for i in cmd_list:
        if i == 'rn':
            tn.write(b"\r\n")
            time.sleep(2)
        else:
            print("start to run command "+ "\033[31m" +  i +  "\033[0m" )
            tn.write(i.encode('ascii') + b"\r\n")
            time.sleep(2)
            result=tn.read_very_eager().decode('ascii')
            tcpserver=re.compile('tcpsockets')
            tcp_ser = 0
            if tcpserver.search(result):
               tcp_ser = 1 
            if tcp_ser:
                print("\033[32mwe found the tcp server mode is setup now\033[0m")
            #print(result)
            logging.debug(result)
    #print(tn.read_very_eager().decode('ascii'))
#    result = tn.read_all().decode('ascii')
#   logging.debug(result)
    print("close the telnet session now")
    tn.close()
functionCheck()
