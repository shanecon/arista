#!/usr/bin/python
import pyeapi
import pymongo

# have to easy_install pyeapi and pymongo

__author__ = ['shane@']
__version__ = "Feb 2016"

if __name__ == '__main__':
   try:
      #  needs a mongodb instance running on your localhost
      conn = pymongo.MongoClient('127.0.0.1', 27017)
   except pymongo.errors.ConnectionFailure, e:
      print "Could not connect to MongoDB: %s" % e
   # connecting to the database named neteng
   db = conn.neteng
   # load predefined listing of nodes and values of the format:
   # each device
   #[connection:$DEVICE_NAME]
   #host: $IP
   # once per file
   #[DEFAULT]
   #username: $USER
   #password: $PASS
   #transport: https
   pyeapi.load_config('~/.eapi.conf')
   #reset collection ileaf spine eleaf icore
   db.drop_collection('i_switch')
   db.drop_collection('i_switchd')
   i_switch = ('i_switch1','i_switch2')
   i_switchd = ('i_switch1d','i_switch2d')
   # loop through ileaf connections
   for ic in i_switch:
      # connect to the node
      node = pyeapi.connect_to(ic)
      # insert running config into neteng database with collection ileaf
      db.i_switch.insert(node.enable('show running-config'),check_keys=False)
      # check_keys false otherwise keys with '.' contained in them raise an error
   # loop through icored connections
   for icd in iswitch_d:
      # connect to the node
      node = pyeapi.connect_to(icd)
      # insert running config into neteng database with collection ileaf
      db.iswitch_d.insert(node.enable('show running-config'),check_keys=False)
      # check_keys false otherwise keys with '.' contained in them raise an error
