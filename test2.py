from game_blocks.base_block import CPUBlock
from communication.messages import SetTargetMessage
import logging

logging.basicConfig(level=logging.INFO)

with CPUBlock(server_port=80) as cpu0, CPUBlock(server_port=81) as cpu1, CPUBlock(server_port=82) as cpu2:
    print(id(cpu0), id(cpu1), id(cpu2))

    target_cpu0 = SetTargetMessage("127.0.0.1:80")
    target_cpu1 = SetTargetMessage("127.0.0.1:81")
    target_cpu2 = SetTargetMessage("127.0.0.1:82")
    target_cpu3 = SetTargetMessage("127.0.0.1:83")

    cpu0.target = "127.0.0.1:80"
    cpu0.send_message(target_cpu1)
    cpu0.send_message(target_cpu0)
    cpu1.send_message(target_cpu2)
    cpu0.send_message(target_cpu1)
    cpu2.send_message(target_cpu0)
    cpu1.send_message(target_cpu0)
    cpu0.send_message(target_cpu3)
    print(0, cpu0.target)
    print(1, cpu1.target)
    print(2, cpu2.target)
