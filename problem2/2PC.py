import SendReceive 
from main import simulateRound 
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank() 

n = comm.Get_size()

msg_matrix = [["NULL" for i in range(n)] for j in range(n)]


state = "INIT"

coordinator_rank = 0
participant_ranks = range(1, n)
num_rounds = 2

def commit():
    msg_matrix[0] = ["COMMIT" for i in range(n)]

def abort():
    msg_matrix[0] = ["ABORT" for i in range(n)]

def all_votes_commit():
    return all(msg == "COMMIT" for msg in SendReceive.messages) and len(SendReceive.messages) == n-1

for round in range(1, num_rounds+1):
    #Phase 1
    if round%2 == 1:
        msg_matrix[0] = ["VOTE_REQUEST" for i in range(n)]
        for i in participant_ranks:
            msg_matrix[i][0] = "COMMIT" # or "ABORT"
        #msg_matrix[1][0] = "ABORT"
       
        simulateRound(round, msg_matrix)
    #Phase 2
    if round%2 == 0:
        if rank == coordinator_rank:
            if all_votes_commit():
                commit()
            else:
                abort()
        simulateRound(round, msg_matrix)
        
        if rank in participant_ranks:
            if SendReceive.messages[1] == "COMMIT":
                state = "COMMIT"
            else:
                state = "ABORT"
            print("Process", rank, "is in state", state)


#CITATIONS : Chapter 8 Principles of Transaction Processing, 2nd Edition, Philip A. Bernstein, Eric Newcomer, 1997,

