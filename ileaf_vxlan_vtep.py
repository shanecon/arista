#!/usr/bin/python
import getpass
import sys
import argparse
import os
import ssl
import switch_list
from jsonrpclib import Server

__author__ = ['shane@']
__version__ = "May 2018"

# Disable ssh HTTPS certificates checking by default
def disable_https_cert():
    """Disable https cert for arista api access

    Args: None

    Return:
      None
    """
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        # Legacy Python that doesn't verify HTTPS certificates by default
        pass
    else:
        # Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context

def get_user_info():
    """Get password of the user to login with.

    Args: None

    Return:
      Tuple: (password)
    """
    password = getpass.getpass('LDAP Password: ')
    if len(password) > 6:
        return (password)
    else:
        print('Password entered is less than 6 characters long')
        get_user_info()

def arista_devices_dc1():
    """Get management switch names from dc1 

    Args: None

    Return:
      List: (arista_devices)
    """
    arista_devices = []
    for a in list(switch_list.ileaf_dc1_mgt):
        arista_devices.append(a+".int.org")
    for a in list(switch_list.icore_dc1_mgt):
        arista_devices.append(a+".int.org")
    return arista_devices

def arista_devices_dc2():
    """Get management switch names from dc2 

    Args: None

    Return:
      List: (arista_devices)
    """
    arista_devices = []
    for a in list(switch_list.ileaf_dc2_mgt):
        arista_devices.append(a+".int.org")
    for a in list(switch_list.icore_dc2_mgt):
        arista_devices.append(a+".int.org")
    return arista_devices

def main():
    parser = argparse.ArgumentParser(description='Location,Ipaddress')
    parser.add_argument('-location', choices=['dc1','dc2'],
    help='Enter the colo location dc1|dc2')
    parser.add_argument('-ip', help='Enter switch ip address')
    args = parser.parse_args()
    if args.location == 'dc1':
         hostlist = arista_devices_dc1()
    elif args.location == 'dc2':
         hostlist = arista_devices_dc2()
    disable_https_cert()
    #----------------------------------------------------------------
    # Configuration section
    #----------------------------------------------------------------
    #-------------------Configuration - MUST Set ------------------------
    EAPI_USERNAME = os.getenv("USER")
    EAPI_PASSWORD = get_user_info()
    # http or https method
    EAPI_METHOD = 'https'

    for host in hostlist:
        switch = Server( '%s://%s:%s@%s/command-api' %
                       ( EAPI_METHOD, EAPI_USERNAME, EAPI_PASSWORD, host ) )
        rc = switch.runCmds( 1, [ 'enable',
                        'configure',
                        'interface Vxlan1',
                        'vxlan flood vtep add %s' % args.ip  ] )
        print( 'Host configured: %s' % ( host ) )

if __name__ == '__main__':
    main()
