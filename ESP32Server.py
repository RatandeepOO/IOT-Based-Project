import network
import socket
import time
from machine import Pin

# Initialize relays
light_relay1 = Pin(12, Pin.OUT)
light_relay2 = Pin(14, Pin.OUT)
light_relay3 = Pin(27, Pin.OUT)
light_relay4 = Pin(26, Pin.OUT)
fan_relay = Pin(25, Pin.OUT)

def connect_to_wifi(ssid, password):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)
    
    while not station.isconnected():
        print("Connecting to WiFi...")
        time.sleep(1)
    
    print("Connected to WiFi!")
    print("IP Address:", station.ifconfig()[0])
    return station.ifconfig()[0]

def create_response(content):
    return 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nAccess-Control-Allow-Origin: *\r\n\r\n' + content

def handle_request(request):
    print("Request received:", request)
    if '/light1/on' in request:
        light_relay1.value(1)
        return create_response("Light 1 turned on")
    elif '/light1/off' in request:
        light_relay1.value(0)
        return create_response("Light 1 turned off")
    elif '/light2/on' in request:
        light_relay2.value(1)
        return create_response("Light 2 turned on")
    elif '/light2/off' in request:
        light_relay2.value(0)
        return create_response("Light 2 turned off")
    elif '/light3/on' in request:
        light_relay3.value(1)
        return create_response("Light 3 turned on")
    elif '/light3/off' in request:
        light_relay3.value(0)
        return create_response("Light 3 turned off")
    elif '/light4/on' in request:
        light_relay4.value(1)
        return create_response("Light 4 turned on")
    elif '/light4/off' in request:
        light_relay4.value(0)
        return create_response("Light 4 turned off")
    elif '/fan/on' in request:
        fan_relay.value(1)
        return create_response("Fan turned on")
    elif '/fan/off' in request:
        fan_relay.value(0)
        return create_response("Fan turned off")
    else:
        return create_response("Invalid command")

def start_server():
    ssid = input("SSID: ")
    password = input("Password: ")
    ip = connect_to_wifi(ssid, password)
    
    # Start the HTTP server on port 80
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    print(f"HTTP server started at http://{ip}")
    
    while True:
        try:
            conn, addr = s.accept()
            print(f"Connection from {addr}")
            request = conn.recv(1024).decode()
            response = handle_request(request)
            conn.send(response.encode())
            conn.close()
        except Exception as e:
            print("Error:", e)
            continue

if __name__ == "__main__":
    start_server()
