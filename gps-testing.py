from gps import *
import time

gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)

lat = 0
lon = 0
speed = 0

def getCurLat():
    return lat
def getCurLon():
    return lon
def getCurSpeed():
    return speed

try:

    while True:
        report = gpsd.next()
        if report['class'] == 'TPV':
            lat =  getattr(report, 'lat', 0.0)
            lon =  getattr(report, 'lon', 0.0)
            speed =  getattr(speed, 'nan')
        time.sleep(.2)

        print("lat: " + str(lat))
        print("lon: " + str(lon))
        print("speed: " + str(speed))
except (KeyboardInterrupt, SystemExit):
    print "done"




