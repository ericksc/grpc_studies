import time
import grpc

import demo_pb2_grpc
import demo_pb2
from timer import timing
__all__ = [
    'server_streaming_method'
]

SERVER_ADDRESS = "192.168.100.4:23333"
CLIENT_ID = 100000

@timing(current_module=__file__)
def server_streaming_method(stub):
    print("--------------Call ServerStreamingMethod Begin--------------")
    request = demo_pb2.Request(client_id=CLIENT_ID,
                               request_data="called by Python client")
    response_iterator = stub.ServerStreamingMethod(request)
    for response in response_iterator:
        print("recv from server(%d), message=%s" %
              (response.server_id, response.response_data))

    print("--------------Call ServerStreamingMethod Over---------------")

def close(channel):
    "Close the channel"
    channel.close()


def main():
    with grpc.insecure_channel(SERVER_ADDRESS) as channel:
        stub = demo_pb2_grpc.GRPCDemoStub(channel)
        server_streaming_method(stub)
        channel.unsubscribe(close)


if __name__ == '__main__':
    main()