#!/usr/bin/python3

import sys

sys.path.append('.')

from client import *
from domains import *

client_id = int(sys.argv[1])
n_parties = int(sys.argv[2])
bonus = sys.argv[3].split(",")
finish = int(sys.argv[4])

client = Client(['localhost'] * n_parties, 14000, client_id)

type = client.specification.get_int(4)

if type == ord('R'):
    domain = Z2(client.specification.get_int(4))
elif type == ord('p'):
    domain = Fp(client.specification.get_bigint())
else:
    raise Exception('invalid type')

for socket in client.sockets:
    os = octetStream()
    os.store(finish)
    os.Send(socket)

client.send_private_inputs([domain(int(y)) for y in bonus])

print('Winning index value is :',
        client.receive_outputs(domain, 1)[0].v % 2 ** 64)
