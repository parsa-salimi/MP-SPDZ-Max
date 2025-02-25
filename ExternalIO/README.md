The ExternalIO directory contains an example of managing I/O between external client processes and SPDZ parties running SPDZ engines. These instructions assume that SPDZ has been built as per the [project readme](../README.md).

## Working Examples

[bankers-bonus-client.cpp](./bankers-bonus-client.cpp) and
[bankers-bonus-client.py](./bankers-bonus-client.py) act as a
client to [bankers_bonus.mpc](../Programs/Source/bankers_bonus.mpc)
and demonstrates sending input and receiving output as described by
[Damgård et al.](https://eprint.iacr.org/2015/1006) The computation
allows up to eight clients to input a number and computes the client
with the largest input. You can run the C++ code as follows from the main
directory:
```
make bankers-bonus-client.x
./compile.py bankers_bonus 1
Scripts/setup-ssl.sh <nparties>
Scripts/setup-clients.sh 3
Scripts/<protocol>.sh bankers_bonus-1 &
./bankers-bonus-client.x 0 <nparties> 100 0 &
./bankers-bonus-client.x 1 <nparties> 200 0 &
./bankers-bonus-client.x 2 <nparties> 50 1
```

```
make bankers-bonus-client.x
./compile.py bankers_bonus 1
Scripts/setup-ssl.sh 2
Scripts/setup-clients.sh 3
Scripts/mascot.sh bankers_bonus-1 &
./bankers-bonus-client.x 0 2 100 0 &
./bankers-bonus-client.x 1 2 200 0 &
./bankers-bonus-client.x 2 2 50 1
```


`<protocol>` can be any arithmetic protocol (e.g., `mascot`) but not a
binary protocol (e.g., `yao`).
This should output that the winning id is 1. Note that the ids have to
be incremental, and the client with the highest id has to input 1 as
the last argument while the others have to input 0 there. Furthermore,
`<nparties>` refers to the number of parties running the computation
not the number of clients, and `<protocol>` can be the name of
protocol script. The setup scripts generate the necessary SSL
certificates and keys. Therefore, if you run the computation on
different hosts, you will have to distribute the `*.pem` files.

For the Python client, make sure to install
[gmpy2](https://pypi.org/project/gmpy2), and run
`ExternalIO/bankers-bonus-client.py` instead of
`bankers-bonus-client.x`.

## I/O MPC Instructions

### Connection Setup

1. [Listen for clients](https://mp-spdz.readthedocs.io/en/latest/Compiler.html#Compiler.library.listen_for_clients)
2. [Accept client connections](https://mp-spdz.readthedocs.io/en/latest/Compiler.html#Compiler.library.accept_client_connection)
3. [Close client connections](https://mp-spdz.readthedocs.io/en/latest/instructions.html#Compiler.instructions.closeclientconnection)

### Data Exchange

Only the `sint` methods used in the example are documented here, equivalent methods are available for other data types. See [the reference](https://mp-spdz.readthedocs.io/en/latest/Compiler.html#module-Compiler.types).

1. [Public value from client](https://mp-spdz.readthedocs.io/en/latest/Compiler.html#Compiler.types.regint.read_from_socket)
2. [Secret value from client](https://mp-spdz.readthedocs.io/en/latest/Compiler.html#Compiler.types.sint.receive_from_client)
3. [Reveal secret value to clients](https://mp-spdz.readthedocs.io/en/latest/Compiler.html#Compiler.types.sint.reveal_to_clients)

## Client-Side Interface

The example uses the `Client` class implemented in
`ExternalIO/Client.hpp` to handle the communication, see
https://mp-spdz.readthedocs.io/en/latest/io.html#reference for
documentation.


###Our protocol working example
```
make bankers-bonus-client.x
./compile.py bankers_bonus 1
Scripts/setup-ssl.sh 3
Scripts/setup-clients.sh 3
Scripts/mascot.sh bankers_bonus-1
```
Then Open 3 more terminals, and run 1 of the following lines in each 1

```
./ExternalIO/bankers-bonus-client.py 0 2 0,1,0,1,1,0 0
./ExternalIO/bankers-bonus-client.py 1 2 1,0,1,1,0,1 0
./ExternalIO/bankers-bonus-client.py 2 2 1,0,0,1,1,1 1

```

Each line represents a unique client. The first argument is the client_id. The second is the number of parties who are running the computation. The third is the binary vector representing the clients schedule. And the fourth should be a 0, except input a 1 for the last client to run the protocol.

The protocol now will output whether or not each particpant inputed a valid binary array before revealing the outputs. Each particpant must know how many clients are involved in the computation, or there will be a break in the pipeline. The parties should communicate this with the clients. 

To expose a faulty client try change one of the values in the array above to a larger number (or negative number) and the protocol should indicate this as an issue.

