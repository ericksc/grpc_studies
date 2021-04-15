import time
import grpc

import demo_pb2_grpc
import demo_pb2
import client as fast_client
import slow_client as slow_client

from multiprocessing import Process

def main():
    COUNT = 10
    PROCESSES = {}

    PROCESSES[f'slow'] = Process(target=slow_client.main)
    PROCESSES[f'fast_0'] = Process(target=fast_client.main)
    PROCESSES[f'fast_1'] = Process(target=fast_client.main)
    # PROCESSES[f'fast_2'] = Process(target=fast_client.main)
    # PROCESSES[f'fast_3'] = Process(target=fast_client.main)
    # PROCESSES[f'fast_4'] = Process(target=fast_client.main)
    # PROCESSES[f'fast_5'] = Process(target=fast_client.main)
    # PROCESSES[f'fast_6'] = Process(target=fast_client.main)
    # PROCESSES[f'fast_7'] = Process(target=fast_client.main)
    # PROCESSES[f'fast_8'] = Process(target=fast_client.main)
    # PROCESSES[f'fast_9'] = Process(target=fast_client.main)

    for p in PROCESSES.keys():
        PROCESSES[p].start()

if __name__ == '__main__':
    main()