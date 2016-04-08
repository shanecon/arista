#!/usr/bin/python
# A script to generate variables in json format for an arista 64Q switch
# Update a mongodb instance with the data

import json
import netaddr
import pymongo
import ptc

__author__ = ['shconnor']
__version__ = "May 2015"

class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

def server_networks(server_networks):
    """Generate server networks /26's.

    Args: network supernet

    Return:
      String: /26
    """
    ip_server_networks = netaddr.IPNetwork(server_networks)
    ip_server_networks.subnet(26)
    subnets = list(ip_server_networks.subnet(26))
    for s in subnets:
         yield str(s)

def asn_d1(r1):
    """Generate bgp asn's.

    Args: range

    Return:
      Integer: Bgp asn
    """
    asn = int(64900)
    for r in range(asn, r1):
        yield r

def port_d1(r1):
    """Generate Arista port range.

    Args: range

    Return:
       String: Ethernet Port
    """
    for r in range(1,r1):
        if str(r) in UPLINK:
            continue
        yield r

def vlan_management(server_subnet):
    """Generate Vlan management ip.

    Args: Server Subnet /26

    Return:
       String: ip address
    """
    ip = netaddr.IPNetwork(server_subnet)
    return str(ip[1])

def csw_bgp():
    """Generate Vlan management ip.

    Args: Server Subnet /26

    Return:
       String: ip address
    """
    for c in range(64740,64760):
        yield c

# D1 core
def d1(r,s_n,bgp_asn_d1,port_d1,csw_asn_d1):
    """Generate instance with json data

    Args: Rack,Server_network,Asn,port,switch,asn

    Return:
       dict: switch data
    """
    # variable definitions
    tacacs_server1 = ''
    tacacs_server2 = ''
    ntp_server1 = ''
    ntp_server2 = ''
    syslog_server1 = ''
    ip_count = int(1)
    ETH_UPLINK = ('d_Eth58/1','d1_Eth60/1','d1_Eth62/1','d1_Eth64/1')
    d1_racks = ['d1_Eth%s/1' %n for n in range(1,19)]
    d1_csw = {
   'd1_csw01':['d1','d1-csw01.nw','Ethernet49/1','10.165.1.'],
   'd2_csw01':['d1','d1-csw02.nw','Ethernet50/1','10.165.2.'],
   'd3_csw01':['d1','d1-csw03.nw','Ethernet51/1','10.165.3.'],
   'd4_csw01':['d1','d1-csw04.nw','Ethernet52/1','10.165.4.']
    }

    for rack in d1_racks:
       if rack in ETH_UPLINK:
           continue
       bgp_neighbor = []
       r[rack]['core'] = 'd1'
       r[rack]['csw_bgp'] = csw_asn_d1
       r[rack]['boot_file'] = 'EOS-4.14.6M.swi'
       r[rack]['syslog_server_1'] = syslog_server1
       r[rack]['location'] = LOCATION
       r[rack]['rack'] = ptc.d1_rack_number[rack]
       r[rack]['tacacs_server_1'] = tacacs_server1
       r[rack]['tacacs_server_2'] = tacacs_server2
       r[rack]['ntp_server_1'] = ntp_server1
       r[rack]['ntp_server_2'] = ntp_server2
       port = port_d1.next()
       for d in d1_csw.values():
           r[rack]['uplink_interfaces'][d[2]]['description'] = '%s-%s:Eth1/%s'\
           %(LOCATION.lower(),d[1],port)
           r[rack]['uplink_interfaces'][d[2]]['ip_address'] = '%s%s'\
            %(d[3],ip_count)
           bgp_neighbor.append('%s%s' %(d[3],int(ip_count - 1)))
           ip_count +=2
           r[rack]['bgp_neighbor']= bgp_neighbor
       r[rack]['server_subnet'] = s_n.next()
       r[rack]['asn'] = bgp_asn_d1.next()
       r[rack]['vlan_management'] = vlan_management(r[rack]['server_subnet'])
    return r

if __name__ == '__main__':
    #try:
    #    conn = pymongo.MongoClient('1.1.1.1', 27017)
    #except pymongo.errors.ConnectionFailure, e:
    #    print "Could not connect to MongoDB: %s" % e
    #db = conn.neteng
    # Hard coded variables
    UPLINK = ('58','60','62','64')
    ASN = 64999
    LOCATION = 'DC'
    # Generators
    bgp_asn_d1 = asn_d1(ASN)
    bgp_asn_csw_d1 = csw_bgp().next()
    s_n = server_networks('10.165.32.0/19')
    p_d1 = port_d1(64)
    # Create json data object
    r1 = AutoVivification()
    r1 = d1(r1,s_n,bgp_asn_d1,p_d1,bgp_asn_csw_d1)
    json_r = json.dumps(r1)
    print json_r
    #db.drop_collection('lsg1_grid_d1')
    #db.lsg1_grid_d1.insert(r1)
