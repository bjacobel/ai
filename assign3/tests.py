import re
f = open("results", "rb")

total_moves = 0
total_time = 0

for line in f.readlines():
    if re.match("New game.", line):
        if total_moves + total_time > 0:
            print("Total moves: {}   Total time: {}".format(total_moves, total_time))
        total_moves = 0
        total_time = 0
    elif line == "":
        continue
    elif re.match(r'\w+', line):
        total_moves += int(re.findall(r'\d+', line)[0])
        total_time += int(re.findall(r'\d+', line)[1])



