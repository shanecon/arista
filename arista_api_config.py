#!/usr/bin/python
# A script to take host names and commands and configure
# Arista switches
import json
from jsonrpclib import Server
import ssl
import getpass
import socket
import argparse
import os

__author__ = ['shane']
__version__ = "Apr 2016"

# Disable ssh HTTPS certificates checking by default
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

def resolve_host(hostname):
   """Resolve dns name to ip address

    Args: hostname

    Return:
      ip or false
    """
   try:
      ip = socket.gethostbyname(hostname)
      return "%s" % ip
   except:
      return False

# function to grab password from user for later use
def get_user_info():
    """Get password of the user to login with.

    Args: None

    Return:
      Tuple: (password)
    """
    password = getpass.getpass('LDAP Password: ')
    if len(password) > 8:
        return (password)
    else:
        print('Password entered is less than 8 characters long')
        get_user_info()

# execute commands on arista with the api
def execute_commands(hostname,ip,commands):
  """ Execute commands.

    Args: hostname, ip, commands

    Return:
      Boolean
  """
  try:
    my_headers = {'content-type': 'application/json-rpc'}

    switch = Server("https://"+username+":"+password+"@"+ip+"/command-api")

    try:
      response = switch.runCmds( 1, commands )
      print response
    except Exception, e:
        print "Failed : %s" % str(e)
        return
    return True
  except Exception, e:
      print "Failed : %s" % str(e)
      return False

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Configure arista with api')
  parser.add_argument('-file',help='Enter the file with hostname list')
  parser.add_argument('-commands',help='Enter the file with commands')
  args = parser.parse_args()
  if args.file:
    if os.path.exists(args.file):
       print 'file:', args.file
       filename = args.file
    else:
        exit('Given file doesnt exist.Please provide the correct file')
  else:
    exit('No input.Please enter the file')
  if args.commands:
    if os.path.exists(args.commands):
       print 'commands:', args.commands
       commands_file = args.commands
    else:
        exit('Given commands file doesnt exist.Please provide the correct file')
  else:
    exit('No input.Please enter the commands file')

  with open(commands_file) as f:
    commands = [cmd.strip() for cmd in f]

  username = getpass.getuser()
  password = get_user_info()

  lines =  open(filename).readlines()
  for line in lines:
      hostname = line.strip()
      print hostname
      ip = resolve_host(hostname)
      if ip:
        res = execute_commands(hostname,ip,commands)
        if res:
           print "Executed commands on {0} " .format(hostname)
        else:
           print "Command Execution failed on {0}" .format(hostname)
      else:
        print "{0} doesn't resolve".format(hostname)
