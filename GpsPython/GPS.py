import time

import serial
import os
from datetime import datetime

firstFixFlag = False # this will go true after the first GPS fix.
firstFixDate = ""
DEBUG = True

# Set up serial:
ser = serial.Serial(
    port='/dev/ttyUSB0',\
    baudrate=4800,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=1)

# Helper function to take HHMM.SS, Hemisphere and make it decimal:
def degrees_to_decimal(data, hemisphere):
    try:
        decimalPointPosition = data.index('.')
        degrees = float(data[:decimalPointPosition-2])
        minutes = float(data[decimalPointPosition-2:])/60
        output = degrees + minutes
        if hemisphere is 'N' or hemisphere is 'E':
            return output
        if hemisphere is 'S' or hemisphere is 'W':
            return -output
    except:
        return ""

# Helper function to take a $GPRMC sentence, and turn it into a Python dictionary.
# This also calls degrees_to_decimal and stores the decimal values as well.
def parse_GPRMC(data):
    data = data.split(',')
    dict = {
            # $GPRMC,161854.000,
            'fix_time': data[1],
            'validity': data[2],
            'latitude': data[3],
            'latitude_hemisphere' : data[4],
            'longitude' : data[5],
            'longitude_hemisphere' : data[6],
            'speed': data[7],
            'true_course': data[8],
            'fix_date': data[9],
            'variation': data[10],
            'variation_e_w' : data[11],
            'checksum' : data[12]
    }
    dict['decimal_latitude'] = degrees_to_decimal(dict['latitude'], dict['latitude_hemisphere'])
    dict['decimal_longitude'] = degrees_to_decimal(dict['longitude'], dict['longitude_hemisphere'])
    return dict

# Main program loop:
while True:
    print "Start : %s" % time.ctime()
    line = ser.readline()
    if "$GPRMC" in line: # This will exclude other NMEA sentences the GPS unit provides.
        if DEBUG is True: 
            print "GPRMC entering..." 
        gpsData = parse_GPRMC(line) # Turn a GPRMC sentence into a Python dictionary called gpsData
        if gpsData['validity'] == "A": # If the sentence shows that there's a fix, then we can log the line
            if DEBUG is True: 
                print "GpsData validity entering..." 

            if firstFixFlag is False: # If we haven't found a fix before, then set the filename prefix with GPS date & time.
                # printf("Date = %s", gpsData['fix_date'])
                # printf("Time = %d", gpsData['fix_time'])

                firstFixDate = gpsData['fix_date'] + "-" + gpsData['fix_time']
                firstFixFlag = True
            else: # write the data to a simple log file and then the raw data as well:
                if DEBUG is True: 
                    print "Writing into database..." 
                
                cus_date = datetime.strptime(gpsData['fix_date'], "%d%m%Y").date()                
                
                # Data to insert 
                os.system("docker exec -u postgres pi_postgis_1 psql tamatatracking -c " +
                    "\"insert into trame ( jour, heure, latitude, longitude, geom ) " + 
                    "values ( current_date ,'"+ gpsData['fix_time']+"',"+str(gpsData['decimal_latitude'])+","+ str(gpsData['decimal_longitude'])+",st_setsrid( st_makepoint( "+ str( gpsData['decimal_longitude']) +","+ str(gpsData['decimal_latitude']) +" ), 4326 ) );\" ")
                time.sleep( 10 )
    
    