import RPi.GPIO as GPIO

def on_led_command(client, userdata, message):
    obj = json.loads(message.payload.decode('utf-8'))
    led_selector = obj['led_id']
    led_opp = obj['command']
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(26,GPIO.OUT)
        GPIO.output(led_selector,GPIO.HIGH)
    except Exception:
        print("LED FAILTURE")


default_subscriptions = {
    "/command/led": on_led_command,
}
    
subber = Subscriber(client_id="led_actuator", broker_ip="192.168.1.170", default_subscriptions=default_subscriptions)
subber.listen()

