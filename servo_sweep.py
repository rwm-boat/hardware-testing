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

for x in range(125):
    
    bus.write_word_data(addr, 0x08, x*10) # ch1 end adress
    time.sleep(.10)
    bus.write_word_data(addr, 0x06, 0)
    print("loop");
for x in range(125):

    bus.write_word_data(addr, 0x08, x*10)
    time.sleep(.10)
    bus.write_word_data(addr, 0x06, 0)
    print("loop back")

