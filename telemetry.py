import sys,os
import curses
import time
from mqtt_client.subscriber import Subscriber
from threading import Thread
import json

# global variables for UI
# From '/status/compass'
kalman_lp_live = 0
int_compass_reading = 0
# From '/status/gps'
time_reading = 0
lat_reading = 0
lon_reading = 0
speed_reading = 0
gps_heading_reading = 0
gps_distance = 0
# From '/status/temp'
jet1_temp = 0
jet2_temp = 0
compartment_temp = 0
# From '/status/adc'
jet1_current = 0 #starboard
jet2_current = 0 #port
pack_voltage = 0
# From '/status/vector'
target_heading = 0
magnitude = 0


def on_compass_received(client, userdata, message):
    global kalman_lp_live
    obj = json.loads(message.payload.decode('utf-8'))
    kalman_lp_live = obj['kalman_lp']

def on_internal_compass_received(client, userdata, message):
    global int_compass_reading
    obj = json.loads(message.payload.decode('utf-8'))
    int_compass_reading = obj['heading']

def on_gps_received(client, userdata, message):
    global time_reading
    global lat_reading
    global lon_reading
    global speed_reading
    global gps_heading_reading
    global gps_distance
    
    obj = json.loads(message.payload.decode('utf-8'))

    time_reading = obj["time"]
    lat_reading = obj['latitude']
    lon_reading = obj['longitude']
    speed_reading = obj["speed"]
    gps_heading_reading = obj["course"]
    gps_distance = obj['distance']

def on_adc_received(client, userdata, message):
    global jet1_current
    global jet2_current
    global pack_voltage

    obj = json.loads(message.payload.decode('utf-8'))
    jet1_current = obj["jet1_amps"]
    jet2_current = obj["jet2_amps"]
    pack_voltage = obj['pack_voltage']
    
def on_temp_received(client, userdata, message):
    global jet1_temp
    global jet2_temp
    global compartment_temp

    obj = json.loads(message.payload.decode('utf-8'))
    jet1_temp = obj["jet1_temp"]
    jet2_temp = obj["jet2_temp"]
    compartment_temp = obj["compartment_temp"]

def on_vector_received(client, userdata, message):
    global target_heading
    global magnitude

    obj = json.loads(message.payload.decode('utf-8'))
    target_heading = obj["heading"]
    magnitude = obj["magnitude"]

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
        try:
            c = stdscr.getch()

            curses.flushinp()
            stdscr.clear()

            # --- HEADER ---
            stdscr.addstr(0,start_x_title, "RWM TELEMETRY")

            # --- NAV VALUES ---
            stdscr.addstr(1,0, "----------------- COMPASS -----------------")
            
            stdscr.addstr(2,0,"KLP Heading: ")
            stdscr.addstr(2,second_column_width,str(kalman_lp_live))

            stdscr.addstr(3,0,"GPS Heading: ")
            stdscr.addstr(3,second_column_width,str(round(gps_heading_reading,3)))

            stdscr.addstr(4,0,"Target Heading: ")
            stdscr.addstr(4,second_column_width,str(target_heading))

            stdscr.addstr(5,0, " ------------------ GPS ------------------")

            stdscr.addstr(6,0,"Latitude: ")
            stdscr.addstr(6,second_column_width,str(round(lat_reading,6)))

            stdscr.addstr(7,0,"Longitude: ")
            stdscr.addstr(7,second_column_width,str(round(lon_reading,6)))

            stdscr.addstr(8,0,"GPS Speed(kn): ")
            stdscr.addstr(8, second_column_width, str(round(speed_reading,2)))

            stdscr.addstr(9,0,"GPS distance (NM): ")
            stdscr.addstr(9, second_column_width, str(gps_distance))

            # --- JET VALUES ---
            stdscr.addstr(10,0, "--------------- CURRENT(A)-----------------")
            stdscr.addstr(11,0,"Starboard: ")

            jet1_amps = (jet1_current)
            jet2_amps = (jet2_current)
            
            if(jet1_current < 0):
                stdscr.addstr(11,second_column_width,str(round(jet1_amps,2)), curses.color_pair(1))
            else:
                stdscr.addstr(11,second_column_width,str(round(jet1_amps,2)), curses.color_pair(2))

            stdscr.addstr(12,0,"Port: ")

            if(jet2_current < 0):
                stdscr.addstr(12,second_column_width,str(round(jet2_amps,2)), curses.color_pair(1))
            else:
                stdscr.addstr(12,second_column_width,str(round(jet2_amps,2)), curses.color_pair(2))

            stdscr.addstr(13,0,"Delta: ")

            jet_delta = jet1_amps - jet2_amps

            if(jet_delta < -3 or jet_delta > 3):
                stdscr.addstr(13,second_column_width,str(round(jet_delta,2)), curses.color_pair(1))
            else:
                stdscr.addstr(13,second_column_width,str(round(jet_delta,2)), curses.color_pair(2))

            stdscr.addstr(14,0, "---------------- TEMP(C) -----------------")

            stdscr.addstr(15,0,"Starboard: ")
            stdscr.addstr(15,second_column_width,str(jet1_temp))

            stdscr.addstr(16,0,"Port: ")
            stdscr.addstr(16,second_column_width,str(jet2_temp))

            stdscr.addstr(17,0,"Compartment: ")
            stdscr.addstr(17,second_column_width,str(compartment_temp))

            stdscr.addstr(18,0,"Pack Voltage:  ")
            stdscr.addstr(18,second_column_width,str(round(pack_voltage,2)))

            time.sleep(0.1)
        except Exception:
            pass

# ==================
# -- MAIN METHOD -- 
# ==================
if __name__ == '__main__':

    try:
        default_subscriptions = {
            "/status/compass": on_compass_received,
            "/status/gps" : on_gps_received,
            "/status/adc" : on_adc_received,
            "/status/internal_compass" : on_internal_compass_received,
            "/status/temp" : on_temp_received,
            "/status/vector" : on_vector_received
        }
        subber = Subscriber(client_id="telemetry_live_feedr", broker_ip="192.168.1.170", default_subscriptions=default_subscriptions)
        thread = Thread(target=subber.listen)
        thread.start()

       
        curses.wrapper(draw)
    except KeyboardInterrupt:
        
        curses.endwin()
       
        
    

        
    