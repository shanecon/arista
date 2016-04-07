#!/usr/bin/python
# shane
# a script that logins to arista devices
# and checks for show interface counter error

import pexpect
import sys
import re
import getpass

__author__ = ['shane']
__version__ = "Feb 2016"

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

# Arista devices
arista_devices = (
"router1",
"router2",
"router3",
"router4",
)

# remove device name from pexpect output string
def split_arista_devices(arista_devices):
   arista = arista_devices.split('.')
   return arista[0]

if __name__ == '__main__':
   password = get_user_info()
   # loop through arista devices login with ssh run senz and report interfaces
   #  with error counts > 0
   for a in arista_devices:
      arista_switch = pexpect.spawn ('ssh -p 22 -o "StrictHostKeyChecking=no"\
      %s' %a)
      arista_switch.maxread = 5000
      arista_switch.expect('[pP]assword:')
      arista_switch.sendline('%s' %password)
      arista_switch.expect('#')
      arista_switch.sendline('senz') #  alias show interface counter error | nz
      arista_switch.expect('.*')
      arista_switch.expect ('#')
      # len of 110 or 118 means no port errors, skip printing device
      # information
      if len(arista_switch.before) == 110 or len(arista_switch.before) == 118:
         arista_switch.sendline ('exit')
         continue
      print "\n%s_interface errors:\n" %a, arista_switch.before.replace\
      (split_arista_devices(a),'')
      print "%s" %format_string
      arista_switch.sendline ('exit')
