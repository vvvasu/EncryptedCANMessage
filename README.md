# EncryptedCANMessage
This was an experiment to make awareness of how the CANBUS messages could encrypt with symmetric cryptographic functions

#Instruction for the project deployment

Import following modules to your IDE: 
Import "python-can" - https://python-can.readthedocs.io/en/master/installation.html
Import "cyptography" - https://cryptography.io/en/latest/

Create a Virtual CAN adapter - refer to the "automatecanopen.py"

Run the CAN reciever then the CAN sender.
  CAN reciever - ecu_2.py 
  CAN sender - ecu_1.py
  
Note: This program is coded with simple python scripts. You can get a basic explanation of how a pre-coded 8 byte, raw CAN Message could encrypt using a cryptographic method. 


