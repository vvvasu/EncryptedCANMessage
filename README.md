
---
## Testing Symmetric Encryption for Securing Automotive CAN-BUS Networks
*vasu@vdefense.tech*
---

> **Note:** This article demonstrates a test implementation of symmetric encryption to secure CAN-BUS messages in automotive systems using Python. It is intended as a proof of concept for cybersecurity enthusiasts exploring encryption in automotive networks.

### Introduction

As vehicles become more connected, they are exposed to new security vulnerabilities. This article presents a test case for securing the Controller Area Network (CAN-BUS) in vehicles using symmetric encryption. While unsuitable for commercial applications, this proof of concept illustrates how encryption protects communication between Electronic Control Units (ECUs) in a vehicle.

### What is an Electronic Control Unit (ECU)?

An Electronic Control Unit (ECU) is an embedded system that manages specific functions within a vehicle, such as engine control or braking. ECUs communicate via the CAN-BUS, a critical network that enables the coordinated operation of various vehicle subsystems.

### The Role of CAN-BUS in Vehicle Communication

The CAN-BUS allows ECUs to communicate efficiently without a central computer. However, this protocol does not include built-in security features, meaning all messages are transmitted in plain text and are vulnerable to interception and manipulation.

### Structure of a CAN Frame

Below is a basic representation of a CAN frame:

- **Start of Frame:** Marks the beginning of the CAN frame.
- **Identifier:** Contains the message ID and priority.
- **Control Field:** Specifies the length of the data field.
- **Data Field:** Carries the actual data (0 to 8 bytes).
- **CRC Field:** Contains the cyclic redundancy check for error detection.
- **ACK Slot:** Acknowledgement from receiving ECUs.
- **End of Frame:** Marks the end of the CAN frame.

### Security Risks: Hacking CAN-BUS Messages

The lack of encryption in the CAN-BUS protocol exposes vehicles to significant security risks. Attackers who gain access to the CAN-BUS can intercept and modify messages, potentially leading to dangerous outcomes such as unauthorized control over vehicle systems.

### Symmetric Encryption: A Test for CAN-BUS Security

This proof of concept explores using symmetric encryption to secure CAN-BUS messages. By encrypting data before transmission, we can ensure that only authorized ECUs with the correct decryption key can access the information. This approach uses the same key for both encryption and decryption, making it efficient and suitable for the constrained environments typical of automotive systems.

### Test Implementation in Automotive Systems

In this test, symmetric encryption keys are stored on all ECUs involved. The AES 128-bit algorithm is used, known for its strong security and efficient performance.

### Why Use Symmetric Encryption for CAN-BUS?

Symmetric encryption is ideal for securing CAN-BUS messages due to its efficiency and speed. While this test implementation is not intended for commercial use, it demonstrates the feasibility of encrypting bulk data with minimal computational overhead in a real-time automotive environment.

### Implementing the Test: Python Example

Below is a Python-based test implementation of symmetric encryption for CAN-BUS messages. The `cryptography` and `python-can` libraries are utilized for this purpose.

### Setting Up a Virtual CAN Adapter

Begin by creating a virtual CAN socket to simulate CAN-BUS communication:

```python
import subprocess

subprocess.call('sudo modprobe vcan', shell=True)
subprocess.call('sudo ip link add dev vcan0 type vcan', shell=True)
subprocess.call('sudo ip link set up vcan0', shell=True)
```

### Encrypting and Sending CAN Messages

This script encrypts a CAN message and transmits it over the virtual CAN adapter:

```python
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
```

```bash
$ python sender.py

Encryption key generated and stored.


Encrypted message:
 b'gAAAAABmt76d-RnkRuA-zt6Vzbm_QWTpO2EuwRrt3uk1gKWYrFiFS4X4VSXg9GAwRE57HPRKUBcQq4HqbOukNoZ9vH8z9nsflQeMbIryFx9gnOD-fwyYBzU='

Message sent on socketcan channel 'vcan0'
```

### Receiving and Decrypting CAN Messages

This script receives and decrypts the CAN message:


```python
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
```

```bash
$ python receiver.py

Received encrypted message: 62 4f 75 6b 4e 6f 5a 39     'bOukNoZ9'
......
......
Received encrypted message: 6c 51 65 4d 62 49 72 79     'lQeMbIry' 

Concatenated encrypted message:
 b'gAAAAABmt76d-RnkRuA-zt6Vzbm_QWTpO2EuwRrt3uk1gKWYrFiFS4X4VSXg9GAwRE57HPRKUBcQq4HqbOukNoZ9vH8z9nsflQeMbIryFx9gnOD-fwyYBzU='

This is the original data frame:
 bytearray(b'0 25 0 1 3 1 4 1')

```

This test implementation demonstrates the potential of symmetric encryption for securing CAN-BUS communication in vehicles. While not intended for commercial use, it provides a foundation for further exploration and development of robust security solutions in the automotive industry.

*Written by Vasu*
