import dht
import network
import ntptime
import ujson
import utime
import upip
from machine import RTC
from machine import Pin
from time import sleep
from third_party import rd_jwt

from umqtt.simple import MQTTClient
# Konstanta-konstanta aplikasi

# WiFi AP Information
AP_SSID = "iphone11"
AP_PASSWORD = "advang5pro"

# Decoded Private Key
PRIVATE_KEY = (21513766964858698543383903921838741956601088750832904272913739266938398916243857121393047279229291042589672650950699557074107470760382987164769023411589707950891893987507830704425434065974839351941214546176375676300030818884458607788338342400412165561077007912393017523849311536660967007375326313254157948954413456860823595967182628807864637972174736104528254409322867938902756299383471053301081822648194462826568290113601108187465519074408584532314144390416602746110152795973572956857714247926637283175300413387117009421820426993224113922616805536174355871588712480040451430968633674639617299524114489814805681788299, 65537, 986776683344755600979782644751014820964384588629380506345708534666170669121702771059210829323332604086616048777908706052531654746261062596965007314574036988271984273409654685101589251908393229655542532093415708423606400072732694127160917607697010386142140863705287252646459717094204294126527471468666536377253826481948804901559151584538944902312717599275180994695246443621479543686616908069852003895788566232596989469410318216418726642796104882052519967235874391049350934693963943380520017949402438758724473763061928508095863375604605658987076101126544356840107934469191077920467862748118114536122304458474652926273, 153868574649425164462348549070693568507792298952553289582896206138750711776943480663294332181734550194372278352491694240504934402877266336633033403980743535986743334351691564125947302645932204021439143211571336321262473338549674866908782460768285318315206168016864162672324593222267279628733132301465018125499, 139819108702837857450114791086415440636812966022295647570189239210810359865405714961842454099761554286983470557934422280482178820257756766846779285591714178120311588355642218636909854013244124752488736240153255058282970937775223795217002969108553083469729298947281322297073445714283861427700896004673554937201)


#Project ID of IoT Core
PROJECT_ID = "iot-2021-tim-01"
# Location of server
REGION_ID = "asia-east1"
# ID of IoT registry
REGISTRY_ID = "esp_coba"
# ID of this device
DEVICE_ID = "esp_coba"

# MQTT Information
MQTT_BRIDGE_HOSTNAME = "mqtt.googleapis.com"
MQTT_BRIDGE_PORT = 8883


dht22_obj = dht.DHT22(Pin(4))
led_obj = Pin(21, Pin.OUT)
def read_dht22():
    # Read temperature from DHT 22
    #
    # Return
    #    * List (temperature, humidity)
    #    * None if failed to read from sensor
    
    try:
        dht22_obj.measure()
        return dht22_obj.temperature()
    except:
        return None
    
    

def connect():
    # Connect to WiFi
    print("Connecting to WiFi...")
    
    # Activate WiFi Radio
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # If not connected, try tp connect
    if not wlan.isconnected():
        # Connect to AP_SSID using AP_PASSWORD
        wlan.connect(AP_SSID, AP_PASSWORD)
        # Loop until connected
        while not wlan.isconnected():
            pass
    
    # Connected
    print("  Connected:", wlan.ifconfig())


def set_time():
    # Update machine with NTP server
    print("Updating machine time...")

    # Loop until connected to NTP Server
    while True:
        try:
            # Connect to NTP server and set machine time
            ntptime.settime()
            # Success, break out off loop
            break
        except OSError as err:
            # Fail to connect to NTP Server
            print("  Fail to connect to NTP server, retrying (Error: {})....".format(err))
            # Wait before reattempting. Note: Better approach exponential instead of fix wiat time
            utime.sleep(0.5)
    
    # Succeeded in updating machine time
    print("  Time set to:", RTC().datetime())


def on_message(topic, message):
    print((topic,message))


def get_client(jwt):
    #Create our MQTT client.
    #
    # The client_id is a unique string that identifies this device.
    # For Google Cloud IoT Core, it must be in the format below.
    #
    client_id = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(PROJECT_ID, REGION_ID, REGISTRY_ID, DEVICE_ID)
    client = MQTTClient(client_id.encode('utf-8'),
                        server=MQTT_BRIDGE_HOSTNAME,
                        port=MQTT_BRIDGE_PORT,
                        user=b'ignored',
                        password=jwt.encode('utf-8'),
                        ssl=True)
    client.set_callback(on_message)

    try:
        client.connect()
    except Exception as err:
        print(err)
        raise(err)

    return client


def publish(client, payload):
    # Publish an event
    
    # Where to send
    mqtt_topic = '/devices/{}/{}'.format(DEVICE_ID, 'events')
    
    # What to send
    payload = ujson.dumps(payload).encode('utf-8')
    
    # Send    
    client.publish(mqtt_topic.encode('utf-8'),
                   payload,
                   qos=1)
def subscribe_command1():
    """Subscribe to commands from controller."""
    print()
    print("Subscribe Command 1")
    print("================================================")
    print()
    client = get_client(jwt)

    # Subscribe to the events
    #mqtt_topic = '/devices/{esp_coba}/commands/#'
    mqtt_topic = '/devices/{}/{}'.format(DEVICE_ID, 'commands/#')
    commands = 'Ubah sampling'
    data = commands.encode("utf-8")
    while True:
        dht22_obj.measure()
        temp = dht22_obj.temperature()
        print(temp)
        sleep(2)
    # Subscribe to the config topic.
    print("Subscribing")
    print(mqtt_topic)
    print()
    client.subscribe(mqtt_topic, qos=1)
    time.sleep(5)

    # Unsubscribe to the config topic.
    print("Unsubscribing")
    print()
    client.unsubscribe(mqtt_topic)
    time.sleep(5)

    release_client(client)

def subscribe_command2():
    """Subscribe to commands from controller."""
    print()
    print("Subscribe Command 2")
    print("================================================")
    print()
    client = get_client(jwt)

    # Subscribe to the events
    #mqtt_topic = '/devices/{esp_coba}/commands/#'
    mqtt_topic = '/devices/{}/{}'.format(DEVICE_ID, 'commands/#')
    commands = 'Minta Suhu Sekarang'
    data = commands.encode("utf-8")
    while True:
        dht22_obj.measure()
        temp = dht22_obj.temperature()
        print(temp)
        break
    # Subscribe to the config topic.

def subscribe_command3():
    """Subscribe to commands from controller."""
    print()
    print("Subscribe Command 2")
    print("================================================")
    print()
    client = get_client(jwt)

    # Subscribe to the events
    #mqtt_topic = '/devices/{esp_coba}/commands/#'
    mqtt_topic = '/devices/{}/{}'.format(DEVICE_ID, 'commands/#')
    commands = 'Ping'
    data = commands.encode("utf-8")
    
    while True:
        led_obj.value(0)
        sleep(1)
        led_obj.value(1)
        sleep(1)
        led_obj.value(0)
        sleep(1)
        led_obj.value(1)
        sleep(1)
        led_obj.value(0)
        sleep(1)
        led_obj.value(1)
        sleep(1)
        led_obj.value(0)
        sleep(1)
        led_obj.value(1)
        sleep(1)
        led_obj.value(0)
        sleep(1)
        led_obj.value(1)
        sleep(1)
        led_obj.value(0)
        sleep(1)
        led_obj.value(1)
        sleep(1)
        led_obj.value(0)
        sleep(1)
        led_obj.value(1)
        sleep(1)
        led_obj.value(0)
        sleep(1)
        led_obj.value(1)
        sleep(1)
        led_obj.value(0)
        sleep(1)
        led_obj.value(1)
        sleep(1)
        led_obj.value(0)
        sleep(1)
        led_obj.value(1)
        sleep(1)
        led_obj.value(0)
        sleep(1)
        led_obj.value(1)
        sleep(1)
        led_obj.value(0)
        sleep(1)
        led_obj.value(1)
        sleep(1)
        led_obj.value(0)
        sleep(1)
        led_obj.value(1)
        sleep(1)
        led_obj.value(0)
        sleep(1)
        led_obj.value(1)
        sleep(1)
        led_obj.value(0)
        sleep(1)
        led_obj.value(1)
        sleep(1)
        led_obj.value(0)
        sleep(1)
        led_obj.value(1)
        sleep(1)
        led_obj.value(0)
        sleep(1)
        led_obj.value(1)
        sleep(1)
        led_obj.value(0)
        sleep(1)
        led_obj.value(1)
        sleep(1)
        led_obj.value(0)
        sleep(1)
        led_obj.value(1)
        sleep(1)
        led_obj.value(0)
        sleep(1)
        led_obj.value(1)
        sleep(1)
        break
    

# Connect to Wifi
connect()
# Set machine time to now
set_time()

# Create JWT Token
print("Creating JWT token.")
start_time = utime.time()
jwt = rd_jwt.create_jwt(PRIVATE_KEY, PROJECT_ID)
end_time = utime.time()
print("  Created token in", end_time - start_time, "seconds.")

# Connect to MQTT Server
print("Connecting to MQTT broker...")
start_time = utime.time()
client = get_client(jwt)
end_time = utime.time()
print("  Connected in", end_time - start_time, "seconds.")

#  Read from DHT22
print("Reading from DHT22")
result = read_dht22()
print("  Temperature:", result)
# Publish a message
print("Publishing message...")
if result == None:
    result = "Fail to read sensor...."
publish(client, result)
    
# Need to wait because command not blocking
utime.sleep(1)

# Disconnect from client
client.disconnect()
#subscribe_command1()
subscribe_command2()
#subscribe_command3()
