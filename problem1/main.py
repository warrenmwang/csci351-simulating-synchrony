from mpi4py import MPI
from random import randint
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
ith_round = 0

# let's say we end at round 10
end_round = 10

n = comm.Get_size()

# assume a fully connected graph, uniform
# we'll use a nonblocking send
# msg = [sender_id, sender_round]

msg = [rank, ith_round]
# send a message to a random process
j = randint(0, n-1)
while j == rank:
    j = randint(0, n-1)
comm.isend(msg, dest=j)

backlog = []

while ith_round < end_round:
    # wait till we receive a message
    recvRequest = comm.irecv()

    recvTimeCounterStart = time.time()
    receivedMsg = False
    while True:
        recvData = recvRequest.test()
        if recvData[0]:
            receivedMsg = True
            break
        
        if time.time() - recvTimeCounterStart > 0.1:
            break
    
    if receivedMsg:
        sender_id = recvData[1][0]
        jth_round = recvData[1][1]

        if jth_round < ith_round:
            print(f"{ith_round},{rank},{sender_id},{jth_round}")
        else:
            backlog.append(recvData[1])

    # check backlog
    tmp = []
    for item in backlog:
        if item[1] < ith_round:
            print(f"{ith_round},{rank},{sender_id},{jth_round}")
            tmp.append(item)
    for item in tmp:
        backlog.remove(item)

    # send a message to a random process
    new_j = randint(0, n-1)
    while new_j == rank:
        new_j = randint(0, n-1)
    msgToSend = [rank, ith_round] 
    comm.isend(msgToSend, dest=new_j)

    ith_round += 1