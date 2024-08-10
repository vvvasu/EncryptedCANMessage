import can
from cryptography.fernet import Fernet
from can import Message

# Initialize CAN bus interface
bus = can.interface.Bus(interface='socketcan', channel='vcan0', bitrate=2500000)

# Generate encryption key and store it in a file
key = Fernet.generate_key()
with open("keystorage.txt", 'wb') as fkey:
    fkey.write(key)
print('\nEncryption key generated and stored.\n')

# Initialize Fernet cipher with the generated key
cipher = Fernet(key)

# Define the message to be sent (as a bytearray)
message = bytearray([0, 25, 0, 1, 3, 1, 4, 1])

# Convert bytearray to a string, then encode to bytes
message_string = ' '.join(map(str, message)).encode()

# Encrypt the message string
encrypted_msg = cipher.encrypt(message_string)
print("\nEncrypted message:\n", encrypted_msg)

# Reload the key from file for decryption (example of key retrieval)
with open("keystorage.txt", "rb") as fkey:
    key2 = fkey.read()
cipher = Fernet(key2)

# Split the encrypted message into chunks of 8 bytes each
def split_list(lst, n):
    """Splits a list into chunks of size n."""
    return [lst[i:i + n] for i in range(0, len(lst), n)]

# Convert encrypted message to a list of hexadecimal values
split_string = encrypted_msg.decode()
hex_data = [ord(c) for c in split_string]

# Split the hexadecimal data into chunks suitable for CAN messages
n = 8
encrypted_data = split_list(hex_data, n)

# Send the encrypted data over the CAN bus
try:
    for enc_data in encrypted_data:
        data = Message(data=enc_data)
        bus.send(data)

    print("\nMessage sent on {}\n".format(bus.channel_info))

except can.CanError as e:
    print(f"CAN error: {e}")
