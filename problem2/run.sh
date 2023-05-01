
echo "Running a system of 3 proccesses over 4 Rounds where each process sends a respective message to every other process" 
mpiexec -n 3 python main.py SendReceive.py --n 3

echo ""
echo "The above output prints the messages received by each process in the order that they were received. The rounds each message was sent is tagged in the message and all messages are in order according to the rounds"