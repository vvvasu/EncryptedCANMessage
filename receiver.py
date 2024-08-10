import can
from cryptography.fernet import Fernet

# Initialize CAN bus interface
bus = can.interface.Bus(interface='socketcan', channel='vcan0', bitrate=2500000)

encrypted_data = b''
rmessage = []

def fullmessage(message):
    """\nPrints the received message."""
    print("Received encrypted message:", message)

def decrypted_data():
    """Decrypts the message when the accumulated data reaches the expected length."""
    global encrypted_data  # Use global to accumulate encrypted data
    
    # Append the received data directly to encrypted_data
    encrypted_data += message.data

    if len(encrypted_data) == 120:  # Assuming 120 bytes is the full encrypted message length
        print("\nConcatenated encrypted message:\n", encrypted_data)

        # Load the encryption key
        with open("keystorage.txt", 'rb') as fkey:
            key = fkey.read()

        # Initialize Fernet cipher with the key
        cipher = Fernet(key)

        # Decrypt the concatenated message
        original_data = cipher.decrypt(encrypted_data)
        
        # Convert decrypted data to a bytearray
        byte_array = bytearray(original_data)
        print("\nThis is the original data frame:\n", byte_array)

while True:
    message = bus.recv()
    fullmessage(message)
    decrypted_data()
