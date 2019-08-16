from RPLCD import CharLCD
from RPi import GPIO

GPIO.setWarnings(False)

lcd = CharLCD(numbering_mode=GPIO.BOARD, cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[40, 38, 36, 32, 33, 31, 29, 23])
lcd.write_string('Hello world!')

GPIO.cleanup() 