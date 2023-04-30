from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank() 

n = comm.Get_size() 

messages = [] 

def lowLevelSend(process,messageList,round): 
    count = 0; 
    if process == rank: 
        for i in range(n): 
            if (i != rank): 
                msg = [rank, messageList[i],round]
                comm.isend(msg, dest = i,tag = 0)
                print("Sent " + str(msg[1]) + " to " + str(i))

                recvRequest = comm.irecv(source = i, tag = 1)
                while True: 
                    recvData = recvRequest.test() 
                    if recvData[0]: 
                        msg = recvData[1]
                        
                        if msg[1] == round: 
                            print(str(rank) + "Received Validation From " + str(msg[0]) + " in round " + str(msg[1]))
                            break
        for i in range(n):
            if i != process:
                comm.isend(process+1,dest = i, tag = 3)

def receive(round): 
    recvRequest = comm.irecv(tag = 0)
    while True: 
        recvData = recvRequest.test() 
        if recvData[0]: 
            senderID = recvData[1][0]
            msg = recvData[1]
            # print(str(rank) + "Received " + str(msg))
            if msg[2] == round: 
                
                comm.isend([rank,round],dest = senderID,tag = 1)
                messages.append(round)
                break
    return msg 

def highLevelSend(process,message,round):
    if rank == process:
        lowLevelSend(process,message,round)

        if process == n-1: 
            for i in range(n):
                if i != process:
                    comm.isend(round+1, dest = i, tag = 4)
            return n
        return process+1
    else: 
        receive(round)

    recvRequest = comm.irecv(tag = 3,source = process)
    while True: 
        recvData = recvRequest.test() 
        if recvData[0]: 
            nextProcess = recvData[1]
            # print("curProcess " + str(rank) + " Next Proccess = " + str(nextProcess))
            break

    return nextProcess
    
    



