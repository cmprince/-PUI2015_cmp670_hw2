'''
Created on Sep 21, 2015

@author: cmp670
'''

import sys
import urllib2
import json
import csv

if __name__ == '__main__':
    #Get command line arguments; make BusLine upper case.
    APIKey = sys.argv[1]
    BusLine = sys.argv[2].upper()
    FName = sys.argv[3]

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
    nd6a = 'OnwardCalls'
    nd6b = 'VehicleLocation'
    nd7a = 'OnwardCall'
    nd7b = 'Latitude'
    nd7c = 'Longitude'
    nd8a = 'Extensions'
    nd8b = 'StopPointName'
    nd9 = 'Distances'
    nd10 = 'PresentableDistance'

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

    #Write headerrow into csv 
    header = ['Latitude', 'Longitude', 'Stop name', 'Stop status']
    with open(FName, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)    
        csvwriter.writerow(header)

        #Loop through list in myroot (one per bus) and display their 
        #IDs and locations:
        for bus in buses:
            busLat = bus[nd5][nd6b][nd7b]
            busLon = bus[nd5][nd6b][nd7c]
 
            #The next stop, if any, is in the 0th item in node 7a
            #(OnwardCall). If OnwardCall is not present, this will trigger
            #a KeyError, which we capture and substitute values with 'N/A'.
            try:
                busStop = bus[nd5][nd6a][nd7a][0][nd8b]
                busDist = bus[nd5][nd6a][nd7a][0][nd8a][nd9][nd10]
            except KeyError:
                busStop = 'N/A'
                busDist = 'N/A'
            csvwriter.writerow([busLat, busLon, busStop, busDist])

    print 'Wrote data for bus line %s to %s.' %(BusLine, FName)
