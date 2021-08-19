import can
from cryptography.fernet import Fernet
from can import Message

bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=2500000)


key = Fernet.generate_key()
fkey = open("keystorage.txt",'wb')
w = fkey.write(key)
print('Key is generated')
#print("Key is ",key)
cipher = Fernet(key)

##hexa array to be sent on can data frame
message = bytearray([0, 25, 0, 1, 3, 1, 4, 1])
#print("Original data without encryption : ",message)
##hexa convert into string and encode
message_string = ' '.join(map(str, message)).encode()
#print("Bytearray after encode : ",message_string)
##message_string after encryption
encrypted_msg = cipher.encrypt(message_string)

fkey = open("keystorage.txt","rb")
key2 = fkey.read()
cipher = Fernet(key2)
#originalmsg = cipher.decrypt(msg1)

print("Encypted msg : " ,encrypted_msg)
##split encrypted msg to 8 string charaters
info = [encrypted_msg[i:i+8] for i in range(0, len(encrypted_msg), 8)]
split_string = encrypted_msg.decode()

##string convert into hexa
hex_data = [ord(c) for c in split_string]


#newmessage = hex_data[0:8]
def split_list(lst,n):
    result = list((lst[j:j+n] for j in range (0, len(lst),n)))
    return result
n = 8
encrypted_data = split_list(hex_data,n)
#print(encrypted_data)

try:
    for enc_data in encrypted_data:

        data = Message(data=enc_data)
        bus.send(data)

    print("Message sent on {}" .format(bus.channel_info))

except can.CanError:
    print(can.CanError)