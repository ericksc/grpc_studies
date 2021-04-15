import time
import grpc
import io
import json

import pandas as pd

import demo_pb2_grpc
import demo_pb2

from timer import timing

__all__ = [
    'server_streaming_method'
]

SERVER_ADDRESS = "192.168.100.4:23333"
CLIENT_ID = 1

@timing(current_module=__file__)
def server_streaming_method(stub, session_id, sql, client_id):
    print("--------------Call ServerStreamingMethod Begin--------------")
    request_data={}
    request_data["info"] = "called by Python client"

    request_data["sql"] = sql
    request_data["session_id"] = session_id

    request = demo_pb2.Request(client_id=CLIENT_ID,
                               request_data=json.dumps(request_data))
    response_iterator = stub.ServerStreamingMethod(request)
    file_to_write_stream_data = io.StringIO()

    for response in response_iterator:
        file_to_write_stream_data.write(response.response_data)

    # Pointing the file like object to the beginning
    file_to_write_stream_data.seek(0)
    try:
        rcv_df = pd.read_csv(file_to_write_stream_data, sep=',')
    except pd.errors.EmptyDataError:
        rcv_df = pd.DataFrame()
        print('DataFrame is empty')
    file_to_write_stream_data.close()

    return rcv_df


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