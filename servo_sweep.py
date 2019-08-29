import smbus, time

bus = smbus.SMBus(1)
addr = 0x40

bus.write_byte_data(addr, 0, 0x20) # enable the chip
time.sleep(.25)

bus.write_byte_data(addr,0, 0x10) # enablpe prescale change as noted in datasheet
time.sleep(.25)

bus.write_byte_data(addr, 0xfe, 0x79) #changes the prescale register to 50Hz
bus.write_byte_data(addr, 0, 0x20) # enables the chip
time.sleep(.25)

bus.write_word_data(addr, 0x06, 0) # ch1 startaddress

def servo_to_degrees(servo_start, servo_end, degrees):
    ms_degree = 1250/360
    servo_time = ms_degree * degrees

    bus.write_word_data(addr, servo_end, servo_time) 
    time.sleep(.20)
    bus.write_word_data(addr, servo_start, 0)
    print(degree + " : " + servo_time)


servo_to_degrees(0x06, 0x08, 25)
time.sleep(.20)

servo_to_degrees(0x06, 0x08, 45)
time.sleep(.20)

servo_to_degrees(0x06, 0x08, 90)
time.sleep(.20)