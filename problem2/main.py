import SendReceive 
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank() 

n = comm.Get_size() 

# SendReceive.highLevelSend(0,["P0","P1","P2","P3"],1)
twoDimensionalMsg = [["P0->P0","P0->P1","P0->P2"],["P1->P0","P1->P1","P1->P2"],["P2->P0","P2->P1","P2->P2"]]

def simulateRound(round): 
        nextProcess = 0
        while (nextProcess < n):
            nextProcess = SendReceive.highLevelSend(nextProcess,twoDimensionalMsg[rank],round)

        if rank == n-1: 
             return round+1
        
        recvRequest = comm.irecv(tag = 4)
        while True: 
            recvData = recvRequest.test() 
            if recvData[0]: 
                print("MOVNG ON " + str(recvData))
                if recvData[1] == round+1: 
                    return round+1

totalRounds = 6
i = 1

while i < totalRounds: 
    print("round " + str(i))
    twoDimensionalMsg = [[ "Round " + str(i) + " P0->P0","Round " + str(i) + " P0->P1","Round " + str(i) + " P0->P2"],["Round " + str(i) + " P1->P0","Round " + str(i) + " P1->P1","Round " + str(i) + " P1->P2"],["Round " + str(i) + " P2->P0","Round " + str(i) + " P2->P1","Round " + str(i) + " P2->P2"]]
    print(simulateRound(i))
    i+=1
      
print(SendReceive.messages)