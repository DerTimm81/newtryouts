# newtryouts
new try

Before you can run the python code
-----------------------------------

update the pip package installer for pyhton3
--> pip3 install --upgrade pip

install the grpc package
--> pip3 install grpcio

install the tools around grpc
--> pip3 install grpcio-tools

once the framework is in place, we need to compile the proto file via the protoc-compiler that is generating the python files for us
We will ask the compiler to store the compiled files in the same folder as the proto-file itself
--> python3 -m grpc_tools.protoc -I config/protos --python_out=. --grpc_python_out=. config/protos/greet.proto

Running the python code
------------------------

you will always want to start the grpc server first by calling
--> python3 greet_server.py

then, you want to run the client
--> python3 greet_client.py