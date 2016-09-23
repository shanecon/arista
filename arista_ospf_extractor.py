#!/usr/bin/python
import pyeapi
import pymongo
import threading
import switch_list

__author__ = ['shane@']
__version__ = "August 2016"

#ileaf collection for threading
def ileaf_collect(ic):
    # connect to the node
    node = pyeapi.connect_to(ic)
    # insert running config into neteng database with collection ileaf
    db.ileaf_ospf.insert(node.enable(['show hostname','show ip ospf'])
    ,check_keys=False)
    # check_keys false otherwise keys with '.' contained in them raise an error

#spine collection for threading
def spine_collect(sp):
    # connect to the node
    node = pyeapi.connect_to(sp)
    # insert running config into neteng database with collection ileaf
    db.spine_ospf.insert(node.enable(['show hostname','show ip ospf']),
    check_keys=False)
    # check_keys false otherwise keys with '.' contained in them raise an error

#eleaf collection for threading
def eleaf_collect(el):
    # connect to the node
    node = pyeapi.connect_to(el)
    # insert running config into neteng database with collection ileaf
    db.eleaf_ospf.insert(node.enable(['show hostname','show ip ospf']),
    check_keys=False)
    # check_keys false otherwise keys with '.' contained in them raise an error

#icore collection for threading
def icore_collect(ic):
    # connect to the node
    node = pyeapi.connect_to(ic)
    # insert running config into neteng database with collection ileaf
    db.icore_ospf.insert(node.enable(['show hostname','show ip ospf']),
    check_keys=False)
    # check_keys false otherwise keys with '.' contained in them raise an error

# import from switch_list
ileaf = switch_list.ileaf
spine = switch_list.spine
eleaf = switch_list.eleaf
icore = switch_list.icore

if __name__ == '__main__':
    try:
        conn = pymongo.MongoClient('10.0.0.0', 27017)
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
    db.drop_collection('ileaf_ospf')
    db.drop_collection('spine_ospf')
    db.drop_collection('eleaf_ospf')
    db.drop_collection('icore_ospf')
    threads = []
    # loop through ileaf arista devices
    for il in ileaf:
        t = threading.Thread(target=ileaf_collect, args=(il,))
        threads.append(t)
        t.start()
    # loop through spine arista devices
    for sp in spine:
        t = threading.Thread(target=spine_collect, args=(sp,))
        threads.append(t)
        t.start()
    # loop through eleaf arista devices
    for el in eleaf:
        t = threading.Thread(target=eleaf_collect, args=(el,))
        threads.append(t)
        t.start()
    # loop through icore arista devices
    for ic in icore:
        t = threading.Thread(target=icore_collect, args=(ic,))
        threads.append(t)
        t.start()
