import snappi

# Connect to the traffic generator service (Ixia-c service IP)
api = snappi.api(location='http://<ixia-tg-container-ip>:80', ext='ixnetwork')

# Create a config
config = api.config()

# Setup a port
port = config.ports.add(name='port1', location='eth1')  # adjust to match GNS3 interface

# Create a layer 2/3 flow
flow = config.flows.add(name='f1')
flow.tx_rx.port.tx_name = port.name
flow.tx_rx.port.rx_name = port.name
flow.packet.ethernet().ipv4().udp()

flow.size.fixed = 512
flow.rate.percentage = 50
flow.duration.fixed_packets.packets = 100

# Apply configuration and start traffic
api.set_config(config)
api.transmit().start()
