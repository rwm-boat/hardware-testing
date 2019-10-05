import sys,os
import curses
import time
from mqtt_client.subscriber import Subscriber
from threading import Thread
import json

# global variables for UI
mag_compass_reading = 0
int_compass_reading = 0
time_reading = 0
lat_reading = 0
lon_reading = 0
speed_reading = 0
gps_heading_reading = 0

jet1_current = 0 #starboard
jet2_current = 0 #port


def on_compass_received(client, userdata, message):
    global mag_compass_reading
    obj = json.loads(message.payload.decode('utf-8'))
    mag_compass_reading = obj['compass']

def on_internal_compass_received(client, userdata, message):
    global int_compass_reading
    obj = json.loads(message.payload.decode('utf-8'))
    int_compass_reading = obj['heading']

def on_gps_received(client, userdata, message):
    # create global variables for UI
    global time_reading
    global lat_reading
    global lon_reading
    global speed_reading
    global gps_heading_reading
    
    obj = json.loads(message.payload.decode('utf-8'))

    # parse json into global variables
    time_reading = obj["time"]
    lat_reading = obj['latitude']
    lon_reading = obj['longitude']
    speed_reading = obj["speed"]
    gps_heading_reading = obj["course"]

def on_adc_received(client, userdata, message):
    global jet1_current
    global jet2_current

    obj = json.loads(message.payload.decode('utf-8'))
    jet1_current = obj["jet1_amps"]
    jet2_current = obj["jet2_amps"]

def draw(stdscr):
    # Make stdscr.getch non-blocking
    stdscr.nodelay(True)
    stdscr.clear()
    width = 4
    count = 0
    direction = 1

    begin_x = 20
    begin_y = 7
    height = 5
    width = 40

    second_column_width = 25

    start_x_title = int((width // 2) - (len("RWM TELEMETRY") // 2) - len("RWM TELEMETRY") % 2)
    start_x_partition = int((width // 2) - (len("--------------- NAV ---------------") // 2) - len("--------------- NAV ---------------") % 2)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # define static text for UI
   

    while True:
        c = stdscr.getch()

        curses.flushinp()
        stdscr.clear()

        # --- HEADER ---
        stdscr.addstr(0,start_x_title, "RWM TELEMETRY")
        
    
        # --- NAV VALUES ---
        stdscr.addstr(1,start_x_partition, "--------------- NAV ---------------")
        
        stdscr.addstr(2,0,"Mag Compass: ")
        stdscr.addstr(2,second_column_width,str(mag_compass_reading))

        stdscr.addstr(3,0,"Int. Mag Compass: ")
        stdscr.addstr(3,second_column_width,str(round(int_compass_reading,2)))

        stdscr.addstr(4,0,"GPS Compass: ")
        stdscr.addstr(4,second_column_width,str(gps_heading_reading))

        stdscr.addstr(5,0,"GPS Time: ")
        stdscr.addstr(5,second_column_width,str(time_reading))

        stdscr.addstr(6,0,"Latitude: ")
        stdscr.addstr(6,second_column_width,str(round(lat_reading,6)))

        stdscr.addstr(7,0,"Longitude: ")
        stdscr.addstr(7,second_column_width,str(round(lon_reading,6)))

        stdscr.addstr(8,0,"GPS Speed(kn): ")
        stdscr.addstr(8, second_column_width, str(round(speed_reading,2)))

        # --- JET VALUES ---

        stdscr.addstr(9,start_x_partition, "--------------- JET ---------------")
        stdscr.addstr(10,0,"Starboard Jet Current : ")
        
        if(jet1_current < 0):
            stdscr.addstr(10,second_column_width,str(round(jet1_current,2)), curses.color_pair(1))
        else:
            stdscr.addstr(10,second_column_width,str(round(jet1_current,2)), curses.color_pair(2))

        stdscr.addstr(11,0,"Port Jet Current: ")

        if(jet2_current < 0):
            stdscr.addstr(11,second_column_width,str(round(jet2_current,2)), curses.color_pair(1))
        else:
            stdscr.addstr(11,second_column_width,str(round(jet2_current,2)), curses.color_pair(2))

        stdscr.addstr(12,0,"JET Current Delta: ")

        jet_delta = jet1_current - jet2_current

        if(jet_delta < -3 or jet_delta > 3):
            stdscr.addstr(12,second_column_width,str(round(jet_delta,2)), curses.color_pair(1))
        else:
            stdscr.addstr(12,second_column_width,str(round(jet_delta,2)), curses.color_pair(2))


        

     
        

        time.sleep(0.01)

# ==================
# -- MAIN METHOD -- 
# ==================
if __name__ == '__main__':

    try:
        default_subscriptions = {
            "/status/compass": on_compass_received,
            "/status/gps" : on_gps_received,
            "/status/adc" : on_adc_received,
            "/status/internal_compass" : on_internal_compass_received
        }
        subber = Subscriber(client_id="telemetry_live", broker_ip="192.168.1.170", default_subscriptions=default_subscriptions)
        thread = Thread(target=subber.listen)
        thread.start()

       
        curses.wrapper(draw)
    except KeyboardInterrupt:
        
        curses.endwin()
       
        
    

        
    