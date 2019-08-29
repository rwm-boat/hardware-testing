import smbus, time
bus = smbus.SMBus(1)
addr = 0x40

## Running this program will move the servo to 0, 45, and 90 degrees with 5 second pauses in between with a 50 Hz PWM signal.

bus.write_byte_data(addr, 0, 0x20) # enable the chip
time.sleep(.25)
bus.write_byte_data(addr, 0, 0x10) # enable Prescale change as noted in the datasheet
time.sleep(.25) # delay for reset
bus.write_byte_data(addr, 0xfe, 0x79) #changes the Prescale register value for 50 Hz, using the equation in the datasheet.
bus.write_byte_data(addr, 0, 0x20) # enables the chip

time.sleep(.25)
bus.write_word_data(addr, 0x06, 0) # chl 0 start time = 0us
bus.write_word_data(addr, 0x0A, 0) # chl 1 start time = 0us
bus.write_word_data(addr, 0x0E, 0) # chl 2 start time = 0us
               
time.sleep(.25)
bus.write_word_data(addr, 0x08, 209) # chl 0 end time = 1.0ms (0 degrees)
bus.write_word_data(addr, 0x0C, 209) 
time.sleep(.25)
bus.write_word_data(addr, 0x08, 312) # chl 0 end time = 1.5ms (45 degrees)
bus.write_word_data(addr, 0x0C, 312)
time.sleep(.25)

time.sleep(.25)
bus.write_word_data(addr, 0x08, 416) # chl 0 end time = 2.0ms (90 degrees)











































