from threading import Thread
from concurrent import futures
import time
import io
import csv
import grpc
import demo_pb2_grpc
import demo_pb2

from database_connector import GenericDatabaseConnector

__all__ = 'DemoServer'
SERVER_ADDRESS = '[::]:23333'
SERVER_ID = 1


class DemoServer(demo_pb2_grpc.GRPCDemoServicer):
    def ServerStreamingMethod(self, request, context):
        print("ServerStreamingMethod called by client(%d), message= %s" %
              (request.client_id, request.request_data))


        def response_messages(server_id, sql):
            def data2csv(data):
                file_to_write_stream_data = io.StringIO()
                csv_out = csv.writer(file_to_write_stream_data)
                csv_out.writerows(data)
                value = file_to_write_stream_data.getvalue()
                file_to_write_stream_data.close()
                return value

            def get_results(sql):
                DATA_BASE = GenericDatabaseConnector()
                DATA_BASE.cursor.execute(sql)
                row = DATA_BASE.cursor.fetchmany(10000)
                if len(row) > 0:
                    yield data2csv([[i[0] for i in DATA_BASE.cursor.description]])
                while row:
                    yield data2csv(row)
                    row = DATA_BASE.cursor.fetchmany(10000)

            for row in get_results(sql):
                yield demo_pb2.Response(
                    server_id=SERVER_ID,
                    response_data=(row)
                )


        return response_messages(server_id=SERVER_ID, sql=request.request_data)


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