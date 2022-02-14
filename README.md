These files are created to run in BeagleBone Black. 

Dht.py retrieves data from DHT22 sensor and publish these data to a cloud MQTT broker. 
The original code for the sensor is taken from Adafruit libraires https://github.com/adafruit/Adafruit_Python_DHT/blob/master/examples/AdafruitDHT.py
The code for MQTT client is originally taken from www.steves-internet-guide.com and then is adapted for my project.

Stepper_BBB_mqtt.py, is a basic "half step control method" for stepper motor. 
