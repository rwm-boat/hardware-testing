from gps import *
import time

gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
try:

    while True:
        report = gpsd.next()
        if report['class'] == 'TPV':
            print getattr(report, 'lat', 0.0)

        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    print "done"


