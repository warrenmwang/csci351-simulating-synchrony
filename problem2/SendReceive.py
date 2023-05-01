from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank() 

n = comm.Get_size() 

messages = [] 

'''
send a message from process = process to respective processes
messageList -> list of messages to send respective processes i.e messageList[0] = message to be sent to p0
'''
def lowLevelSend(process,messageList,round): 
    if process == rank: 
        #Iterate over all processes
        for i in range(n): 
            if (i != rank): 
                msg = [rank, messageList[i],round]
                #Send message
                comm.isend(msg, dest = i,tag = 0)
                # print("Sent " + str(msg[1]) + " to " + str(i))

                #Get validation response from Pi 
                recvRequest = comm.irecv(source = i, tag = 1)
                while True: 
                    recvData = recvRequest.test() 
                    if recvData[0]: 
                        msg = recvData[1]
                        
                        if msg[1] == round: 
                            # print(str(rank) + " Received Validation From " + str(msg[0]) + " in round " + str(msg[1]))
                            break
        
        #After send a message to all processes saying the next sender in the round can begin 
        for i in range(n):
            if i != process:
                comm.isend(process+1,dest = i, tag = 3)

'''
Function to handle message receiving in round i 
'''
def receive(round): 
    #Receive a message
    recvRequest = comm.irecv(tag = 0)
    while True: 
        recvData = recvRequest.test() 
        if recvData[0]: 
            senderID = recvData[1][0]
            msg = recvData[1]
            # print(str(rank) + "Received " + str(msg))
            if msg[2] == round: 
                #Send validation to sender
                comm.isend([rank,round],dest = senderID,tag = 1)
                messages.append(str(msg[1]))
                break
    return msg 


'''
High level send to handle sending and receiving of messages in order 
process -> current process that is responsible for sending messages. All other messages will be in receive mode
'''
def highLevelSend(process,message,round):

    if rank == process:
        #If its your turn to send message
        lowLevelSend(process,message,round)

        if process == n-1: 
            #The last process indicates its time to move to the next round
            for i in range(n):
                if i != process:
                    comm.isend(round+1, dest = i, tag = 4)
            return n
        return process+1
    else: 
        #If it is not your turn to send look to receive and validate 
        receive(round)

    #Wait to hear which process is next in line to be the sender 
    recvRequest = comm.irecv(tag = 3,source = process)
    while True: 
        recvData = recvRequest.test() 
        if recvData[0]: 
            nextProcess = recvData[1]
            # print("curProcess " + str(rank) + " Next Proccess = " + str(nextProcess))
            break

    return nextProcess


