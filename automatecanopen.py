import subprocess


subprocess.call('sudo modprobe vcan', shell=True)
subprocess.call('sudo ip link add dev vcan0 type vcan', shell=True)
subprocess.call('sudo ip link set up vcan0', shell=True)
