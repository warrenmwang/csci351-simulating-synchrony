import SendReceive 
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank() 

n = comm.Get_size() 

twoDimensionalMsg = [["P0->P0","P0->P1","P0->P2"],["P1->P0","P1->P1","P1->P2"],["P2->P0","P2->P1","P2->P2"]]

'''
Function to simulate a round 
Iterates over all processes each taking a turn to send their respective messages

twoDimensionMsg -> 2d array of messages to send in current round where msg[i][j] is the message
pi will send to pj in the current round 
'''
def simulateRound(round,twoDimensionalMsg): 
        #Iterate over all processes to each get a turn to be sender 
        nextProcess = 0
        while (nextProcess < n):
            nextProcess = SendReceive.highLevelSend(nextProcess,twoDimensionalMsg[rank],round)


        if rank == n-1: 
             return round+1
        
        #wait to get validation that the current roound is over
        recvRequest = comm.irecv(tag = 4)
        while True: 
            recvData = recvRequest.test() 
            if recvData[0]: 
                if recvData[1] == round+1: 
                    return round+1

# totalRounds = 5
# i = 1
#
# while i < totalRounds: 
#
#     twoDimensionalMsg = [[ "Round " + str(i) + " P0->P0","Round " + str(i) + " P0->P1","Round " + str(i) + " P0->P2"],["Round " + str(i) + " P1->P0","Round " + str(i) + " P1->P1","Round " + str(i) + " P1->P2"],["Round " + str(i) + " P2->P0","Round " + str(i) + " P2->P1","Round " + str(i) + " P2->P2"]]
#     (simulateRound(i,twoDimensionalMsg))
#     i+=1 
#
# print("P_"+str(rank)+" List of Recieved Messages: " + str(SendReceive.messages)+"\n")
