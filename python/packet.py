class Packet:
    def __init__(self, data):
        channel, value, timestamp = data.split(",")
        self.timestamp = timestamp
        self.size = int(value)
        self.channel = int(channel)

    def get_packet_timestamp(self):
        return self.timestamp

    def get_packet_value(self):
        return self.value

    def get_packet_channel(self):
        return self.channel

def handle_packet(packet_list):
    data_list = []
    data_map = dict()
    for packet in packet_list:
        if packet.get_packet_timestamp() in data_map.keys():
            data_map[packet.get_packet_timestamp()] += packet.get_packet_size()
        else:
            data_map[packet.get_packet_timestamp()] = packet.get_packet_size()
    key_list = sorted(data_map.keys())
    for key in key_list:
        # print ("key = ", key, data_map[key])
        data_list.append(data_map[key] / 4096.0)
    return data_list

