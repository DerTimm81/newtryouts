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

of course, we need to read the weather data from the davis weather station
we do that with the help of a library, we need to install via the below pip
plesae note that the library will only try to connect to a weatherlink module in the current local network
--> pip3 install weatherlink-live-local

CHECK IF STILL NEEDED
in order to get the code run for the weatherlink connected functionality, we need the requests package that we will also install using pip
--> pip3 install requests

We will need numpy
--> pip3 install numpy

And pandas
--> pip3 install pandas

and tzlocal
--> pip3 install tzlocal

and matplotlib
--> pip3 install matplotlib 

in some cases, you need to accept ssl protection to the weatherlink homepage
in order now to allow python to do such kind of request, we need to install certifi
--> pip3 install certifi

and we might want to display some of the values we get. For that, we have a display-call that we need the IPython package for
--> pip3 install IPython  

we also want to have an auto-generated source code documentation. For that, we need to install a package
--> pip3 install pdoc3


Running the python code
------------------------

IMPORTANT: Common issue is the fact that you do not save and re-run the scripts before executing. In those cases, error messages occur as the server is not understanding your request.

you will always want to start the grpc server first by calling
--> python3 greet_server.py

then, you want to run the client
--> python3 greet_client.py