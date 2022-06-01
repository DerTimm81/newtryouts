# this import will allow me to see and define the number of workers on my server
from concurrent import futures

# this import will help me to understand some timing aspects when streaming
import time

# this import will provide me some functionalities around grpc
import grpc

# now, we import the auto-generated python files that contain the definitions from my proto file
import greet_pb2
import greet_pb2_grpc

# now, we create the server for my micro service architecture
# we will also implement the services that we defined in the proto-file inside the Greeter
class GreeterServicer(greet_pb2_grpc.GreeterServicer):
    # uniary
    def SayHello(self, request, context):
        # let's first print out what we received from a client
        print("Received Request from Say Hello: ")
        print(request)

        # now, we specify the response to the received message
        # we do that in the first step by defining the message format for our response
        hello_reply = greet_pb2.HelloReply()

        # from the proto, we know that the return will be a string
        # we use some string formatting to simply convert the individual strings received into one string sent back
        hello_reply.message = f"{request.greeting} {request.name}"

        return hello_reply


    # server-side streaming
    def ParrotSaysHello(self, request, context):
        return super().ParrotSaysHello(request, context)

    # client-side streaming
    def ChattyClientSaysHello(self, request_iterator, context):
        return super().ChattyClientSaysHello(request_iterator, context)

    # bi-directional streaming
    def InteractingHello(self, request_iterator, context):
        return super().InteractingHello(request_iterator, context)


# now as we defined what the server shall be able to implement, we init the server itself

def serve():
    # in the function call, we are now able to define the number of workers with the futures package
    # this is a plan definition and does not yet define, which interfaces the server shall be able to support
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))

    # now we define, that interfaces the server shall support by linking it to our GreeterServicer definitions from above
    greet_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(),server)

    # now we define, via which port the server shall send/receive messages
    server.add_insecure_port("localhost:50051")

    # now, we're all set with the config but need to finally make the server start to work.
    server.start()

    print("Started Server")

    # as we want the server to stop operating once we exit on the command line, we add a termination criteria
    server.wait_for_termination()

# now we make the serve functionality run as soon as we execute this python file
if __name__ == "__main__":
    serve()