#!/usr/bin/python
import getpass
import sys
import argparse
import os
import ssl
import switch_list
import paramiko
from jsonrpclib import Server

__author__ = ['shane@']
__version__ = "Oct 2018"

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
    for a in list(switch_list.il_dc1_mgt):
        arista_devices.append(a+".com")
    for a in list(switch_list.ic_dc1_mgt):
        arista_devices.append(a+".com")
    for a in list(switch_list.sp_dc1l_mgt):
        arista_devices.append(a+".com")
    for a in list(switch_list.el_dc1_mgt):
        arista_devices.append(a+".com")
    return arista_devices

def arista_devices_dc2():
    """Get management switch names from dc2
    Args: None

    Return:
      List: (arista_devices)
    """
    arista_devices = []
    for a in list(switch_list.il_dc2_mgt):
        arista_devices.append(a+".com")
    for a in list(switch_list.ic_dc2_mgt):
        arista_devices.append(a+".com")
    for a in list(switch_list.sp_dc2_mgt):
        arista_devices.append(a+".com")
    for a in list(switch_list.el_dc2_mgt):
        arista_devices.append(a+".com")
    return arista_devices

def scp(hostlist,username,password,extension):
   """Copy extension locally to arista devices
   Args: Hostlist, password, local username, extension

   Return:
     None
   """
   ssh_client = paramiko.SSHClient()
   ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   for host in hostlist:
       ssh_client.connect(host,username=username,password=password)
       scp_client = ssh_client.open_sftp()
       scp_client.put(extension, '/mnt/flash/%s' %extension)
       scp_client.close()
   sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description='Location,')
    parser.add_argument('-location', choices=['dc1','dc2'],
    help='Enter the colo location dc1|dc2')
    parser.add_argument('-new_extension',
    help='Enter name of extension to be added')
    parser.add_argument('-old_extension',
    help='Enter name of extension to be removed')
    parser.add_argument('--scp', action='store_true',
    help='SCP new extension to arista device.  System exit once finished')
    args = parser.parse_args()
    if args.location == 'dc1':
         hostlist = arista_devices_dc1()
    elif args.location == 'dc2':
         hostlist = arista_devices_dc2()
    #----------------------------------------------------------------
    # Configuration section
    #----------------------------------------------------------------
    EAPI_USERNAME = os.getenv("USER")
    EAPI_PASSWORD = get_user_info()
    EAPI_METHOD = 'https'
    # Disable ssh HTTPS certificates checking by default
    disable_https_cert()
    if args.scp:
        scp(hostlist,EAPI_USERNAME,EAPI_PASSWORD,args.new_extension)
    # configuration loop
    for host in hostlist:
        switch = Server( '%s://%s:%s@%s/command-api' %
                       ( EAPI_METHOD, EAPI_USERNAME, EAPI_PASSWORD, host ) )
        # uninstall extension
        try:
            rc = switch.runCmds( 1, [
                           'no extension %s' %args.old_extension ])
            print( 'Host configured: %s extension removed' % ( host ) )
        except:
            print "Extension %s not installed on %s" %(args.old_extension, host)
        # Pause 1 second between extension being uninstalled and removed
        time.sleep(1)
        # remove uninstalled extension from extension namespace
        try:
            rc = switch.runCmds( 1, [
                           'delete extension:%s' %args.old_extension ])
        except:
            print "Extension %s couldn't be deleted" %args.old_extension
        # New extension logic
        try:
            rc = switch.runCmds( 1, [
                           'copy flash:%s extension:%s' %(args.new_extension,args.new_extension),
                           'extension %s' %args.new_extension ])
            print( 'Host configured: %s extension added' % ( host ) )
        except:
            print "Extension %s already installed on %s" %(args.new_extension, host)
            next
if __name__ == '__main__':
    main()
