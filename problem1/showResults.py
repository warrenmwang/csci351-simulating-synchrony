import sys

# {ith_round},{rank},{sender_id},{jth_round} 

d = {}

inFile = sys.argv[1]
with open(inFile, "r") as f:
    x = f.readlines()
    for l in x:
        tmp = l.split(",")
        ith_round = int(tmp[0])
        rank = int(tmp[1])
        sender_id = int(tmp[2])
        jth_round = int(tmp[3])

        if ith_round not in d:
            d[ith_round] = []
        d[ith_round].append(f"P{rank} received a msg from P{sender_id} sent from round {jth_round}")


for round in d:
    print(f"Round {round}:")
    for msg in d[round]:
        print(f"\t{msg}")
    print()
