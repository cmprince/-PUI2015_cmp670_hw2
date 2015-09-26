'''
Created on Sep 21, 2015

@author: cmp670
'''

import sys
import urllib2
import json

if __name__ == '__main__':
    #Get command line arguments; make BusLine upper case.
    APIKey = sys.argv[1]
    BusLine = sys.argv[2].upper()
    
    #Set url for JSON request of MTA BusTime data using key and line inputs
    url = 'http://api.prod.obanyc.com/api/siri/vehicle-monitoring.json?' \
          'key=%s&VehicleMonitoringDetailLevel=calls&LineRef=%s' \
          % (APIKey, BusLine)

    #Collection of node names
    nd1 = 'Siri'
    nd2 = 'ServiceDelivery'
    nd3 = 'VehicleMonitoringDelivery'
    nd4 = 'VehicleActivity'
    nd5 = 'MonitoredVehicleJourney'
    nd6a = 'VehicleRef'
    nd6b = 'VehicleLocation'
    nd7a = 'Latitude'
    nd7b = 'Longitude'

    #Get data and load into busdata object
    request = urllib2.urlopen(url)
    busdata = json.loads(request.read())
    
    #Set the root node containing the individual bus data,
    #If the line number is invalid, nd4 ('VehicleActivity') won't be
    #present, so test for KeyError here.
    try:
        buses = busdata[nd1][nd2][nd3][0][nd4]
    except KeyError:
        print 'Could not find data for line %s. Please verify the line number.'\
                %BusLine
        raise

    print 'Bus Line: %s' %BusLine
    print 'Number of active buses: %s' %len(buses)

    #Loop through list items in buses (one per bus) and display their 
    #IDs and locations:
    i = 1
    for bus in buses:
        busID = bus[nd5][nd6a]
        busLat = bus[nd5][nd6b][nd7a]
        busLon = bus[nd5][nd6b][nd7b]
        print '%i: Bus ID %s is at latitude %s and longitude %s.' \
                %(i, busID, busLat, busLon)
        i += 1
