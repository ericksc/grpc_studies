from threading import Thread
from concurrent import futures
import time
import grpc
import demo_pb2_grpc
import demo_pb2

__all__ = 'DemoServer'
SERVER_ADDRESS = 'localhost:23333'
SERVER_ID = 1


class DemoServer(demo_pb2_grpc.GRPCDemoServicer):
    def ServerStreamingMethod(self, request, context):
        print("ServerStreamingMethod called by client(%d), message= %s" %
              (request.client_id, request.request_data))


        def response_messages():
            for i in range(5):
                time.sleep(10)
                response = demo_pb2.Response(
                    server_id=SERVER_ID,
                    response_data=("send by Python server, message=%d" % i))
                yield response

        return response_messages()


def main():
    server = grpc.server(futures.ThreadPoolExecutor())

    demo_pb2_grpc.add_GRPCDemoServicer_to_server(DemoServer(), server)

    server.add_insecure_port(SERVER_ADDRESS)
    print("------------------start Python GRPC server")
    server.start()
    server.wait_for_termination()

    # If raise Error:
    #   AttributeError: '_Server' object has no attribute 'wait_for_termination'
    # You can use the following code instead:
    # import time
    # while 1:
    #     time.sleep(10)


if __name__ == '__main__':
    main()