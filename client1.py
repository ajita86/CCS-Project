import socket
import time
import random

# define the IP address and port number of the server
SERVER_IP = '0.0.0.0'
SERVER_PORT = 8000

# create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server
client_socket.connect((SERVER_IP, SERVER_PORT))

# send an initial string to the server
client_socket.send(b'network')
response = client_socket.recv(4096)
print(response)

window_size = 8
packet_size = 1
total_packets = 1000
max_seq_number = 65536
curr_packet_number = 0
dropped_packets = []
total_sent = 0
swt = 0
prev_ack = 0
# drop_packets = []

def toBeOrNotToBe():
    return (random.randint(1, 100) == 1)

dropped_sequences_csv = open("dropped_sequences.csv", "w")
dropped_sequences_csv.write("Sequence_number,timestamp\n")

window_size_csv = open("window_size.csv", "w")
window_size_csv.write("window_size,timestamp\n")

retransmission_sequences_csv = open("retransmission_sequences.csv", "w")
retransmission_sequences_csv.write("retransmission_sequences,timestamp\n")

if response == b'success':
    print("Let the games begin!!!")

    while(total_sent < total_packets):
        recv_all_packets = True
        if curr_packet_number*packet_size >= max_seq_number:
            curr_packet_number = 0

        if swt >= 100:
            # send stage
            dropped_packets_new = []
            index = 0
            while(index < len(dropped_packets)):
                if(not toBeOrNotToBe()):
                    packet = dropped_packets[index]
                    client_socket.send(str.encode(str(packet)))
                    # to_send.append(packet)
                    del dropped_packets[index]
                    # print("Retransmission: ",curr_packet_number, "- " , packet)
                    retransmission_sequences_csv.write("{},{}\n".format(packet, time.time()))
                    # print("RESEND --->", packet)
                    ack = int(str.encode(str(int((client_socket.recv(4096))))))
                    # print("ACK ", ack)
                    if not (packet == ack):
                        dropped_packets_new.append(packet)
                else:
                    index += 1
                    dropped_packets_new.append(str(seq_number))
                    # print("DROPPED", str(seq_number))
                    dropped_sequences_csv.write("{},{}\n".format(seq_number, time.time()))
            
            dropped_packets.extend(dropped_packets_new)

        to_send = []

        window_size_csv.write("{},{}\n".format(window_size, time.time()))

        for i in range(window_size):
            seq_number = curr_packet_number*packet_size+1

            if not toBeOrNotToBe():
                # recv_all_packets = False
                to_send.append(str(seq_number))
            else:
                if window_size > 1:
                    window_size = int(window_size / 2)
                print ("window_size: ", window_size)
                # dropped_packets.append(str(seq_number))
                print("DROPPED", str(seq_number))
                dropped_sequences_csv.write("{},{}\n".format(seq_number, time.time()))

            curr_packet_number = curr_packet_number + 1
        total_sent += len(to_send)
        swt += len(to_send)
        # random.shuffle(to_send)

        # send stage
        for packet in to_send:
            # print("SND ", packet)
            client_socket.send(str.encode(packet))
            ack = int(str.encode(str(int((client_socket.recv(4096))))))
            # print("ACK ", ack)
            if not(prev_ack + 1 == ack):
            # if not (packet == str(ack)):
                dropped_packets.append(prev_ack + 1);  
                # print("Check")
                # dropped_packets.append(packet)
            prev_ack = ack 

        print("length: ", len(dropped_packets))
        print(dropped_packets)
        
        if (recv_all_packets):
            window_size = window_size * 2


