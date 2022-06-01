# this import will allow me to see and define the number of workers on my server
from concurrent import futures
from email import message

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

    ##################################################
    # Uniary Communication
    # means more or less a ping-pong communication
    # The client is sending a request to the server
    # the server responds with a response
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


    ################################################
    # Server-side streaming
    # means, once the client decides to go for this message, the server keeps sending messages
    def ParrotSaysHello(self, request, context):
        print("Parrt Says Hello Request Message Received: ")
        print(request)

        # of course, we do not want to run infinitely throught the communication
        # that would make us want to kill the service
        # therefore, we define a little loop that will stop the broadcast after 3 messages
        for i in range(3):
            hello_reply = greet_pb2.HelloReply()
            hello_reply.message = f"{request.greeting} {request.name} {i + 1}"

            # if you do streaming, you do not actually return once, but you yield
            yield hello_reply

            # for us now to see that there is really a time sequence, we will add a little sleep function
            time.sleep(3)


    # client-side streaming
    def ChattyClientSaysHello(self, request_iterator, context):
        delayed_reply = greet_pb2.DelayedReply()
        for request in request_iterator:
            print("ChattyClientSaysHello Request Made:")
            print(request)
            delayed_reply.request.append(request)

        delayed_reply.message = f"You have sent {len(delayed_reply.request)} messages. Please expect a delayed response."
        return delayed_reply

    # bi-directional streaming
    def InteractingHello(self, request_iterator, context):
        
        # we want to print out every request the server receives from a client whenever it comes in
        for request in request_iterator:
            print("Interactive Hello Request Received")
            print(request)

            hello_reply = greet_pb2.HelloReply()
            hello_reply.message = f"{request.greeting} {request.name}"

            # as we do not want to close that function, we go with yield and wait for the next message to come
            yield hello_reply


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