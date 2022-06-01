# now, we import the auto-generated python files that contain the definitions from my proto file
import greet_pb2
import greet_pb2_grpc
import time

# importing grpc again, as we are implementing a grpc client in this file.
import grpc

# now, define what the client shall do when we call it
def run():
    # first of all, we need to define to which communication the client should start listening to
    # we better make sure, that this is the same channel as the one the grpc server is communicating on
    with grpc.insecure_channel('localhost:50051') as channel:

        # we're creating a stub which we will be using to call the grpc calls
        stub = greet_pb2_grpc.GreeterStub(channel)
        print("1. Say Hallo - Uniary")
        print("2. ParrotSaysHallo - Server-side Streaming")
        print("3. ChattyClientSaysHallo - Client-side Streaming")
        print("4. InteractingHallo - Bi-directional Streaming")
        rpc_call = input("Which grpc call would you like to call? ")

        if rpc_call == "1":
            # the uniary communication is a ping-pong communication where the client sends the server a message and the server responds.
            # in the proto, we defined, that the HelloRequest, which is implementing that functionality, would get 2 parameters (name/greeting) and would send a response.
            hello_request = greet_pb2.HelloRequest(greeting = "Bonjour", name = "YouTube")

            # now, we finally shoot the message from the client to the server and have a variable ready, that takes the response
            hello_response = stub.SayHello(hello_request)
            print("SayHello Response received: ")
            print(hello_response)

        elif rpc_call == "2":
            print("Not implemented")
        elif rpc_call == "3":
            print("Not implemented")
        elif rpc_call == "4":
            print("Not implemented")

# now we define, that the script shall do if called
# and, well, we just make it call the run function we defined above
# if it's done with the execution, it shall terminate
if __name__ == "__main__":
    run()