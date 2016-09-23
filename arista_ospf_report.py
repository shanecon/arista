#!/usr/bin/python
import pymongo
import re
__author__ = ['shane']
__version__ = "August 2016"

def ospf_area(hostname):
    if re.match('.*[0-9]f$', hostname):
        area = '0.0.0.3'
    elif re.match('.*[0-9]a$', hostname):
        area = '0.0.0.8'
    return area

if __name__ == '__main__':
    try:
    #  needs a mongodb instance running
    #  https://wiki.int.craigslist.org/twiki/bin/view/Main/MongodbAristaJuniper
        conn = pymongo.MongoClient('10.0.0.0', 27017)
    except pymongo.errors.ConnectionFailure, e:
        print "Could not connect to MongoDB: %s" % e
    # connecting to the database named neteng
    db = conn.neteng
    # populate ileaf, spine, eleaf, oob, icore from the db
    ileaf = db.ileaf_ospf.find()
    spine = db.spine_ospf.find()
    eleaf = db.eleaf_ospf.find()
    icore = db.icore_ospf.find()
    # loop through icore arista devices
    for ic in icore:
        try:
            print (ic['result']['hostname'])
            area = ospf_area(ic['result']['hostname'])
        except KeyError:
            pass
        try:
            print ("RouterId %s"
            %ic['result']['vrfs']['default']['instList']['2']['routerId'])
            print ("Number of LSAS %s"
            %ic['result']['vrfs']['default']['instList']['2']['lsaInformation']['numLsa'])
            print("SPF algorithm executed %s"
            %ic['result']['vrfs']['default']['instList']['2']['areaList'][area]['spfCount'])
            print ("Ospf area %s\n" %area)
        except KeyError:
            pass
    # loop through ileaf arista devices
    for i in ileaf:
        try:
            print (i['result']['hostname'])
            area = ospf_area(i['result']['hostname'])
        except KeyError:
            pass
        try:
            print ("RouterId %s"
            %i['result']['vrfs']['default']['instList']['2']['routerId'])
            print ("Number of LSAS %s"
            %i['result']['vrfs']['default']['instList']['2']['lsaInformation']['numLsa'])
            print ("SPF algorithm executed %s"
            %i['result']['vrfs']['default']['instList']['2']['areaList'][area]['spfCount'])
            print ("Ospf area %s\n" %area)
        except KeyError:
            pass
    # loop through spine arista devices
    for s in spine:
        try:
            print (s['result']['hostname'])
            area = ospf_area(s['result']['hostname'])
        except KeyError:
            pass
        try:
            print ("RouterId %s"
            %s['result']['vrfs']['default']['instList']['2']['routerId'])
            print ("Number of LSAS %s" 
            %s['result']['vrfs']['default']['instList']['2']['lsaInformation']['numLsa'])
            print ("SPF algorithm executed %s" 
            %s['result']['vrfs']['default']['instList']['2']['areaList'][area]['spfCount'])
            print ("Ospf area %s\n" %area)
        except KeyError:
            pass
    # loop through eleaf arista devices
    for e in eleaf:
        try:
            print (e['result']['hostname'])
            area = ospf_area(e['result']['hostname'])
        except KeyError:
            pass
        try:
            print ("RouterId %s" 
            %e['result']['vrfs']['default']['instList']['2']['routerId'])
            print ("Number of LSAS %s" 
            %e['result']['vrfs']['default']['instList']['2']['lsaInformation']['numLsa'])
            print ("SPF algorithm executed %s" 
            %e['result']['vrfs']['default']['instList']['2']['areaList'][area]['spfCount'])
            print ("Ospf area %s\n" %area)
        except KeyError:
            pass
