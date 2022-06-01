# now, we import the auto-generated python files that contain the definitions from my proto file
import greet_pb2
import greet_pb2_grpc
import time

# importing grpc again, as we are implementing a grpc client in this file.
import grpc

# if we want a client to send multiple messages to the server before it responds
# we need to have a little helper functionality here
# we will call that in the chatty client example, where the client is sending multiple messages before the server replies.
def get_client_stream_requests():
    while True:
        name = input("Please enter a name (or nothing to stop chatting): ")

        if name == "":
            break

        hello_request = greet_pb2.HelloRequest(greeting="Hello", name=name)
        yield hello_request
        time.sleep(1)


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

        ######################################
        # Uniary Communication
        # this means, the client sends one request to the server
        # the server will respond to the client with one answer
        if rpc_call == "1":
            # the uniary communication is a ping-pong communication where the client sends the server a message and the server responds.
            # in the proto, we defined, that the HelloRequest, which is implementing that functionality, would get 2 parameters (name/greeting) and would send a response.
            hello_request = greet_pb2.HelloRequest(greeting = "Bonjour", name = "YouTube")

            # now, we finally shoot the message from the client to the server and have a variable ready, that takes the response
            hello_response = stub.SayHello(hello_request)
            print("SayHello Response received: ")
            print(hello_response)

        ###################################
        # Server-side Streaming
        # Means: The client sends a request to the server
        # the server will start to continously send replies up until the server decides itself to stop
        elif rpc_call == "2":
            # we just start again by building the message we intend to send to the server
            hello_request = greet_pb2.HelloRequest(greeting="Bonjour",name="YouTube")

            # we shoot the message over the fence to the server
            hello_replies = stub.ParrotSaysHello(hello_request)

            # and now, we need to prepare for the replies
            # we keep printing out the responses up until the server decides to stop
            for hello_reply in hello_replies:
                print("Parrot Says Hello Message Received: ")
                print(hello_reply)

        ########################################
        # client-side streaming
        elif rpc_call == "3":
            delayed_reply = stub.ChattyClientSaysHello(get_client_stream_requests())

            print("ChattyClientSaysHello Response Received:")
            print(delayed_reply)

        ################################
        # Bi-directional Streaming
        # a typical use case is a chat program where both parties can text messages and shoot them over the fence

        elif rpc_call == "4":
            # we simulate a client side input that is shot over the fence to the server as they occur
            responses = stub.InteractingHello(get_client_stream_requests())

            for response in responses:
                print("Interacting Say Hello Response Received: ")
                print(response)

# now we define, that the script shall do if called
# and, well, we just make it call the run function we defined above
# if it's done with the execution, it shall terminate
if __name__ == "__main__":
    run()