import can
from cryptography.fernet import Fernet

bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=2500000)


message_string = ""
encrypted_data = ""
rmessage = []

while True:
    message = bus.recv()

    def fullmessage():

        encrypted_msg = message
        print(encrypted_msg)

    fullmessage()


    def decrypted_data():

        msg_decode = message.data.decode()
        rmessage.append(msg_decode)

        message_string = ''.join(map(str,rmessage))
        #print(rmessage)
        encrypted_data = message_string
        if len(encrypted_data) == 120:

            enc_msg = encrypted_data.encode()
            print("Encrypted msg : ",enc_msg)
            fkey = open("keystorage.txt", 'rb')
            key = fkey.read()
            #fkey.close()

            cipher = Fernet(key)

            original_data = cipher.decrypt(enc_msg)
            byte_array = ([original_data])
            print("This is the original data frame : ",byte_array)

    decrypted_data()














