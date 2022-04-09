###demo code provided by steve cope at www.steves-internet-guide.com

import paho.mqtt.client as mqtt  #import the client
import time,sys
import Adafruit_DHT
keep_alive=20
def on_disconnect(client, userdata, flags, rc=0):
        print("DisConnected flags"+"result code "+str(rc)+"client_id  ")
        client.connected_flag=False


def on_connect(client, userdata, flags, rc):
        if rc==0:
                print("connected OK Returned code=",rc)
                client.connected_flag=True #Flag to indicate success
        else:
                print("Bad connection Returned code=",rc)
                client.bad_connection_flag=True
                sys.exit(1) #quit
def on_log(client, userdata, level, buf):
        print("log: ",buf)
def on_message(client, userdata, message):
        print("message received  "  ,str(message.payload.decode("utf-8")))
QOS1=1
QOS2=0
CLEAN_SESSION=False
user = "****"
password = "*******"
port=1883
broker="138.3.246.220"
#broker="iot.eclipse.org" #use cloud broker
cname="BBB"
client = mqtt.Client(cname)    #create new instance
client.on_log=on_log #client logging
mqtt.Client.connected_flag=False #create flags
mqtt.Client.bad_connection_flag=False #
mqtt.Client.retry_count=0 #
client.on_connect=on_connect        #attach function to callback
client.on_disconnect=on_disconnect
run_main=False
run_flag=True
retry=0
retry_limit=20
retry_delay_fixed=5
connected_once=False
count=0
stime=time.time()
retry_delay=retry_delay_fixed
try:

        while run_flag: #outer loop
            #print("in loop",client.connected_flag)
            ### this does the work
                client.loop(0.01)
                sensor_args = { '11': Adafruit_DHT.DHT11,
                                '22': Adafruit_DHT.DHT22,
                                '2302': Adafruit_DHT.AM2302 }
                if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
                        sensor = sensor_args[sys.argv[1]]
                        pin = sys.argv[2]
                else:
                        print('Usage: sudo ./Adafruit_DHT.py [11|22|2302] <GPIO pin number>')
                        print('Example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO pin #4')
                        sys.exit(1)

        # Try to grab a sensor reading.  Use the read_retry method which will retry up
        # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
                humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
                if humidity is not None and temperature is not None:
                        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
                else:
                        print('Failed to get reading. Try again!')
                        sys.exit(1)
                if client.connected_flag:     #this is main loop
                        print("in Main Loop")
                        msg="test message"+str(count)
                        ret=client.publish("iot",('{0:0.1f}, {1:0.1f}'.format(temperature, humidity)))
                        print("publish",ret)
                        time.sleep(5)
             #######
            ###handles reconnect
                rdelay=time.time()-stime

                if not client.connected_flag and rdelay>retry_delay:
                        print("rdelay= ",rdelay)
                        try:
                                retry+=1
                                if connected_once:
                                        print("Reconnecting attempt Number=",retry)
                                else:
                                        print("Connecting attempt Number=",retry )

                                client.username_pw_set(user, password=password)
                                client.connect(broker,port)
                                while not client.connected_flag:
                                        client.loop(0.01)
                                        time.sleep(1) #wait for connection to complete
                                        stime=time.time()
                                        retry_delay=retry_delay_fixed
                                connected_once=True
                                retry=0 #reset
                        except Exception as e:
                                print("\nConnect failed : ",e)
                                retry_delay=retry_delay*retry_delay
                                if retry_delay>1200:
                                        retry_delay=1200
                                print("retry Interval =",retry_delay)
                                if retry>retry_limit:
                                        sys.exit(1)
except KeyboardInterrupt:
        print("interrrupted by keyboard")

print("quitting")
client.disconnect()


